import os
from functools import lru_cache
from dotenv import load_dotenv
from kombu import Queue

load_dotenv()


CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')

def route_task(name, args, kwargs, options, task=None, **kw):
    if ":" in name:
        queue, _ = name.split(":")
        return {"queue": queue}
    return {"queue": "celery"}


class BaseConfig:
    CELERY_BROKER_URL: CELERY_BROKER_URL
    CELERY_RESULT_BACKEND: CELERY_RESULT_BACKEND

    CELERY_TASK_QUEUES: list = (
        # default queue
        Queue("celery"),


        # CRIAR FILAS MENSAGENS IN GROUP
        # CRIAR FILA MENSAGENS IN CONTATOS
        # PEGAR GRUPOS
        # PEGAR CONTATOS
        
        Queue("universities"),
        Queue("university"),
    )

    CELERY_TASK_ROUTES = (route_task,)


class DevelopmentConfig(BaseConfig):
    pass


@lru_cache()
def get_settings():
    config_cls_dict = {
        "development": DevelopmentConfig,
    }
    config_name = os.environ.get("CELERY_CONFIG", "development")
    config_cls = config_cls_dict[config_name]
    return config_cls()


settings = get_settings()