FROM python:3.11

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip3 install --no-cache-dir --upgrade -r /app/requirements.txt

# RUN wget https://letsencrypt.org/certs/lets-encrypt-r3.pem -O /usr/local/share/ca-certificates/lets-encrypt-r3.crt

# RUN update-ca-certificates

CMD ["uvicorn","main:app","--host","0.0.0.0","--port","80"]
