from typing import List, Any
from celery import shared_task
from endpoints import Import_grupo


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 2},
             name='universities:get_grupos_task')
def get_grupos_task(self, id: int, getparticipantes: bool) -> Any:
    return Import_grupo.get_grupos(id, getparticipantes)


# @shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5},
#              name='universities:get_instance_task')
# def get_instance_task(self, id: int) -> Any:
#     return Import_grupo.get_instance(id)


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 2},
             name='universities:get_chats_task')
def get_chats_task(self, instanceId: str, token: str) -> Any:
    return Import_grupo.get_chats(instanceId, token)


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5},
             name='universities:get_group_data_task')
def get_groups_task(self,  instanceId: str, token: str, numberGroup: str, getparticipantes: bool) -> Any:
    return Import_grupo.get_groups(instanceId, token, numberGroup, getparticipantes)
