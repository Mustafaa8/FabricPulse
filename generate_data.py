import pandas as pd
import numpy as np
from faker import Faker
from datetime import timedelta
import random

fake = Faker()
Faker.seed(42)

# --- CONFIGURATION ---
NUM_CUSTOMERS = 1000
NUM_ACCOUNTS = 2500  # Many customers have multiple accounts
NUM_TRANSACTIONS = 50000 # High volume for a solid DE project
START_DATE = '-2y'  # Generate 2 years of history

# 1. Generate Instruments (The Catalog)
instruments_data = [
    {'instrument_id': 'INST-001', 'name': 'Apple Inc.', 'category': 'EQUITY', 'provider': 'NASDAQ', 'currency': 'USD', 'status': 'TRADING'},
    {'instrument_id': 'INST-002', 'name': 'Tesla Inc.', 'category': 'EQUITY', 'provider': 'NASDAQ', 'currency': 'USD', 'status': 'TRADING'},
    {'instrument_id': 'INST-003', 'name': 'Bitcoin', 'category': 'CRYPTO', 'provider': 'BINANCE', 'currency': 'BTC', 'status': 'TRADING'},
    {'instrument_id': 'INST-004', 'name': 'Ethereum', 'category': 'CRYPTO', 'provider': 'BINANCE', 'currency': 'ETH', 'status': 'TRADING'},
    {'instrument_id': 'INST-005', 'name': 'S&P 500 ETF', 'category': 'INDEX', 'provider': 'VANGUARD', 'currency': 'USD', 'status': 'TRADING'},
    {'instrument_id': 'INST-CASH-USD', 'name': 'US Dollar', 'category': 'CASH', 'provider': 'SYSTEM', 'currency': 'USD', 'status': 'TRADING'},
]
df_instruments = pd.DataFrame(instruments_data)

# 2. Generate Customers
customers = []
for _ in range(NUM_CUSTOMERS):
    customers.append({
        'customer_id': fake.uuid4()[:8],
        'email': fake.unique.email(),
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'country': fake.country(),
        'customer_status': random.choices(['VERIFIED', 'UNVERIFIED', 'BANNED'], weights=[85, 10, 5])[0],
        'created_at': fake.date_time_between(start_date=START_DATE, end_date='now')
    })
df_customers = pd.DataFrame(customers)

# 3. Generate Accounts
accounts = []
for _ in range(NUM_ACCOUNTS):
    cust = df_customers.sample(n=1).iloc[0]
    accounts.append({
        'account_id': f"ACC-{fake.unique.random_number(digits=6)}",
        'account_type': random.choice(['SAVINGS', 'CHECKING', 'BROKERAGE']),
        'currency': random.choice(['USD', 'EUR', 'GBP']),
        'account_status': random.choices(['ACTIVE', 'FROZEN', 'CLOSED'], weights=[90, 5, 5])[0],
        'opened_at': cust['created_at'] + timedelta(days=random.randint(1, 10)),
        'customer_id': cust['customer_id']
    })
df_accounts = pd.DataFrame(accounts)

# 4. Generate Transactions
transactions = []
for _ in range(NUM_TRANSACTIONS):
    acc = df_accounts.sample(n=1).iloc[0]
    inst = df_instruments.sample(n=1).iloc[0]
    
    tx_time = fake.date_time_between(start_date=acc['opened_at'], end_date='now')
    tx_type = random.choices(['DEPOSIT', 'WITHDRAWAL', 'TRADE'], weights=[20, 10, 70])[0]
    
    # Core Transaction
    tx_id = fake.uuid4()[:12]
    amount = round(random.uniform(5.0, 10000.0), 2)
    direction = 'INBOUND' if tx_type in ['DEPOSIT', 'TRADE'] else 'OUTBOUND'
    
    transactions.append({
        'transaction_id': tx_id,
        'account_id': acc['account_id'],
        'amount': amount,
        'direction': direction,
        'transaction_type': tx_type,
        'transaction_status': random.choices(['COMPLETED', 'FAILED', 'PENDING'], weights=[95, 3, 2])[0],
        'currency': acc['currency'],
        'instrument_id': inst['instrument_id'],
        'timestamp': tx_time,
        'parent_transaction_id': None
    })
    
    # 5. Add Fee for Trades (The "Solo Row" approach you wanted)
    if tx_type == 'TRADE':
        transactions.append({
            'transaction_id': f"FEE-{tx_id[:8]}",
            'account_id': acc['account_id'],
            'amount': round(amount * 0.002, 2), # 0.2% fee
            'direction': 'OUTBOUND',
            'transaction_type': 'FEE',
            'transaction_status': 'COMPLETED',
            'currency': acc['currency'],
            'instrument_id': 'INST-CASH-USD',
            'timestamp': tx_time,
            'parent_transaction_id': tx_id
        })

df_transactions = pd.DataFrame(transactions)

# 6. Currency Exchange Rate (Snapshot)
exchange_rates = [
    {'currency_id': 'EUR', 'to_currency_id': 'USD', 'exchange_rate': 1.09},
    {'currency_id': 'GBP', 'to_currency_id': 'USD', 'exchange_rate': 1.27},
    {'currency_id': 'BTC', 'to_currency_id': 'USD', 'exchange_rate': 65000.00},
    {'currency_id': 'ETH', 'to_currency_id': 'USD', 'exchange_rate': 3500.00},
]
df_rates = pd.DataFrame(exchange_rates)

# Save to Files
df_customers.to_csv('customers.csv', index=False)
df_accounts.to_csv('accounts.csv', index=False)
df_transactions.to_csv('transactions.csv', index=False)
df_instruments.to_csv('instruments.csv', index=False)
df_rates.to_csv('exchange_rates.csv', index=False)

print(f"Project Data Generated: {len(df_transactions)} transactions across {len(df_accounts)} accounts.")
