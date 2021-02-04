import csv
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry



session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)

with open("uszips.csv", encoding='utf-8') as r_file:
    file_reader = csv.reader(r_file)
    count = 0
    for row in file_reader:
        if count == 0:
            count += 1
            continue
        session.post('http://127.0.0.1:8080/zip_code/', json={"zip_code": f"{row[0]}",
                                                               "city": f"{row[3]}",
                                                               "state": f"{row[4]}"})

print("END")
