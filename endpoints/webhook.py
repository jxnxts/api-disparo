from fastapi import APIRouter, Request
from typing import Optional
import json
from models.request import InstanceRequest
from models.response import Response
from models.models import Instance
from db.database import Database
from sqlalchemy import and_, desc

# APIRouter
router = APIRouter(
    prefix="/webhook",
    tags=["webhook"],
    responses={404: {"description": "Not found"}},
)

database = Database()
engine = database.get_db_connection()


def text(json_data: dict = None):
    if not isinstance(json_data, dict):
        return
    print("Processing text message:", json_data.get("messageId"))


def video(json_data: dict = None):
    if not isinstance(json_data, dict):
        return
    print("Processing video message:", json_data)


def image(json_data: dict = None):
    if not isinstance(json_data, dict):
        return
    print("Processing image message:", json_data)


def audio(json_data: dict = None):
    if not isinstance(json_data, dict):
        return
    print("Processing audio message:", json_data)


def contact(json_data: dict = None):
    if not isinstance(json_data, dict):
        return
    print("Processing contact message:", json_data)


def document(json_data: dict = None):
    if not isinstance(json_data, dict):
        return
    print("Processing document message:", json_data)


def location(json_data: dict = None):
    if not isinstance(json_data, dict):
        return
    print("Processing location message:", json_data)


def sticker(json_data: dict = None):
    if not isinstance(json_data, dict):
        return
    print("Processing sticker message:", json_data)


def poll(json_data: dict = None):
    if not isinstance(json_data, dict):
        return
    print("Processing poll message:", json_data)


def pollVote(json_data: dict = None):
    if not isinstance(json_data, dict):
        return
    print("Processing pollVote message:", json_data)


types = ['text', 'video', 'image', 'audio', 'contact',
         'document', 'location', 'sticker', 'poll', 'pollVote']


@router.post("/mensagens")
async def webhook(request: Request):
    json_data = await request.json()

    message_type = next((t for t in types if t in json_data), None)

    if message_type:
        func = globals().get(message_type)
        if func:
            func(json_data)
            response_data = message_type
            status_code = 200
            message = "Webhook retrieved successfully."
        else:
            response_data = None
            status_code = 400
            message = "Invalid message type."
    else:
        response_data = None
        status_code = 400
        message = "Invalid message type."

    return Response(response_data, status_code, message, False)
