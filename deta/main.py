from contextlib import asynccontextmanager

from core import get_deta_db
from fastapi import FastAPI
from loggers import DetaLogger

logging = DetaLogger(__name__)


items_db = None
breads_db = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global items_db, breads_db
    items_db = get_deta_db("items_db")
    breads_db = get_deta_db("breads_db")

    yield

    await items_db.close()
    await breads_db.close()


app = FastAPI(lifespan=lifespan)


@app.post("/put_items")
async def put_items(items_dict: dict):
    logging.info("Dict was received by router.")
    try:
        result = await items_db.put(items_dict)
        return {"result": result, "are_dict_=": str(items_db == breads_db)}
    except Exception:
        return {"error message": "Dict already exists."}


@app.post("/put_breads")
async def put_breads(breads_dict: dict):
    logging.info("Dict was received by router.")
    try:
        result = await breads_db.put(breads_dict)
        return {"result": result}
    except Exception as e:
        return {"error message": f"Dict already exists. {e}"}
