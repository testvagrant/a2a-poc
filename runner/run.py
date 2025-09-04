import argparse, time, json, glob
from pathlib import Path
import yaml
from judges.schema_judge import run_hard_assertions, heuristic_soft_metrics
from judges.unified_judge import UnifiedJudge, UnifiedJudgeConfig, UnifiedJudgeFactory, JudgeMode
from judges.llm_judge import LLMJudgeConfig, JudgeType
from config.env_loader import get_config_loader, get_openai_config, get_llm_judge_config, get_uta_config
from reporters.html_report import render_report
from agents.product_adapter_mock import MockProductAgent
from agents.product_adapter_generic import GenericMockAgent
from agents.http_adapter import HTTPAdapter, HTTPAdapterFactory
from agents.strategies.registry import StrategyRegistry
from runner.session import SessionResult
from runner.budget_enforcer import BudgetEnforcer, BudgetViolationError
from runner.seed_manager import SeedManager, SeedConfig, initialize_seed_manager

def load_yaml(path: str):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def validate_scenario(scenario: dict) -> list[str]:
    """Validate scenario against DSL schema."""
    errors = []
    required_fields = ['id', 'title', 'preconditions', 'goal', 'conversation', 'oracle']
    
    for field in required_fields:
        if field not in scenario:
            errors.append(f"Missing required field: {field}")
            
    # Check DSL version
    if 'dsl_version' not in scenario:
        errors.append("Missing dsl_version field")
        
    # Check conversation structure
    if 'conversation' in scenario:
        conv = scenario['conversation']
        if 'initial_user_msg' not in conv:
            errors.append("Missing initial_user_msg in conversation")
        if 'max_turns' not in conv:
            errors.append("Missing max_turns in conversation")
            
    # Check oracle structure
    if 'oracle' in scenario:
        oracle = scenario['oracle']
        if 'hard_assertions' not in oracle:
            errors.append("Missing hard_assertions in oracle")
        if 'soft_metrics' not in oracle:
            errors.append("Missing soft_metrics in oracle")
            
    return errors

def get_agent_for_scenario(scenario_path: str, fixtures_dir: str, http_config: dict = None):
    """Get the appropriate agent based on scenario type."""
    # If HTTP config is provided, use HTTP adapter
    if http_config:
        if "collections" in scenario_path:
            return HTTPAdapterFactory.create_collections_adapter(
                http_config['base_url'], 
                http_config.get('api_key'),
                http_config.get('model')
            )
        else:
            return HTTPAdapterFactory.create_generic_adapter(
                http_config['base_url'], 
                http_config.get('api_key'),
                http_config.get('model')
            )
    
    # Otherwise use mock agents
    if "collections" in scenario_path:
        return MockProductAgent(fixtures_dir)
    else:
        return GenericMockAgent(fixtures_dir)

