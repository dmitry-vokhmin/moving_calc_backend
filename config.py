import os
import dotenv
from pathlib import Path

env_path = Path(__file__).parent.joinpath(".env")
dotenv.load_dotenv(env_path)

DATA_BASE_URL = os.getenv("DATABASE_URL")
DOMAIN = "https://moving-calculator.herokuapp.com/"
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_ADDRESS = "movingcalc01@gmail.com"
