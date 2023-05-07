from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from sqlalchemy import func
from models.request import ContatosRequest, ContatosCreateRequest, InstanceUpdateRequest, TagUpdateRequest, GroupUpdateRequest
from models.response import Response
from models.models import Contatos
from db.database import Database
import json

router = APIRouter(
    prefix="/contatos",
    tags=["Contatos"],
    responses={404: {"description": "Not found"}},
)

database = Database()
engine = database.get_db_connection()

# Funções acessorias


def get_contato_by_email(session: Session, email: str):
    return session.query(Contatos).filter(Contatos.email == email).first()


def get_contato_by_telefone(session: Session, DDD: str, telefone: str):
    return session.query(Contatos).filter(and_(Contatos.DDD == DDD, Contatos.telefone == telefone)).first()


def create_contato(session: Session, contato: ContatosRequest):
    new_contato = Contatos(**contato.dict())
    session.add(new_contato)
    session.commit()
    session.refresh(new_contato)
    return new_contato


def update_contato(session: Session, contato_id: int, contato_data: ContatosRequest):
    contato = session.query(Contatos).filter(Contatos.id == contato_id).first()
    if not contato:
        raise HTTPException(status_code=404, detail="Contato not found")
    contato_data_dict = contato_data.dict(exclude_unset=True)
    for key, value in contato_data_dict.items():
        setattr(contato, key, value)
    session.commit()
    return contato


def delete_contato(session: Session, contato_id: int):
    contato = session.query(Contatos).filter(Contatos.id == contato_id).first()
    if not contato:
        raise HTTPException(status_code=404, detail="Contato not found")
    session.delete(contato)
    session.commit()
    return contato


# Funções de Upadate de Tags, grupos e Instancias

def update_instances(session: Session, contato_id: int, instances: List[int]):
    contato = session.query(Contatos).filter(Contatos.id == contato_id).first()
    if not contato:
        raise HTTPException(status_code=404, detail="Contato not found")

    for instance_id in instances:
        # Verificar se o instance_id já está no array
        existing_instance = session.query(Contatos).filter(
            Contatos.id == contato_id,
            # Use json.dumps para converter o valor para uma string JSON
            func.json_contains(Contatos.instances,
                               json.dumps(instance_id)) == 1
        ).first()

        if existing_instance:
            raise HTTPException(
                status_code=400, detail=f"Instance ID {instance_id} already exists in the array")

        # Adicionar instance_id ao campo JSON
        new_instances = func.json_array_append(
            Contatos.instances, '$', instance_id)
        session.query(Contatos).filter(Contatos.id == contato_id).update(
            {Contatos.instances: new_instances})

    session.commit()
    return contato


def update_tags(session: Session, contato_id: int, tags: List[str]):
    contato = session.query(Contatos).filter(Contatos.id == contato_id).first()
    if not contato:
        raise HTTPException(status_code=404, detail="Contato not found")

    for tag in tags:
        # Verificar se a tag já está no array
        existing_tag = session.query(Contatos).filter(
            Contatos.id == contato_id,
            func.json_contains(Contatos.tags, json.dumps(tag)) == 1
        ).first()

        if existing_tag:
            raise HTTPException(
                status_code=400, detail=f"Tag '{tag}' already exists in the array")

        # Adicionar tag ao campo JSON
        new_tags = func.json_array_append(Contatos.tags, '$', tag)
        session.query(Contatos).filter(
            Contatos.id == contato_id).update({Contatos.tags: new_tags})

    session.commit()
    return contato


def update_groups(session: Session, contato_id: int, groups: List[str]):
    contato = session.query(Contatos).filter(Contatos.id == contato_id).first()
    if not contato:
        raise HTTPException(status_code=404, detail="Contato not found")

    for group in groups:
        # Verificar se o grupo já está no array
        existing_group = session.query(Contatos).filter(
            Contatos.id == contato_id,
            func.json_contains(Contatos.grupos, json.dumps(group)) == 1
        ).first()

        if existing_group:
            raise HTTPException(
                status_code=400, detail=f"Group '{group}' already exists in the array")

        # Adicionar grupo ao campo JSON
        new_groups = func.json_array_append(Contatos.grupos, '$', group)
        session.query(Contatos).filter(Contatos.id == contato_id).update(
            {Contatos.grupos: new_groups})

    session.commit()
    return contato

# Rotas basicas


@router.get("/list")
async def get_all_contatos():
    session = database.get_db_session(engine)
    data = session.query(Contatos).all()
    return Response(data, 200, "Contatos retrieved successfully.", False)


@router.get("/{contato_id}")
async def get_contato(contato_id: int):
    session = database.get_db_session(engine)
    contato = session.query(Contatos).filter(Contatos.id == contato_id).first()
    if not contato:
        raise HTTPException(status_code=404, detail="Contato not found")
    return Response(contato, 200, "Contato retrieved successfully.", False)


@router.get("/telefone/{DDD}/{telefone}")
async def get_contato_by_telefone_route(DDD: str, telefone: str):
    session = database.get_db_session(engine)
    contato = get_contato_by_telefone(session, DDD, telefone)
    if not contato:
        raise HTTPException(status_code=404, detail="Contato not found")
    return Response(contato, 200, "Contato retrieved successfully.", False)


@router.post("/create")
async def create_contato_route(contato: ContatosCreateRequest):
    session = database.get_db_session(engine)
    if get_contato_by_email(session, contato.email) or get_contato_by_telefone(session, contato.DDD, contato.telefone):
        raise HTTPException(status_code=400, detail="Contato already exists")
    new_contato = create_contato(session, contato)
    return Response(new_contato, 201, "Contato created successfully.", False)


@router.put("/{contato_id}")
async def update_contato_route(contato_id: int, contato_data: ContatosRequest):
    session = database.get_db_session(engine)
    updated_contato = update_contato(session, contato_id, contato_data)
    return Response(updated_contato, 200, "Contato updated successfully.", False)


@router.delete("/{contato_id}")
async def delete_contato_route(contato_id: int):
    session = database.get_db_session(engine)
    deleted_contato = delete_contato(session, contato_id)
    return Response(deleted_contato, 200, "Contato deleted successfully.", False)


# Rotas para atualização de contatos (Grupos, etiquetas, instancias associadas)

@router.put("/{contato_id}/update_instances")
async def update_instances_route(contato_id: int, instance_update: InstanceUpdateRequest):
    session = database.get_db_session(engine)
    updated_contato = update_instances(session, contato_id, [
                                       instance_update.instance_id])  # Enviando uma lista com o inteiro
    return Response(updated_contato, 200, "Instances updated successfully.", False)


@router.put("/{contato_id}/update_tags")
async def update_tags_route(contato_id: int, tag_update: TagUpdateRequest):
    session = database.get_db_session(engine)
    updated_contato = update_tags(session, contato_id, tag_update.tags)
    return Response(updated_contato, 200, "Tags updated successfully.", False)


@router.put("/{contato_id}/update_groups")
async def update_groups_route(contato_id: int, group_update: GroupUpdateRequest):
    session = database.get_db_session(engine)
    updated_contato = update_groups(session, contato_id, group_update.groups)
    return Response(updated_contato, 200, "Groups updated successfully.", False)