def _initialize_judge(args):
    """Initialize judge based on command line arguments and environment configuration."""
    if args.judge_config:
        # Load judge configuration from file
        with open(args.judge_config, 'r') as f:
            config_dict = yaml.safe_load(f)
        return UnifiedJudgeFactory.create_from_config(config_dict)
    
    # Create judge based on command line arguments
    mode = JudgeMode(args.judge_mode)
    
    if mode == JudgeMode.HEURISTIC:
        return UnifiedJudgeFactory.create_heuristic_judge()
    
    elif mode in [JudgeMode.LLM, JudgeMode.HYBRID]:
        # Try to get LLM configuration from environment first
        try:
            env_llm_config = get_llm_judge_config()
            judge_type_map = {
                'openai': JudgeType.OPENAI,
                'anthropic': JudgeType.ANTHROPIC,
                'azure': JudgeType.AZURE
            }
            
            llm_config = LLMJudgeConfig(
                judge_type=judge_type_map.get(env_llm_config.judge_type, JudgeType.OPENAI),
                model_name=env_llm_config.model,
                api_key=env_llm_config.api_key,
                base_url=env_llm_config.base_url,  # Use configured base URL for judge
                temperature=env_llm_config.temperature,
                max_tokens=env_llm_config.max_tokens
            )
            
            print(f"✅ Using LLM Judge from environment: {env_llm_config.model}")
            
        except ValueError:
            # Fall back to command line arguments
            print("⚠️ LLM Judge config not found in environment, using command line arguments")
            judge_type_map = {
                'openai': JudgeType.OPENAI,
                'anthropic': JudgeType.ANTHROPIC,
                'azure': JudgeType.AZURE
            }
            
            llm_config = LLMJudgeConfig(
                judge_type=judge_type_map[args.llm_type],
                model_name=args.llm_model,
                api_key=args.llm_api_key
            )
        
        if mode == JudgeMode.LLM:
            return UnifiedJudgeFactory.create_llm_judge(llm_config)
        else:  # HYBRID
            return UnifiedJudgeFactory.create_hybrid_judge(llm_config)
    
    else:
        raise ValueError(f"Unsupported judge mode: {mode}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--suite', required=True, help='Path to scenarios directory')
    ap.add_argument('--report', required=True, help='Output directory for report')
    ap.add_argument('--fixtures', default='fixtures', help='Fixtures directory')
    ap.add_argument('--profile', default='default', help='Policy profile to use')
    ap.add_argument('--tags', nargs='*', help='Filter scenarios by tags')
    ap.add_argument('--seed', type=int, help='Random seed for deterministic runs')
    
    # HTTP adapter options
    ap.add_argument('--http-url', help='HTTP URL for real agent integration')
    ap.add_argument('--http-api-key', help='API key for HTTP authentication')
    ap.add_argument('--http-config', help='Path to HTTP configuration file')
    
    # Judge options
    ap.add_argument('--judge-mode', choices=['heuristic', 'llm', 'hybrid'], 
                   default='heuristic', help='Judge mode to use')
    ap.add_argument('--llm-api-key', help='API key for LLM judge')
    ap.add_argument('--llm-model', default='gpt-3.5-turbo', help='LLM model for judge')
    ap.add_argument('--llm-type', choices=['openai', 'anthropic', 'azure'], 
                   default='openai', help='LLM provider type')
    ap.add_argument('--judge-config', help='Path to judge configuration file')
    
    args = ap.parse_args()

    suite_dir = Path(args.suite)
    scenarios = sorted(glob.glob(str(suite_dir / '*.yaml')))
    if not scenarios:
        raise SystemExit(f'No scenarios found in {suite_dir}')

    # Initialize components
    strategy_registry = StrategyRegistry()
    
    # Initialize seed manager for deterministic runs
    seed_config = SeedConfig(
        seed=args.seed,
        auto_seed=True if args.seed is None else False
    )
    seed_manager = initialize_seed_manager(seed_config)
    
    # Initialize judge
    judge = _initialize_judge(args)
    
    # Set up HTTP configuration
    http_config = None
    if args.http_url:
        http_config = {
            'base_url': args.http_url,
            'api_key': args.http_api_key
        }
    elif args.http_config:
        with open(args.http_config, 'r') as f:
            http_config = yaml.safe_load(f)
    else:
        # Try to get HTTP configuration from environment
        try:
            openai_config = get_openai_config()
            http_config = {
                'base_url': openai_config.base_url,
                'api_key': openai_config.api_key,
                'model': openai_config.model
            }
            print(f"✅ Using HTTP config from environment: {openai_config.base_url}")
        except ValueError:
            print("ℹ️ No HTTP configuration found in environment or command line")
    
    # Filter scenarios by tags if specified
    if args.tags:
        filtered_scenarios = []
        for path in scenarios:
            sc = load_yaml(path)
            sc_tags = sc.get('tags', [])
            if any(tag in sc_tags for tag in args.tags):
                filtered_scenarios.append(path)
        scenarios = filtered_scenarios
        if not scenarios:
            raise SystemExit(f'No scenarios match tags: {args.tags}')

    sessions = []
    start = time.time()

    for path in scenarios:
        sc = load_yaml(path)
        
        # Validate scenario
        validation_errors = validate_scenario(sc)
        if validation_errors:
            print(f"Warning: Scenario {sc.get('id', 'unknown')} has validation errors:")
            for error in validation_errors:
                print(f"  - {error}")
            continue
            
        messages = []
        debtor_id = sc['preconditions'].get('debtor_id', 'D-1001')
        policy_profile = sc['preconditions'].get('policy_profile', args.profile)
        
        # Get appropriate agent for this scenario
        product = get_agent_for_scenario(path, args.fixtures, http_config)
        
        # Get strategy
        strategy_name = sc['conversation'].get('tester_strategy', 'FlowIntent')
        strategy = strategy_registry.get(strategy_name)
        if not strategy:
            print(f"Warning: Unknown strategy '{strategy_name}', using default")
            strategy = strategy_registry.get_default()

        # Initialize budget enforcer
        budget_config = sc.get('budgets', {})
        budget_enforcer = BudgetEnforcer(budget_config)
        
        last_structured = {}
        last_resp = None
        budget_violations = []
        
        # Run conversation
        turn = 0
        while budget_enforcer.should_continue():
            # Send user message (first message or next from strategy)
            if turn == 0:
                # First turn - use strategy's first message
                user_msg = strategy.first_message(sc)
            else:
                # Subsequent turns - get next message from strategy
                user_msg = strategy.next_message(last_resp, sc)
                if not user_msg:
                    # Strategy doesn't want to continue
                    break
                    
            messages.append({'role': 'user', 'content': user_msg})
            
            # Get agent response with timing
            turn_start = time.time()
            resp = product.send(messages, debtor_id=debtor_id)
            turn_latency = (time.time() - turn_start) * 1000  # Convert to milliseconds
            
            messages.append({'role': 'assistant', 'content': resp['text']})
            last_structured = resp.get('structured', {})
            last_resp = resp
            
            # Estimate cost for this turn
            user_msg_len = len(user_msg)
            resp_len = len(resp.get('text', ''))
            estimated_cost = budget_enforcer.estimate_turn_cost(user_msg_len, resp_len)
            
            # Record turn and check budget constraints
            if not budget_enforcer.record_turn(turn_latency, estimated_cost):
                budget_violations = budget_enforcer.violations.copy()
                break
            
            # Check if strategy wants to continue
            if not strategy.should_continue(messages, sc):
                break
                
            turn += 1

        # Run unified evaluation
        evaluation_result = judge.evaluate(sc, messages, last_structured)
        hard = evaluation_result.hard_results
        metrics = evaluation_result.soft_metrics
        
        # Check soft metric thresholds
        thresholds = sc['oracle']['soft_metrics']
        def meets(metric_name, value):
            th = thresholds.get(metric_name, '>=0.0')
            op, num = th[:2], float(th[2:])
            return (value >= num) if op == '>=' else True
        soft_ok = all(meets(k, v) for k, v in metrics.items())
        hard_ok = all(hard.values())
        budget_ok = len(budget_violations) == 0
        passed = hard_ok and soft_ok and budget_ok
        
        # Get budget status
        budget_status = budget_enforcer.get_status()
        
        # Get seed information
        seed_info = seed_manager.get_seed_info()
        
        # Get judge information
        judge_info = judge.get_judge_info()
        
        sessions.append(SessionResult(
            scenario_id=sc['id'],
            title=sc['title'],
            messages=messages,
            agent_structured=last_structured,
            hard_results=hard,
            metrics=metrics,
            passed=passed,
            tags=sc.get('tags', []),
            strategy=strategy_name,
            policy_profile=policy_profile,
            budget_status=budget_status,
            budget_violations=budget_violations,
            seed_info=seed_info,
            judge_info=judge_info,
            llm_result=evaluation_result.llm_result.__dict__ if evaluation_result.llm_result else None,
            hybrid_breakdown=evaluation_result.hybrid_breakdown
        ).__dict__)

    dur = round(time.time() - start, 2)
    # Determine the model being used
    model_name = 'mock-agent'
    if http_config:
        model_name = http_config.get('model', 'http-agent')
    
    summary = {
        'total': len(sessions),
        'pass_count': sum(1 for s in sessions if s['passed']),
        'model': model_name,
        'judge_type': judge.get_judge_info()['mode'],
        'duration_s': dur,
        'policy_profile': args.profile,
        'seed': args.seed,
        'seed_info': seed_manager.get_seed_info(),
        'judge_info': judge.get_judge_info(),
        'tags_filter': args.tags
    }
    
    out = render_report(args.report, summary, sessions)
    print(f'Report written to {out}')
    Path(args.report).mkdir(parents=True, exist_ok=True)
    with open(Path(args.report) / 'results.json', 'w', encoding='utf-8') as f:
        json.dump({'summary': summary, 'sessions': sessions}, f, indent=2)

if __name__ == '__main__':
    main()
