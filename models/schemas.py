from pydantic import BaseModel
from typing import Optional

class ResearchRequest(BaseModel):
    query: str
    max_sources: Optional[int] = 5

class AgentResult(BaseModel):
    agent: str
    output: str

class ResearchResponse(BaseModel):
    query: str
    summary: str
    fact_check: str
    sources: list[str]
    agents_trace: list[AgentResult]
