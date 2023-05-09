
from typing import List
from celery import shared_task
from typing import Any
from endpoints import Import_grupo


# Tarefa de importar grupos

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5},
             name='universities:get_grupos_task')

def get_grupos_task(self, id: int, getparticipantes: bool) -> Any:
    return Import_grupo.get_grupos(id, getparticipantes)