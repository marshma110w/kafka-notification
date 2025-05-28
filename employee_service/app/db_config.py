import os
from dotenv import load_dotenv

# Загрузка переменных из .env (если запуск не через compose)
load_dotenv()

DB_CONFIG = {
    'host': 'localhost',
    'port': os.getenv('POSTGRES_PORT', '5432'),
    'user': os.getenv('POSTGRES_USER', 'postgres'),
    'password': os.getenv('POSTGRES_PASSWORD', ''),
    'database': os.getenv('POSTGRES_DB', 'postgres')
}
