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


# APIRouter
router = APIRouter(
    prefix="/webhook",
    tags=["webhook"],
    responses={404: {"description": "Not found"}},
)

# database = Database()
# engine = database.get_db_connection()

# Initialize NoSQL Database
nosql_db = NoSQLDatabase()
mongo_client = nosql_db.get_mongo_connection()
mongo_db = nosql_db.get_mongo_db(mongo_client)


def save_to_mongo(json_data: dict):
    try:
        collection = mongo_db["webhook_data"]
        result = collection.insert_one(json_data)
        return result.inserted_id
    except Exception as e:
        print(f"Error saving data to MongoDB: {e}")
        return None


@router.post("/mensagens")
async def webhook(request: Request):
    json_data = await request.json()

    # Save JSON data to MongoDB
    mongo_result = save_to_mongo(json_data)
    if mongo_result is not None:
        print(f"Data saved to MongoDB with ID: {mongo_result}")
        return JSONResponse(content={"success": True, "message": "Data saved to MongoDB successfully.", "id": str(mongo_result)}, status_code=201)
    else:
        print("Error saving data to MongoDB.")
        return JSONResponse(content={"success": False, "message": "Error saving data to MongoDB."}, status_code=500)
