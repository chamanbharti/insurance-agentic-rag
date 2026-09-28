from fastapi import APIRouter

from app.models.health import HealthResponse

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get(
    "",
    response_model=HealthResponse,
)
async def health_check() -> HealthResponse:
    return HealthResponse(status="UP")
