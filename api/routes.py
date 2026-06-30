from fastapi import APIRouter, HTTPException
from models.schemas import ResearchRequest, ResearchResponse
from agents.orchestrator import orchestrator

router = APIRouter()

@router.post("/research", response_model=ResearchResponse)
async def research(request: ResearchRequest):
    try:
        result = orchestrator(request.query, request.max_sources)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health():
    return {"status": "ok"}
