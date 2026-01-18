import json
import os
import random
import time
from datetime import datetime

import faker
import pandas as pd
from azure.eventhub import EventData, EventHubProducerClient
from dotenv import load_dotenv

load_dotenv()
fake = faker.Faker()
instruments_data = [
    {
        "instrument_id": "INST-001",
        "name": "Apple Inc.",
        "category": "EQUITY",
        "provider": "NASDAQ",
        "currency": "USD",
        "status": "TRADING",
    },
    {
        "instrument_id": "INST-002",
        "name": "Tesla Inc.",
        "category": "EQUITY",
        "provider": "NASDAQ",
        "currency": "USD",
        "status": "TRADING",
    },
    {
        "instrument_id": "INST-003",
        "name": "Bitcoin",
        "category": "CRYPTO",
        "provider": "BINANCE",
        "currency": "BTC",
        "status": "TRADING",
    },
    {
        "instrument_id": "INST-004",
        "name": "Ethereum",
        "category": "CRYPTO",
        "provider": "BINANCE",
        "currency": "ETH",
        "status": "TRADING",
    },
    {
        "instrument_id": "INST-005",
        "name": "S&P 500 ETF",
        "category": "INDEX",
        "provider": "VANGUARD",
        "currency": "USD",
        "status": "TRADING",
    },
    {
        "instrument_id": "INST-CASH-USD",
        "name": "US Dollar",
        "category": "CASH",
        "provider": "SYSTEM",
        "currency": "USD",
        "status": "TRADING",
    },
]
df_instruments = pd.DataFrame(instruments_data)

CONN_STR = os.getenv("CONN_STR")
EVENTHUB_NAME = os.getenv("EVENTHUB_NAME")


def generate_events():
    transactions_status = random.choices(
        ["COMPLETED", "FAILED", "PENDING"], weights=[95, 3, 2]
    )[0]
    transaction_type = random.choices(
        ["DEPOSIT", "WITHDRAWAL", "TRADE"], weights=[20, 10, 70]
    )[0]
    timestamp = datetime.now()
    amount = round(random.uniform(5.0, 10000.0), 2)
    account_id = f"ACC-{fake.unique.random_number(digits=6)}"
    transaction_id = fake.uuid4()[:12]
    instrument_id = inst = df_instruments.sample(n=1).iloc[0]["instrument_id"]
    direction = "INBOUND" if transaction_type in ["DEPOSIT", "TRADE"] else "OUTBOUND"
    currency = random.choice(["USD", "EUR", "GBP"])

    transactions = [
        {
            "transaction_id": transaction_id,
            "account_id": account_id,
            "amount": amount,
            "direction": direction,
            "transaction_type": transaction_type,
            "transaction_status": transactions_status,
            "currency": currency,
            "instrument_id": instrument_id,
            "timestamp": str(timestamp),
            "parent_transaction_id": None,
        }
    ]
    if transaction_type == "TRADE":
        transactions.append(
            {
                "transaction_id": f"FEE-{transaction_id[:8]}",
                "account_id": account_id,
                "amount": round(amount * 0.002, 2),  # 0.2% fee
                "direction": "OUTBOUND",
                "transaction_type": "FEE",
                "transaction_status": "COMPLETED",
                "currency": currency,
                "instrument_id": "INST-CASH-USD",
                "timestamp": str(timestamp),
                "parent_transaction_id": transaction_id,
            }
        )
    return transactions


def send_event():
    producer = EventHubProducerClient.from_connection_string(
        conn_str=str(CONN_STR), eventhub_name=str(EVENTHUB_NAME)
    )
    with producer:
        transactions = generate_events()
        batch = producer.create_batch()
        batch.add(EventData(json.dumps(transactions)))
        producer.send_batch(batch)
        print("events has been delivered")


if __name__ == "__main__":
    while True:
        send_event()
        time.sleep(random.randint(1, 6))
