from typing import List, Any
from celery import shared_task
from endpoints import webhook


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 3},
             name='universities:webhook_task')
def process_webhook_task(self, json_data: dict) -> Any:
    webhook.webhook(json_data)


