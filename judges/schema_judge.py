import re
from typing import Dict, Any, List

def _get_last_agent_text(messages: List[Dict[str,str]], k: int = 2) -> str:
    texts = [m['content'] for m in messages if m['role'] == 'assistant']
    return ' '.join(texts[-k:]) if texts else ''

def _jsonpath_exists(obj: Any, path: str) -> bool:
    if not path.startswith('$.'):
        return False
    keys = path[2:].split('.')
    cur = obj
    for k in keys:
        if isinstance(cur, dict) and k in cur:
            cur = cur[k]
        elif isinstance(cur, list) and k.isdigit() and int(k) < len(cur):
            cur = cur[int(k)]
        else:
            return False
    return cur is not None

def _jsonpath_equals(obj: Any, path: str, expected_value: Any) -> bool:
    """Check if jsonpath value equals expected value."""
    if not path.startswith('$.'):
        return False
    keys = path[2:].split('.')
    cur = obj
    for k in keys:
        if isinstance(cur, dict) and k in cur:
            cur = cur[k]
        elif isinstance(cur, list) and k.isdigit() and int(k) < len(cur):
            cur = cur[int(k)]
        else:
            return False
    return cur == expected_value

def _number_between(value: Any, min_val: float, max_val: float) -> bool:
    """Check if a value is between min and max (inclusive)."""
    try:
        num_val = float(value)
        return min_val <= num_val <= max_val
    except (ValueError, TypeError):
        return False

def _matches_regex(text: str, pattern: str) -> bool:
    """Check if text matches regex pattern."""
    try:
        return bool(re.search(pattern, text, re.IGNORECASE))
    except re.error:
        return False

def run_hard_assertions(oracles: Dict[str, Any], conversation: List[Dict[str, str]], agent_structured: Dict[str, Any]) -> Dict[str, bool]:
    results = {}
    agent_text = _get_last_agent_text(conversation)
    for rule in oracles.get('hard_assertions', []):
        name = rule['name']
        kind = rule['kind']
        passed = True
        
        if kind == 'contains_any':
            vals = [v.lower() for v in rule['values']]
            at = agent_text.lower()
            passed = any(v in at for v in vals)
        elif kind == 'not_contains_any':
            vals = [v.lower() for v in rule['values']]
            at = agent_text.lower()
            passed = all(v not in at for v in vals)
        elif kind == 'matches_regex':
            pattern = rule.get('pattern', '')
            passed = _matches_regex(agent_text, pattern)
        elif kind == 'jsonpath_exists':
            path = rule.get('path', '')
            passed = _jsonpath_exists(agent_structured, path)
        elif kind == 'jsonpath_equals':
            path = rule.get('path', '')
            expected = rule.get('expected_value')
            passed = _jsonpath_equals(agent_structured, path, expected)
        elif kind == 'number_between':
            path = rule.get('path', '')
            min_val = rule.get('min_value', 0)
            max_val = rule.get('max_value', float('inf'))
            value = _get_jsonpath_value(agent_structured, path)
            passed = _number_between(value, min_val, max_val)
        else:
            passed = False
        results[name] = passed
    return results

def _get_jsonpath_value(obj: Any, path: str) -> Any:
    """Get value at jsonpath, return None if not found."""
    if not path.startswith('$.'):
        return None
    keys = path[2:].split('.')
    cur = obj
    for k in keys:
        if isinstance(cur, dict) and k in cur:
            cur = cur[k]
        elif isinstance(cur, list) and k.isdigit() and int(k) < len(cur):
            cur = cur[int(k)]
        else:
            return None
    return cur

def heuristic_soft_metrics(scenario: Dict[str, Any], conversation: List[Dict[str, str]], agent_structured: Dict[str, Any]) -> Dict[str, float]:
    user_goal = scenario.get('goal', {}).get('user_goal', '').lower()
    agent_text = ' '.join([m['content'] for m in conversation if m['role'] == 'assistant']).lower()
    ug_tokens = set([t for t in re.findall(r'[a-z]+', user_goal)])
    at_tokens = set([t for t in re.findall(r'[a-z]+', agent_text)])
    relevance = len(ug_tokens & at_tokens) / max(1, len(ug_tokens)) if ug_tokens else 0.8
    completeness = 0.7
    if 'promise_to_pay' in (agent_structured or {}):
        ptp = agent_structured.get('promise_to_pay')
        completeness = 0.9 if (ptp and ptp.get('date') and ptp.get('amount')) else 0.6
    nums = re.findall(r'\d[\d,]*', agent_text.replace(',', ''))
    groundedness = 0.85 if nums else 0.8
    return {'relevance': float(relevance), 'completeness': float(completeness), 'groundedness': float(groundedness)}
