from fastapi import APIRouter
from models.request import InstanceRequest
from models.response import Response
from models.models import Instance
from db.database import Database
from sqlalchemy import and_, desc

# APIRouter creates path operations for product module
router = APIRouter(
    prefix="/instance",
    tags=["Instance"],
    responses={404: {"description": "Not found"}},
)

database = Database()
engine = database.get_db_connection()


@router.get("/list")
async def get_Instance():
    session = database.get_db_session(engine)

    data = session.query(Instance).all()

    return Response(data, 200, "Instance retrieved successfully.", False)


@router.get("/{id}")
async def get_Instance_by_id(id: int):
    session = database.get_db_session(engine)

    data = session.query(Instance).filter(Instance.id == id).first()

    if data:
        return Response(data, 200, "Instance retrieved successfully.", False)
    else:
        return Response(None, 404, "Instance not found.", True)


@router.get("/instance/{instanceId}")
async def get_Instance_by_instanceId(instanceId: str):
    session = database.get_db_session(engine)

    data = session.query(Instance).filter(
        Instance.instanceId == instanceId).first()

    if data:
        return Response(data, 200, "Instance retrieved successfully.", False)
    else:
        return Response(None, 404, "Instance not found.", True)


@router.post("/create")
async def create_Instance(instance: InstanceRequest):
    session = database.get_db_session(engine)

    new_instance = Instance(
        instanceId=instance.instanceId,
        token=instance.token,
        nome=instance.nome,
        tipo_instance=instance.tipo_instance,
        numero=instance.numero
    )

    session.add(new_instance)
    session.commit()

    return Response(new_instance, 201, "Instance created successfully.", False)


@router.put("/update/{instanceId}")
async def update_Instance(instanceId: str, instance: InstanceRequest):
    session = database.get_db_session(engine)

    data = session.query(Instance).filter(
        Instance.instanceId == instanceId).first()

    if data:
        data.instanceId = instance.instanceId or data.instanceId
        data.token = instance.token or data.token
        data.nome = instance.nome or data.nome
        data.tipo_instance = instance.tipo_instance or data.tipo_instance
        data.numero = instance.numero or data.numero

        session.commit()

        return Response(data, 200, "Instance updated successfully.", False)
    else:
        return Response(None, 404, "Instance not found.", True)


@router.delete("/delete/{instanceId}")
async def delete_Instance(instanceId: str):
    session = database.get_db_session(engine)

    data = session.query(Instance).filter(
        Instance.instanceId == instanceId).first()

    if data:
        session.delete(data)
        session.commit()

        return Response(None, 200, "Instance deleted successfully.", False)
    else:
        return Response(None, 404, "Instance not found.", True)
