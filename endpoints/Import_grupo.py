from fastapi import APIRouter
from starlette.responses import JSONResponse
from models.request import GruposRequest
from models.response import Response
from models.models import Grupos, Instance
from db.database import Database
from api.zapi import status_instance, get_chats, get_groups, save_contacts
from sqlalchemy import and_, desc
from celery_tasks.tasks import get_grupos_task, get_chats_task, get_groups_task
from config.celery_utils import get_task_info
from celery.result import AsyncResult
import datetime
import time

router = APIRouter(
    prefix="/import-grupos",
    tags=["Importar Grupos"],
    responses={404: {"description": "Not found"}},
)

database = Database()
engine = database.get_db_connection()


@router.post("/async/{id}")
async def get_grupos_async(id: int, getparticipantes: bool):
    task = get_grupos_task.apply_async(args=[id, getparticipantes])
    return JSONResponse({"task_id": task.id})


def get_grupos(id: int, getparticipantes: bool):
    session = database.get_db_session(engine)

    #Filtro da Instanca
    instance = session.query(Instance).filter(Instance.id == id).first()

    # Verificação de Status da Linha (Instancia)
    instance_status = status_instance(
        instance.id, instance.instanceId, instance.token)

    if instance_status.connected == True:
        chats_task = get_chats_task.apply_async(
            args=[instance.instanceId, instance.token])

        # Aguarde a tarefa ser concluída
        chats_task_result = AsyncResult(chats_task.id)
        while not chats_task_result.ready():
            time.sleep(1)

        chats = chats_task_result.result

        for messages in chats:
            if messages.isGroup == True:

                numberGroup = messages.phone

                grupo_task = get_groups_task.apply_async(
                    args=[instance.instanceId, instance.token, numberGroup, getparticipantes])

                # Aguarde a tarefa ser concluída
                grupo_task_result = AsyncResult(grupo_task.id)
                while not grupo_task_result.ready():
                    time.sleep(1)

                grupoData = grupo_task_result.result

                grupo_existente = session.query(Grupos).filter(
                    Grupos.number_group == numberGroup).first()

                if not grupo_existente:
                    try:
                        new_grupo = Grupos(
                            number_group=numberGroup,
                            nome=grupoData.subject,
                            instance=instance.instanceId,
                            admin=grupoData.owner,
                            ativo=True,
                            invitationLink=grupoData.invitationLink,
                            communityId=grupoData.communityId,
                            creation=grupoData.creation
                        )
                        session.add(new_grupo)
                        session.commit()
                    except Exception as e:
                        return Response(None, 500, f"Erro inesperado: {str(e)}", True)

        return Response(None, 200, "Grupos Coletados.", False)
    return Response(None, 400, f"{instance_status.error}.", True)


# @router.post("/groups/{grupo_id}/participants")
# def import_group_participants(grupoId: str):
#     with database.get_db_session(engine) as session:
#         grupo = session.query(Grupos).filter(Grupos.number_group == grupoId).first()
#         instance = session.query(Instance).filter(Instance.instanceId == grupo.instance).first()

#         metada = get_groups(instance.instanceId, instance.token, grupoId, False)
#         print(metada)

#         for participant in metada.participants:
#             print(participant)
#             save_contacts(participant, grupo.number_group)

#     return Response(None, 200, "Participantes do grupo importados com sucesso.", False)


# def get_grupos_by_instanceId(id: int):
#     with database.get_db_session(engine) as session:
#         instance = session.query(Instance).filter(Instance.id == id).first()
#         grupos = session.query(Grupos).filter(Grupos.instance == instance.instanceId).all()

#     for grupo in grupos:
#         try:
#             print(grupo.number_group)
#             import_group_participants(grupo.number_group)
#         except Exception as e:
#             print(f"Error importing group participants: {e}")
#             continue