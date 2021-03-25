from pathlib import Path
import csv
import requests

file_path = Path(__file__).parent.joinpath("inventory.csv")
with file_path.open("r", encoding="utf-8") as file:
    file_reader = csv.reader(file)
    item = set()
    for idx, row in enumerate(file_reader):
        if idx == 0:
            continue
        if row[0] not in item:
            requests.post('http://127.0.0.1:8080/inventory/', json={"name": str(row[1]), "dimension": float(row[3])})
        item.add(row[0])
