import os

from dotenv import load_dotenv
from loggers import DetaLogger

from deta import Deta

logging = DetaLogger(__name__)
load_dotenv()


class DetaBase:
    def __init__(self, items_db_name: str, breads_db_name: str) -> None:
        DETA_PROJECT_KEY = os.getenv("DETA_PROJECT_KEY")
        # DETA_PROJECT_ID = os.getenv("DETA_PROJECT_ID")
        logging.info(f"Deta key is: {DETA_PROJECT_KEY}")
        self.deta = Deta(DETA_PROJECT_KEY) #, project_id=DETA_PROJECT_ID)
        self.items_db = self.deta.AsyncBase(items_db_name)
        self.breads_db = self.deta.AsyncBase(breads_db_name)

    async def get_itemsdb_new_rows(self):
        result = await self.items_db.fetch({"csv": False})
        items = result.items
        sorted_items = self.sort_items(items)
        return sorted_items


    def sort_items(self, items: list[dict]):
        sorted_items = sorted(items,key= lambda x: x["date"])
        return sorted_items
    
    async def close(self):
        await self.items_db.close()
        await self.breads_db.close()
