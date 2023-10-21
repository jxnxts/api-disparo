from fastapi import APIRouter, Request
from typing import Optional
import json
from models.request import InstanceRequest
from models.response import Response
from models.models import Instance
from db.database import Database
from db.nosql import NoSQLDatabase
from sqlalchemy import and_, desc
from fastapi.responses import JSONResponse
from api.compreFace import recognition, subjects, face_collection, _recognitionImage
from api.openai import transcribe_audio
from celery_tasks.webhook import process_webhook_task
from config.celery_utils import get_task_info



# APIRouter
router = APIRouter(
    prefix="/webhook",
    tags=["webhook"],
    responses={404: {"description": "Not found"}},
)

# Initialize NoSQL Database
nosql_db = NoSQLDatabase()
mongo_client = nosql_db.get_mongo_connection()
mongo_db = nosql_db.get_mongo_db(mongo_client)


def save_to_mongo_mesage(json_data: dict):
    try:
        collection = mongo_db["webhook_data"]
        result = collection.insert_one(json_data)
        return result.inserted_id
    except Exception as e:
        print(f"Error saving data to MongoDB: {e}")
        return None   


@router.post("/mensagens")
async def webhookEnpoint(request: Request):
    json_data = await request.json()
    task = process_webhook_task.apply_async(args=[json_data])
    return JSONResponse({"task_id": task.id})


def webhook(json_data):

    if json_data.get("image"):
        try:
             print("Processando a imagem")
             json_data = imageProcess(json_data)
             print(json_data)
        except:
             pass
    # # elif json_data.get("video"):
    # #     videoProcess(json_data)
    # # elif json_data.get("audio"):
    # #     audioProcess(json_data)
    # # elif json_data.get("poll"):
    # #     pollProcess(json_data)
    # # elif json_data.get("link"):
    # #     linkProcess(json_data)
    # else:
    #     pass:

    # Save JSON data to MongoDB
    mongo_result = save_to_mongo_mesage(json_data)
    if mongo_result is not None:
        print(f"Data saved to MongoDB with ID: {mongo_result}")
        return JSONResponse(content={"success": True, "message": "Data saved to MongoDB successfully.", "id": str(mongo_result)}, status_code=201)
    else:
        print("Error saving data to MongoDB.")
        return JSONResponse(content={"success": False, "message": "Error saving data to MongoDB."}, status_code=500)



def imageProcess(json_data):
    data = _recognitionImage(json_data["image"]["imageUrl"])
    print(data)  # Chamada à função de reconhecimento de imagem

    if "result" in data and data["result"]:
        print(data)
        filtered_subjects = filterSubjects(data)  # Filtra os subjects com similarity acima de 0.8
        json_data["image"]["subjects"] = filtered_subjects  # Adiciona o resultado filtrado ao json_data

    return json_data

def filterSubjects(data):
    filtered_subjects = []
    for result in data["result"]:
        for subject in result["subjects"]:
            if subject["similarity"] > 0.8:
                filtered_subjects.append(subject)
    return filtered_subjects
   

def videoProcess(json_data):
    pass

def audioProcess(json_data):
    pass

def pollProcess(json_data):
    pass

def linkProcess(json_data):
    pass


