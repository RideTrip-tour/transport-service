import logging

from fastapi import APIRouter, HTTPException, status

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/api/admin/transport", tags=["Admin Transport"])


def raise_not_found():
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Путь не найден.",
    )


@router.post("/stations/sync")
async def sync_stations():
    raise_not_found()


@router.get("/stations/sync/status")
async def get_stations_sync_status():
    raise_not_found()
