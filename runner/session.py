from dataclasses import dataclass
from typing import Dict, Any, List, Optional

@dataclass
class SessionResult:
    scenario_id: str
    title: str
    messages: List[Dict[str, str]]
    agent_structured: Dict[str, Any]
    hard_results: Dict[str, bool]
    metrics: Dict[str, float]
    passed: bool
    tags: List[str] = None
    strategy: str = "FlowIntent"
    policy_profile: str = "default"
    budget_status: Optional[Dict[str, Any]] = None
    budget_violations: List[str] = None
    seed_info: Optional[Dict[str, Any]] = None
    judge_info: Optional[Dict[str, Any]] = None
    llm_result: Optional[Dict[str, Any]] = None
    hybrid_breakdown: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.budget_violations is None:
            self.budget_violations = []
