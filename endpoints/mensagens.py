from fastapi import APIRouter
from starlette.responses import JSONResponse
from models.request import GruposRequest, MensagemImagemRequestGrupo, MensagemImagemRequest, MensagemAudioRequest, MensagemAudioRequestGrupo, MensagemVideoRequest, MensagemVideoRequestGrupo, MensagemTextRequest, MensagemLinkRequest, MensagemTextRequestGrupo, MensagemLinkRequestGrupo
from models.response import Response
from models.models import Grupos, Instance
from db.database import Database

from api.zapi import status_instance, get_chats, get_groups, send_image, send_video, send_audio, send_text, send_link
from sqlalchemy import and_, desc
from celery_tasks.mensagens import (
    send_text_task,
    send_text_grupos_task,
    send_image_task,
    send_image_grupos_task,
    send_video_task,
    send_video_grupos_task,
    send_audio_task,
    send_audio_grupos_task,
    send_link_task,
    send_link_grupos_task
)
from config.celery_utils import get_task_info
# import datetime


router = APIRouter(
    prefix="/mensagem",
    tags=["Envio de Mensagens"],
    responses={404: {"description": "Not found"}},
)

database = Database()
engine = database.get_db_connection()




@router.post("/text/{id}")
async def enviar_text_async(id: int, text: MensagemTextRequest):
    task = send_text_task.apply_async(args=[id, text])
    return JSONResponse({"task_id": task.id})

def enviar_text(id: int, text: MensagemTextRequest):
    session = database.get_db_session(engine)
    instance = session.query(Instance).filter(Instance.id == id).first()

    # Verifica o status da conexção com o whats
    instance_status = status_instance(
        instance.id, instance.instanceId, instance.token)
    if instance_status.connected == True:

        
        phone = text.phone
        message = text.message
        delay = text.delayMessage

        mensagem = send_text(instance.instanceId,
                              instance.token, message, phone, delay)

        return Response(mensagem, 200, "sucess.", False)
    return Response(None, 400, f"{instance_status.error}.", True)


@router.post("/text_grupos/{id}")
async def enviar_text_grupos_async(id: int, text: MensagemTextRequestGrupo):
    task = send_text_grupos_task.apply_async(args=[id, text])
    return JSONResponse({"task_id": task.id})
def enviar_text_grupos(id: int, text: MensagemTextRequestGrupo):

    session = database.get_db_session(engine)
    instance = session.query(Instance).filter(Instance.id == id).first()

    # Verifica o status da conexção com o whats
    instance_status = status_instance(
        instance.id, instance.instanceId, instance.token)
    if instance_status.connected == True:

        phones = session.query(Grupos).filter(
            Grupos.instance == instance.instanceId).all()

        for number_group in phones:

            message = text.message
            phone = number_group.number_group
            delay = 5

            send_text(instance.instanceId, instance.token,
                       message, phone, delay)

        return Response(None, 200, "sucess.", False)
    return Response(None, 400, f"{instance_status.error}.", True)



# Link


@router.post("/link/{id}")
async def enviar_link(id: int, link: MensagemLinkRequest):
    task = send_link_task.apply_async(args=[id, link])
    return JSONResponse({"task_id": task.id})
def enviar_link(id: int, link: MensagemLinkRequest):
    session = database.get_db_session(engine)
    instance = session.query(Instance).filter(Instance.id == id).first()

    # Verifica o status da conexção com o whats
    instance_status = status_instance(
        instance.id, instance.instanceId, instance.token)
    if instance_status.connected == True:

        # print(link.dict())
        
        message = link.message
        image = link.image
        linkUrl = link.linkUrl
        title = link.title
        linkDescription = link.linkDescription
        phone = link.phone
        delay = link.delayMessage
        linkType = link.linkType

        mensagem = send_link(instance.instanceId,
                              instance.token, message,phone, image,  linkUrl, title, linkDescription, linkType, delay)

        return Response(mensagem, 200, "sucess.", False)
    return Response(None, 400, f"{instance_status.error}.", True)

@router.post("/link_grupos/{id}")
async def enviar_link_grupos_async(id: int, link: MensagemLinkRequestGrupo):
    task = send_link_grupos_task.apply_async(args=[id, link])
    return JSONResponse({"task_id": task.id})
def enviar_link_grupos(id: int, link: MensagemLinkRequestGrupo):

    session = database.get_db_session(engine)
    instance = session.query(Instance).filter(Instance.id == id).first()

    # Verifica o status da conexção com o whats
    instance_status = status_instance(
        instance.id, instance.instanceId, instance.token)
    if instance_status.connected == True:

        phones = session.query(Grupos).filter(
            Grupos.instance == instance.instanceId).all()

        for number_group in phones:

          
            phone = number_group.number_group
            message = link.message
            image = link.image
            linkUrl = link.linkUrl
            title = link.title
            linkDescription = link.linkDescription
            delay = link.delayMessage
            linkType = link.linkType
            

            mensagem = send_link(instance.instanceId,
                              instance.token, message,phone, image,  linkUrl, title, linkDescription, linkType, delay)

        return Response(mensagem, 200, "sucess.", False)
    return Response(None, 400, f"{instance_status.error}.", True)



@router.post("/image/{id}")
async def enviar_image_async(id: int, image: MensagemImagemRequest):
    task = send_image_task.apply_async(args=[id, image])
    return JSONResponse({"task_id": task.id})



