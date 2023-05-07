from fastapi import APIRouter
from models.request import GruposRequest
from models.response import Response
from models.models import Grupos, Instance
from db.database import Database
from api.zapi import status_instance, get_chats, get_groups, get_qrcode64, disconect, restart, update_call_reject_auto, get_device_info, create_group
from sqlalchemy import and_, desc
import datetime


router = APIRouter(
    prefix="/whatsapp",
    tags=["Controlador do WhatsApp"],
    responses={404: {"description": "Not found"}},
)

database = Database()
engine = database.get_db_connection()


@router.get("/qrcode")
async def get_qrcode(id: int):

    session = database.get_db_session(engine)

    session = database.get_db_session(engine)
    instance = session.query(Instance).filter(Instance.id == id).first()

    data = get_qrcode64(instance.id, instance.instanceId, instance.token)

    return Response(data, 200, "Instance retrieved successfully.", False)


@router.get("/status")
async def get_status(id: int):

    session = database.get_db_session(engine)

    session = database.get_db_session(engine)
    instance = session.query(Instance).filter(Instance.id == id).first()

    data = status_instance(instance.id, instance.instanceId, instance.token)

    return Response(data, 200, "Instance retrieved successfully.", False)

@router.get("/device")
async def device_info(id: int):

    session = database.get_db_session(engine)

    session = database.get_db_session(engine)
    instance = session.query(Instance).filter(Instance.id == id).first()

    data = get_device_info(instance.instanceId, instance.token)

    return Response(data, 200, "Instance retrieved successfully.", False)


@router.get("/restart")
async def get_restart(id: int):

    session = database.get_db_session(engine)

    session = database.get_db_session(engine)
    instance = session.query(Instance).filter(Instance.id == id).first()

    data = restart(instance.id, instance.instanceId, instance.token)

    return Response(data, 200, "Instance retrieved successfully.", False)


@router.get("/disconect")
async def disconect_whatsapp(id: int):

    session = database.get_db_session(engine)

    session = database.get_db_session(engine)
    instance = session.query(Instance).filter(Instance.id == id).first()

    data = disconect(instance.id, instance.instanceId, instance.token)

    return Response(data, 200, "Instance retrieved successfully.", False)

@router.put("/update-call-reject-auto")
async def update_call_rejec(id: int, value: bool):

    session = database.get_db_session(engine)

    session = database.get_db_session(engine)
    instance = session.query(Instance).filter(Instance.id == id).first()

    data = update_call_reject_auto(instance.id, instance.instanceId, instance.token, value)

    return Response(data, 200, "Instance retrieved successfully.", False)
