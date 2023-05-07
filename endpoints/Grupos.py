from fastapi import APIRouter
from models.request import GruposRequest, CreateGroup
from models.response import Response
from typing import Optional, List
from models.models import Grupos, Instance
from db.database import Database
from sqlalchemy import and_, desc
from api.zapi import status_instance, get_chats, get_groups, get_qrcode64, disconect, restart, update_call_reject_auto, get_device_info, create_group
import datetime

# APIRouter cria operações de caminho para o módulo de grupos
router = APIRouter(
    prefix="/grupos",
    tags=["Grupos"],
    responses={404: {"description": "Not found"}},
)

database = Database()
engine = database.get_db_connection()


@router.get("/list")
async def get_grupos():
    session = database.get_db_session(engine)

    data = session.query(Grupos).all()

    return Response(data, 200, "Grupos recuperados com sucesso.", False)


@router.get("/{id}")
async def get_grupo_by_id(id: int):
    session = database.get_db_session(engine)

    data = session.query(Grupos).filter(Grupos.id == id).first()

    if data:
        return Response(data, 200, "Grupo recuperado com sucesso.", False)
    else:
        return Response(None, 404, "Grupo não encontrado.", True)


# Atualizar nome do grupo

# Atualizar imagem do grupo

# Adicionar Participantes

# Remover Participantes

# Promover admin do grupo

# Sair do grupo

# Metadata do Grupo : Semi implementado

# Metadata do Grupo por Convite : IMPORTANTE

# Configurações do grupo: Deve vir em seguida ao create grupo

# Alterar descrição

@router.post("/create")
async def create_grupo(id: int, tema: Optional[str], cidade: Optional[str],  grupo: CreateGroup):



    session = database.get_db_session(engine)
    instance = session.query(Instance).filter(Instance.id == id).first()

    group = create_group(instance.instanceId, instance.token, grupo)

    print(group)

    new_grupo = Grupos(
        number_group=group.phone,
        nome=grupo.groupName,
        instance=instance.instanceId,
        invitationLink= group.invitationLink,
        # admin= ,
        ativo= True,
        cidade=cidade,
        tema= tema,
        creation = datetime.datetime.now()
    )

    session.add(new_grupo)
    session.commit()

    return Response(group, 201, "Grupo criado com sucesso.", False)





@router.put("/update/{id}")
async def update_grupo(id: int, grupo: GruposRequest):
    session = database.get_db_session(engine)

    data = session.query(Grupos).filter(Grupos.id == id).first()

    if data:
        data.number_group = grupo.number_group or data.number_group
        data.nome = grupo.nome or data.nome
        data.instance = grupo.instance or data.instance
        data.admin = grupo.admin or data.admin
        data.ativo = grupo.ativo or data.ativo
        data.cidade = grupo.cidade or data.cidade
        data.tema = grupo.tema or data.tema

        session.commit()

        return Response(data, 200, "Grupo atualizado com sucesso.", False)
    else:
        return Response(None, 404, "Grupo não encontrado.", True)


@router.delete("/delete/{id}")
async def delete_grupo(id: int):
    session = database.get_db_session(engine)

    data = session.query(Grupos).filter(Grupos.id == id).first()

    if data:
        session.delete(data)
        session.commit()

        return Response(None, 200, "Grupo excluído com sucesso.", False)
    else:
        return Response(None, 404, "Grupo não encontrado.", True)
