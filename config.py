import os
import dotenv

dotenv.load_dotenv(".env")

DATA_BASE_URL = os.getenv("DATABASE_URL")
DOMAIN = "https://moving-calculator.herokuapp.com/"
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_ADDRESS = "movingcalc01@gmail.com"
