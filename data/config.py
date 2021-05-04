import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
admins = [
    1184689415
]

DB_USER= str(os.getenv('POSTGRES_USER'))
DB_PASS=str(os.getenv('POSTGRES_PASSWORD'))
DB_HOST=str(os.getenv('POSTGRES_HOST'))
DB_NAME=str(os.getenv('POSTGRES_DB'))

ip = os.getenv("ip")

aiogram_redis = {
    'host': ip,
}