def enviar_imagem(id: int, image: MensagemImagemRequest):
    session = database.get_db_session(engine)
    instance = session.query(Instance).filter(Instance.id == id).first()

    # Verifica o status da conexção com o whats
    instance_status = status_instance(
        instance.id, instance.instanceId, instance.token)
    if instance_status.connected == True:

        url = image.image
        legenda = image.caption
        phone = image.phone
        delay = image.delayMessage

        mensagem = send_image(instance.instanceId,
                              instance.token, url, legenda, phone, delay)

        return Response(mensagem, 200, "sucess.", False)
    return Response(None, 400, f"{instance_status.error}.", True)


@router.post("/image_grupos/{id}")
async def enviar_image_grupos(id: int, image: MensagemImagemRequestGrupo):
    task = send_image_grupos_task.apply_async(args=[id, image])
    return JSONResponse({"task_id": task.id})


def enviar_image_grupos_func(id: int, image: MensagemImagemRequestGrupo):

    session = database.get_db_session(engine)
    instance = session.query(Instance).filter(Instance.id == id).first()

    # Verifica o status da conexção com o whats
    instance_status = status_instance(
        instance.id, instance.instanceId, instance.token)
    if instance_status.connected == True:

        phones = session.query(Grupos).filter(
            Grupos.instance == instance.instanceId).all()

        for number_group in phones:

            url = image.imagem
            legenda = image.caption
            phone = number_group.number_group
            delay = 5

            send_image(instance.instanceId, instance.token,
                       url, legenda, phone, delay)

        return Response(None, 200, "sucess.", False)
    return Response(None, 400, f"{instance_status.error}.", True)


@router.post("/video/{id}")
async def enviar_video(id: int, video: MensagemVideoRequest):
    task = send_video_task.apply_async(args=[id, video])
    return JSONResponse({"task_id": task.id})


def enviar_video(id: int, video: MensagemVideoRequest):
    session = database.get_db_session(engine)
    instance = session.query(Instance).filter(Instance.id == id).first()

    # Verifica o status da conexção com o whats
    instance_status = status_instance(
        instance.id, instance.instanceId, instance.token)
    if instance_status.connected == True:

        url = video.video
        legenda = video.caption
        phone = video.phone
        delay = video.delayMessage

        mensagem = send_video(instance.instanceId,
                              instance.token, url, legenda, phone, delay)

        return Response(mensagem, 200, "sucess.", False)
    return Response(None, 400, f"{instance_status.error}.", True)


@router.post("/video_grupos/{id}")
async def enviar_video_grupos(id: int, video: MensagemVideoRequestGrupo):
    task = send_video_grupos_task.apply_async(args=[id, video])
    return JSONResponse({"task_id": task.id})


def enviar_video_grupos_func(id: int, video: MensagemVideoRequestGrupo):
    session = database.get_db_session(engine)
    instance = session.query(Instance).filter(Instance.id == id).first()

    # Verifica o status da conexção com o whats
    instance_status = status_instance(
        instance.id, instance.instanceId, instance.token)
    if instance_status.connected == True:

        phones = session.query(Grupos).filter(
            Grupos.instance == Instance.instanceId).all()

        for number_group in phones:

            url = video.video
            legenda = video.caption
            phone = number_group.number_group
            delay = 5

            send_video(instance.instanceId, instance.token,
                       url, legenda, phone, delay)

        return Response(None, 200, "sucess.", False)
    return Response(None, 400, f"{instance_status.error}.", True)


@router.post("/audio/{id}")
async def enviar_audio(id: int, audio: MensagemAudioRequest):
    task = send_audio_task.apply_async(args=[id, audio])
    return JSONResponse({"task_id": task.id})


def enviar_audio(id: int, audio: MensagemAudioRequest):
    session = database.get_db_session(engine)
    instance = session.query(Instance).filter(Instance.id == id).first()

    # Verifica o status da conexção com o whats
    instance_status = status_instance(
        instance.id, instance.instanceId, instance.token)
    if instance_status.connected == True:

        url = audio.audio
        phone = audio.phone
        delay = audio.delayMessage
        delayGravando = audio.delayTyping

        mensagem = send_audio(instance.instanceId,
                              instance.token, url, phone, delay, delayGravando)

        return Response(mensagem, 200, "sucess.", False)

    return Response(None, 400, f"{instance_status.error}.", True)


@router.post("/audio_grupos/{id}")
async def enviar_audio_grupos(id: int, audio: MensagemAudioRequestGrupo):
    task = send_audio_grupos_task.apply_async(args=[id, audio])
    return JSONResponse({"task_id": task.id})


def enviar_audio_grupos(id: int, audio: MensagemAudioRequestGrupo):
    session = database.get_db_session(engine)
    instance = session.query(Instance).filter(Instance.id == id).first()

    # Verifica o status da conexção com o whats
    instance_status = status_instance(
        instance.id, instance.instanceId, instance.token)
    if instance_status.connected == True:

        phones = session.query(Grupos).filter(
            Grupos.instance == Instance.instanceId).all()

        for number_group in phones:

            url = audio.audio
            phone = number_group.number_group
            delay = 5
            delayGravando = audio.delayTyping

            send_audio(instance.instanceId, instance.token,
                       url, phone, delay, delayGravando)

        return Response(None, 200, "sucess.", False)
    return Response(None, 400, f"{instance_status.error}.", True)
