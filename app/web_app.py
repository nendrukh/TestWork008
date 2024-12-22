import json
from typing import Annotated

import redis
from fastapi import FastAPI, Body, Depends, Header, HTTPException
from fastapi.responses import JSONResponse
from status import HTTP_201_CREATED

from config import API_KEY, CELERY_BACKEND
from celery_worker import execute_task
from database import TransactionRepository
from models import TransactionBodyRequestSchema


def auth_user(authorization: Annotated[str, Header(alias="Authorization")]):
    if authorization != f"ApiKey {API_KEY}":
        raise HTTPException(status_code=401, detail="Invalid API Key")


web_app = FastAPI(dependencies=[Depends(auth_user)])

redis_client = redis.StrictRedis.from_url(CELERY_BACKEND)


@web_app.post("/transactions")
def create_transaction(transaction: Annotated[TransactionBodyRequestSchema, Body()]):
    db = TransactionRepository()

    if db.check_transaction(transaction.transaction_id):
        raise HTTPException(status_code=400, detail="Transaction already exists. transaction_id must be unique.")
    db.add_transaction(transaction.model_dump())

    task = execute_task.apply_async(())
    return JSONResponse(
        status_code=HTTP_201_CREATED,
        content={
            "message": "Transaction received",
            "task_id": task.id
        }
    )


@web_app.delete("/transactions")
def delete_transactions():
    db = TransactionRepository()
    db.delete_transactions()
    redis_client.delete("statistics_cache")

    return JSONResponse(content={"message": "Transactions and cached statistics deleted"})


@web_app.get("/statistics")
def get_statistics():
    cached_statistics = redis_client.get("statistics_cache")
    if not cached_statistics:
        raise HTTPException(status_code=404, detail="Statistics not available")

    return JSONResponse(content=json.loads(cached_statistics))
