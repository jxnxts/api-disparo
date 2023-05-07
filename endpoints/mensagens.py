from fastapi import APIRouter
from starlette.responses import JSONResponse
from models.request import GruposRequest
from models.response import Response
from models.models import Grupos, Instance
from db.database import Database

from api.zapi import status_instance, get_chats, get_groups
from sqlalchemy import and_, desc

from celery_tasks.tasks import get_grupos_task
from config.celery_utils import get_task_info
import datetime


router = APIRouter(
    prefix="/mensagem",
    tags=["Envio de Mensagens"],
    responses={404: {"description": "Not found"}},
)

database = Database()
engine = database.get_db_connection()


@router.post("/async/{id}")
async def get_grupos_async(id: int, getparticipantes: bool):
    task = get_grupos_task.apply_async(args=[id, getparticipantes])
    return JSONResponse({"task_id": task.id})


# @router.get("/{id}")
def get_grupos(id: int, getparticipantes: bool):

    session = database.get_db_session(engine)
    instance = session.query(Instance).filter(Instance.id == id).first()
    # Verifica o status da conexção com o whats
    instance_status = status_instance(
        instance.id, instance.instanceId, instance.token)
    data = instance_status
    if instance_status.connected == True:
        chats = get_chats(instance.instanceId, instance.token)
        for Message in chats.messages:
            if Message.isGroup == True:
                numberGroup = Message.phone
                grupoData = get_groups(
                    instance.instanceId, instance.token, numberGroup, getparticipantes)
                # Verifica se o número de grupo já existe no banco de dados
                grupo_existente = session.query(Grupos).filter(
                    Grupos.number_group == numberGroup).first()
                # Se o grupo não existe no banco de dados, adicionamos um novo registro
                if not grupo_existente:
                    creationDate = datetime.datetime.fromtimestamp(
                        grupoData.creation / 1000.0)
                    new_grupo = Grupos(
                        number_group=numberGroup,
                        nome=grupoData.subject,
                        instance=instance.instanceId,
                        admin=grupoData.owner,
                        ativo=True,
                        invitationLink=grupoData.invitationLink,
                        communityId=grupoData.communityId,
                        creation=creationDate
                    )
                    session.add(new_grupo)
                    session.commit()

        return Response(None, 200, "Grupos Coletados.", False)
    return Response(None, 400, f"{instance_status.error}.", True)
