import json
from locale import currency
import os
from datetime import datetime
import random

from azure.eventhub import EventHubProducerClient
from dotenv import load_dotenv

load_dotenv(dotenv_path="./env")
producer = 1


EVENTHUB_NAMESPACE = os.getenv("EVENTHUB_NAMESPACE")
EVENTHUB_NAME = os.getenv("EVENTHUB_NAME")

def generate_transactions():
    transactions_status = []
    transaction_type = []
    timestamp = datetime.now()
    amount = random.randint(0,2500)
    account_id = 0
    transaction_id = 0
    currency = "EGY"
    parent_transaction_id = 0
    pass
    


def send_event():
    pass
