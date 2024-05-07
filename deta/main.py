from contextlib import asynccontextmanager
from datetime import datetime

import pytz
from core import DetaBase, DetaDrive
from deta_csv import merge_list_csv
from fastapi import FastAPI
from fastapi.responses import FileResponse
from loggers import DetaLogger
from pydantic import BaseModel

logging = DetaLogger(__name__)


items_db = None
breads_db = None
pre_orders_db = None

items_deta_drive = None
breads_deta_drive = None
pre_orders_deta_drive = None


def tehran_time_now() -> str:
    tehran_tz = pytz.timezone("Asia/Tehran")
    current_time = datetime.now(tehran_tz)
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

    return formatted_time


@asynccontextmanager
async def lifespan(app: FastAPI):
    global items_db, breads_db, pre_orders_db, items_deta_drive, breads_deta_drive, pre_orders_deta_drive
    items_db = DetaBase("items_db")
    breads_db = DetaBase("breads_db")
    pre_orders_db = DetaBase("preorders_db")

    items_deta_drive = DetaDrive("items")
    breads_deta_drive = DetaDrive("breads")
    pre_orders_deta_drive = DetaDrive("pre_orders")

    logging.info("DetaBases/Drives were set.")

    yield

    await items_db.close()
    await breads_db.close()
    await pre_orders_db.close()


app = FastAPI(lifespan=lifespan)


@app.post("/put_items")
async def put_items(items_dict: dict):
    logging.info("Dict was received by router.")
    try:
        result = await items_db.db.put(items_dict)
        return {"result": result}
    except Exception:
        return {"error message": "Dict already exists."}


@app.post("/put_breads")
async def put_breads(breads_dict: dict):
    logging.info("Dict was received by router.")
    try:
        result = await breads_db.db.put(breads_dict)
        return {"result": result}
    except Exception as e:
        return {"error message": f"Dict already exists. {e}"}
    

@app.post("/put_preorders")
async def put_pre_orders(pre_orders_dict: dict):
    logging.info("Request was received by put_preorders router")
    try:
        result = await pre_orders_db.db.put(pre_orders_dict)
        return {"result": result}
    except Exception as e:
        return {"error message": f"Dict already exists. Error:{e}"}


def pop_csv_column(data: list[dict]):
    for row in data:
        row.pop("csv")


async def core_update_csv(drive, csv_name, new_rows: list[dict]):
    pop_csv_column(new_rows)

    csv_file = drive.get_last_csv()

    new_string_io_data = merge_list_csv(csv_file, new_rows)

    encoded = str(new_string_io_data.getvalue()).encode("utf-8")
    current_time = tehran_time_now()
    drive.save_csv(f"{current_time} - {csv_name}.csv", encoded)


@app.get("/update_csv")
async def update_csv():
    items_new_rows = await items_db.fetch_new_records()
    breads_new_rows = await breads_db.fetch_new_records()
    pre_orders_new_rows = await pre_orders_db.fetch_new_records()

    if items_deta_drive:
        await core_update_csv(
            drive=items_deta_drive, csv_name="items", new_rows=items_new_rows
        )

    if breads_new_rows:
        await core_update_csv(
            drive=breads_deta_drive, csv_name="breads", new_rows=breads_new_rows
        )

    if pre_orders_new_rows:
        await core_update_csv(
            drive=pre_orders_deta_drive, csv_name="preorders", new_rows=pre_orders_new_rows
        )

    await items_db.mark_csv_as_read(items_new_rows)
    await breads_db.mark_csv_as_read(breads_new_rows)
    await pre_orders_db.mark_csv_as_read(pre_orders_new_rows)

    return {"result": "ok"}


class ActionEvent(BaseModel):
    id: str
    trigger: str


class Action(BaseModel):
    event: ActionEvent


@app.post("/__space/v0/actions")
async def actions(action: Action):
    logging.info("Triggered Automatic Action to Update.")
    if action.event.id == "update":
        await update_csv()


@app.get("/get_items_csv")
async def get_items_csv():
    csv_bytes = items_deta_drive.get_last_csv()
    csv_name = items_deta_drive.get_last_csv_name()
    return {
        "file_name": csv_name,
        "content": FileResponse(csv_bytes, media_type="application/octet-stream"),
    }


@app.get("/get_breads_csv")
async def get_breads_csv():
    csv_bytes = breads_deta_drive.get_last_csv()
    csv_name = breads_deta_drive.get_last_csv_name()
    return {
        "file_name": csv_name,
        "content": FileResponse(csv_bytes, media_type="application/octet-stream"),
    }

@app.get("/get_preorders_csv")
async def get_pre_orders_csv():
    csv_bytes = pre_orders_deta_drive.get_last_csv()
    csv_name = pre_orders_deta_drive.get_last_csv_name()
    return {
        "file_name": csv_name,
        "content": FileResponse(csv_bytes, media_type="application/octet-stream")
    }
