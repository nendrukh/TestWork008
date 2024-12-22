from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, func
from sqlalchemy.orm import sessionmaker, declarative_base

from config import POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT


Base = declarative_base()


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, unique=True, nullable=False)
    user_id = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)


class TransactionRepository:
    def __init__(self):
        self.engine = create_engine(
            f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
        )
        self.session_local = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base.metadata.create_all(bind=self.engine)

    def check_transaction(self, transaction_id: str) -> bool:
        with self.session_local() as session:
            if session.query(Transaction).filter_by(transaction_id=transaction_id).first():
                return True

            return False

    def add_transaction(self, transaction: dict):
        new_transaction = Transaction(**transaction)

        with self.session_local() as session:
            session.add(new_transaction)
            session.commit()

    def get_number_of_transactions(self) -> int:
        with self.session_local() as session:
            number_transactions = session.query(func.count(Transaction.id)).scalar()

            return number_transactions

    def get_average_amount(self) -> float:
        with self.session_local() as session:
            average_amount = session.query(func.avg(Transaction.amount)).scalar()
            return average_amount

    def get_all_transactions(self) -> list[Transaction]:
        with self.session_local() as session:
            all_transactions = session.query(Transaction).all()

            return all_transactions

    def delete_transactions(self):
        with self.session_local() as session:
            session.query(Transaction).delete()
            session.commit()
