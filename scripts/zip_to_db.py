from pathlib import Path
import aiohttp
import asyncio
import csv


async def post_zip(zip_code, session):
    while True:
        response = await session.post('http://127.0.0.1:8080/zip_code/', json=zip_code)
        if response.status == 201:
            break


async def csv_to_dict(file_path: Path):
    with file_path.open("r", encoding='utf-8') as r_file:
        file_reader = csv.reader(r_file)
        for idx, row in enumerate(file_reader):
            if idx == 0:
                continue
            data = {"zip_code": f"{row[0]}", "city": f"{row[3]}", "state": f"{row[4]}"}
            yield data


async def main():
    db_file = Path(__file__).parent.joinpath("uszips.csv")
    tasks = []
    async with aiohttp.ClientSession() as session:
        async for data in csv_to_dict(db_file):
            tasks.append(asyncio.create_task(post_zip(data, session)))
        await asyncio.wait(tasks)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
