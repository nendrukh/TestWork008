from datetime import datetime
from pydantic import BaseModel, field_validator


class TransactionSchema(BaseModel):
    transaction_id: str
    amount: float


class TransactionStatisticsSchema(BaseModel):
    total_transactions: int
    average_transaction_amount: float
    top_transactions: list[TransactionSchema]


class TransactionBodyRequestSchema(TransactionSchema):
    user_id: str
    currency: str
    timestamp: datetime

    @field_validator("amount")
    def amount_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError("Amount must be positive.")
        return value
