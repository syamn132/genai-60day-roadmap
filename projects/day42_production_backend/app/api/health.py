from fastapi import APIRouter


router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("/live")
def liveness_check():
    return {
        "status": "alive",
        "service": "day42-production-backend",
    }
