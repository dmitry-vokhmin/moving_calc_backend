from fastapi import APIRouter, status
from calculator.calculations import calculations

router = APIRouter()


@router.post("/calculate/", status_code=status.HTTP_200_OK)
def get_data(data: dict):
    return calculations(data)
