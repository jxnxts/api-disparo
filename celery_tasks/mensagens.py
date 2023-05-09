
from typing import List
from celery import shared_task
from typing import Any
from endpoints import mensagens
from models.request import MensagemImagemRequest



# Tarefas de mensagens

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5},
             name='universities:send_image_task')

def send_image_task(self, id: int, image: MensagemImagemRequest) -> Any:
    return mensagens.enviar_imagem(id, image)
