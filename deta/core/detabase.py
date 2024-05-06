import os

from dotenv import load_dotenv
from loggers import DetaLogger

from deta import Deta

logging = DetaLogger(__name__)
load_dotenv()


class DetaBase:
    def __init__(self, db_name: str) -> None:
        DETA_PROJECT_KEY = os.getenv("DETA_PROJECT_KEY")
        logging.info(f"Non-empty Deta Project Key: {bool(DETA_PROJECT_KEY)}")
        self.deta = Deta(DETA_PROJECT_KEY)
        self.db = self.deta.AsyncBase(db_name)

    async def fetch_new_records(self):
        result = await self.db.fetch({"csv": False})
        new_records = result.items
        sorted_new_records = self.sort_records(new_records)
        return sorted_new_records

    def sort_records(self, new_records: list[dict]):
        sorted_records = sorted(new_records, key=lambda x: x["date"])
        return sorted_records
    
    async def close(self):
        return await self.db.close()
    
    async def mark_csv_as_read(self, records: list[dict]):
        for record in records:
            key = record["key"]
            logging.info(f"Marking record with key `{key}` as csv_exported.")
            await self.db.update({"csv": True}, key=key)



# class DetaBase:
#     def __init__(self, items_db_name: str, breads_db_name: str) -> None:
#         DETA_PROJECT_KEY = os.getenv("DETA_PROJECT_KEY")
#         logging.info(f"Deta key is: {DETA_PROJECT_KEY}")
#         self.deta = Deta(DETA_PROJECT_KEY)
#         self.items_db = self.deta.AsyncBase(items_db_name)
#         self.breads_db = self.deta.AsyncBase(breads_db_name)

#     async def get_db_new_rows(self, db):
#         result = await db.fetch({"csv": False})
#         items = result.items
#         sorted_items = self.sort_items(items)
#         return sorted_items

#     def sort_items(self, items: list[dict]):
#         sorted_items = sorted(items, key=lambda x: x["date"])
#         return sorted_items

#     async def close(self):
#         await self.items_db.close()
#         await self.breads_db.close()

#     async def mark_csv_as_read(self, db, data: list[dict]):
#         for row in data:
#             key = row["key"]
#             logging.info(f"{key = }")
#             await db.update({"csv": True}, key=key)
