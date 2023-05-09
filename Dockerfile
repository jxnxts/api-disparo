FROM python:3.11

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip3 install --no-cache-dir --upgrade -r /app/requirements.txt

CMD ["uvicorn","main:app","--host","0.0.0.0","--port","80"]

