import os
import dotenv

dotenv.load_dotenv(".env")

DATA_BASE_URL = os.getenv("DATABASE_URL")
DOMAIN = "http://127.0.0.1:8080/"
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_ADDRESS = "movingcalc01@gmail.com"
