import json
from heapq import nlargest

import redis

from config import CELERY_BACKEND
from celery_config import celery_app
from database import TransactionRepository
from models import TransactionStatisticsSchema, TransactionSchema

redis_client = redis.StrictRedis.from_url(CELERY_BACKEND)


class TransactionWorker:
    @staticmethod
    def calculate_statistics() -> dict:
        db = TransactionRepository()
        total_transactions = db.get_number_of_transactions()
        average_amount = db.get_average_amount()
        transactions = db.get_all_transactions()

        top_transactions = nlargest(3, transactions, key=lambda t: t.amount)
        top_transactions_result = [
            TransactionSchema.model_validate({"transaction_id": t.transaction_id, "amount": t.amount})
            for t in top_transactions
        ]

        calculated_statistics = TransactionStatisticsSchema(
            total_transactions=total_transactions,
            average_transaction_amount=average_amount,
            top_transactions=top_transactions_result
        )

        redis_client.set("statistics_cache", json.dumps(calculated_statistics.model_dump()))
        return calculated_statistics.model_dump()


@celery_app.task
def execute_task():
    return TransactionWorker.calculate_statistics()
