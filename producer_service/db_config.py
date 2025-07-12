import os
from dotenv import load_dotenv

# Загрузка переменных из .env (если запуск не через compose)
load_dotenv()

DB_CONFIG = {
    'host': 'postgres',
    'port': os.getenv('POSTGRES_PORT'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'database': os.getenv('POSTGRES_DB')
}
