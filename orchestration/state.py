from typing import TypedDict, Optional

# state that gets passed between agents
class AgentState(TypedDict):
    task: str
    architecture: Optional[str]
    code: Optional[str]
    tests: Optional[str]
    review: Optional[str]
    decision: Optional[str]
