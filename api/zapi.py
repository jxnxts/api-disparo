from models.responses.model_zapi import InstanceStatus, Message, MessageList, GroupMetadata, Participant, QrCodeReturn, DisconectReturn, RestartReturn, CallRejectReturn, DeviceReturn, CreateGroupReturn, ReturnEnvioImagem
from db.database import Database
from models.models import Grupos, Instance, Contatos
from models.response import Response
from models.request import MensagemImagemRequest
from sqlalchemy import and_, desc
from typing import List
import requests
import json


database = Database()
engine = database.get_db_connection()


def send_image(instanceId: str, token: str, link: str, legenda: str, phone: str, delay: int ):
    url = f"https://api.z-api.io/instances/{instanceId}/token/{token}/send-image"
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/json"
    }
      
    body = MensagemImagemRequest(phone=phone, image=link, caption=legenda, delayMessage=delay)


    # json_data = json.dumps(body.dict())
    json_data = body.dict()

    response = requests.post(url, headers=headers, json=json_data)

    if response.status_code == 200:
        data = response.json()
        returnSendImagem = ReturnEnvioImagem(**data)

        return returnSendImagem

    else:
        
        return None
    









def create_group(instanceId: str, token: str, grupo) -> CreateGroupReturn:
    url = f"https://api.z-api.io/instances/{instanceId}/token/{token}/create-group"
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/json"
    }

    json_data = grupo.dict()

    print(json_data)

    response = requests.post(url, headers=headers, json=json_data)

    if response.status_code == 200:
        data = response.json()
        creatgroup = CreateGroupReturn(**data)

        return creatgroup

    else:
        return None


def get_device_info(instanceId: str, token: str) -> DeviceReturn:
    url = f"https://api.z-api.io/instances/{instanceId}/token/{token}/device"
    headers = {
        "Accept": "*/*"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        device_info = DeviceReturn(**data)

        return device_info

    else:
        return None


def update_call_reject_auto(id: str, instanceId: str, token: str, value: bool) -> CallRejectReturn:
    url = f"https://api.z-api.io/instances/{instanceId}/token/{token}/update-call-reject-auto"
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/json"
    }
    bodyResquest = {"value": value}
    json_data = json.dumps(bodyResquest)

    response = requests.put(url, headers=headers, json=json_data)

    if response.status_code == 200:
        data = response.json()
        call_reject = CallRejectReturn(**data)

        return call_reject

    else:
        return None


def disconect(id: str, instanceId: str, token: str) -> DisconectReturn:

    url = f"https://api.z-api.io/instances/{instanceId}/token/{token}/disconnect"
    headers = {
        "Accept": "*/*"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        disconected = DisconectReturn(**data)

        return disconected

    else:
        return None


def restart(id: str, instanceId: str, token: str) -> RestartReturn:

    url = f"https://api.z-api.io/instances/{instanceId}/token/{token}/restart"
    headers = {
        "Accept": "*/*"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        restart = RestartReturn(**data)

        return restart

    else:
        return None


def get_qrcode64(id: str, instanceId: str, token: str) -> QrCodeReturn:
    url = f"https://api.z-api.io/instances/{instanceId}/token/{token}/qr-code/image"
    headers = {
        "Accept": "*/*"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        getqrcode64 = QrCodeReturn(**data)

        return getqrcode64

    else:
        return None


def status_instance(id: str, instanceId: str, token: str) -> InstanceStatus:
    url = f"https://api.z-api.io/instances/{instanceId}/token/{token}/status"
    headers = {
        "Accept": "*/*"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        instance_status = InstanceStatus(**data)

        return instance_status

    else:
        return None


def get_chats(instanceId: str, token: str) -> MessageList:
    url = f"https://api.z-api.io/instances/{instanceId}/token/{token}/chats"
    headers = {
        "Accept": "*/*"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        messages = [Message(**message_data) for message_data in data]
        return MessageList(messages=messages)
    else:
        return None


def get_groups(instanceId: str, token: str, group_id: str, getparticipantes: bool) -> GroupMetadata:

    url = f"https://api.z-api.io/instances/{instanceId}/token/{token}/group-metadata/{group_id}"
    headers = {
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        grupoData = GroupMetadata(**data)

        if getparticipantes == True:

            for participant in grupoData.participants:
                save_contacts(participant.phone, grupoData)

    return grupoData


def save_contacts(participant, grupoData: GroupMetadata):

    session = database.get_db_session(engine)

    contact = session.query(Contatos).filter_by(telefone=participant).first()

    if contact:
        grupos = contact.grupos or []
        grupos.append(grupoData.phone)
        contact.grupos = grupos
    else:
        new_contact = Contatos(
            telefone=participant,
            grupos=[grupoData.phone]
        )
        session.add(new_contact)
    session.commit()
