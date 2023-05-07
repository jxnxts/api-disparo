from celery import group
from fastapi import APIRouter
from starlette.responses import JSONResponse
from config.celery_utils import get_task_info

router = APIRouter(prefix='/queue', tags=['Queue'], responses={404: {"description": "Not found"}})


@router.get("/task/{task_id}")
async def get_task_status(task_id: str) -> dict:
    """
    Return the status of the submitted Task
    """
    return get_task_info(task_id)

