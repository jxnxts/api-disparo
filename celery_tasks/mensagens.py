
from typing import List
from celery import shared_task
from typing import Any
from endpoints import mensagens
from models.request import (
    MensagemImagemRequest,
    MensagemImagemRequestGrupo,
    MensagemVideoRequest,
    MensagemVideoRequestGrupo,
    MensagemAudioRequest,
    MensagemAudioRequestGrupo,
)


# Tarefas de mensagens

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5},
             name='universities:send_image_task')
def send_image_task(self, id: int, image: MensagemImagemRequest) -> Any:
    return mensagens.enviar_imagem(id, image)


# ...

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5},
             name='universities:send_image_grupos_task')
def send_image_grupos_task(self, id: int, image: MensagemImagemRequestGrupo) -> Any:
    return mensagens.enviar_image_grupos(id, image)


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5},
             name='universities:send_video_task')
def send_video_task(self, id: int, video: MensagemVideoRequest) -> Any:
    return mensagens.enviar_video(id, video)


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5},
             name='universities:send_video_grupos_task')
def send_video_grupos_task(self, id: int, video: MensagemVideoRequestGrupo) -> Any:
    return mensagens.enviar_video_grupos(id, video)


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5},
             name='universities:send_audio_task')
def send_audio_task(self, id: int, audio: MensagemAudioRequest) -> Any:
    return mensagens.enviar_audio(id, audio)


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5},
             name='universities:send_audio_grupos_task')
def send_audio_grupos_task(self, id: int, audio: MensagemAudioRequestGrupo) -> Any:
    return mensagens.enviar_audio_grupos(id, audio)
