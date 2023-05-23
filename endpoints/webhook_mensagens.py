from fastapi import APIRouter, Request
from typing import Optional
import json
from models.request import InstanceRequest
from models.response import Response
from models.models import Instance
from db.database import Database
from db.nosql import NoSQLDatabase
from db.elastic import ElasticsearchDatabase
from sqlalchemy import and_, desc
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()

# APIRouter
router = APIRouter(
    prefix="/webhook-m",
    tags=["webhook"],
    responses={404: {"description": "Not found"}},
)

# Initialize Elasticsearch Database
es_db = ElasticsearchDatabase()
es_client = es_db.get_es_connection()

ELASTICSEARCH_INDEX = os.getenv('ELASTICSEARCH_INDEX', 'webhook_data')
            
            
def save_to_elasticsearch(json_data: dict):
    try:
        result = es_client.index(index=ELASTICSEARCH_INDEX, body=json_data)
        return result['_id']
    except Exception as e:
        print(f"Error saving data to Elasticsearch: {e}")
        return None

@router.post("/mensagens")
async def webhook(request: Request):
    json_data = await request.json()

    # Save JSON data to Elasticsearch
    es_result = save_to_elasticsearch(json_data)
    if es_result is not None:
        print(f"Data saved to Elasticsearch with ID: {es_result}")
        return JSONResponse(content={"success": True, "message": "Data saved to Elasticsearch successfully.", "id": str(es_result)}, status_code=201)
    else:
        print("Error saving data to Elasticsearch.")
        return JSONResponse(content={"success": False, "message": "Error saving data to Elasticsearch."}, status_code=500)