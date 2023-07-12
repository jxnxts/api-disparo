# Api de WhatX


ativar virtualenv

source env/bin/activate



# ATIVAR WORKER

celery -A main.celery worker --loglevel=info -Q universities,university

# MONITOR TAKS:

celery -A main.celery flower --port=5555


# CRIAR MAQUINA DOCKER RABIMT

docker run --rm -it -p 15672:15672 -p 5672:5672 rabbitmq:3-management


https://www.architect.io/blog/2021-01-19/rabbitmq-docker-tutorial/



# UTEIS

https://medium.com/cuddle-ai/async-architecture-with-fastapi-celery-and-rabbitmq-c7d029030377




docker-compose -f docker-compose.dev.yml build


docker-compose -f docker-compose.dev.yml up


