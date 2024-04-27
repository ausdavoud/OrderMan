from contextlib import asynccontextmanager

from core import DetaBase, DetaDrive
from deta_csv import merge_list_csv
from fastapi import FastAPI
from loggers import DetaLogger

logging = DetaLogger(__name__)


deta_bases = None
deta_drive = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global deta_bases, deta_drive
    deta_bases = DetaBase("items_db", "breads_db")
    deta_drive = DetaDrive("csv")
    logging.info("DetaBases/Drives were set.")

    yield

    await deta_bases.close()


app = FastAPI(lifespan=lifespan)


@app.post("/put_items")
async def put_items(items_dict: dict):
    logging.info("Dict was received by router.")
    try:
        result = await deta_bases.items_db.put(items_dict)
        return {"result": result}
    except Exception:
        return {"error message": "Dict already exists."}


@app.post("/put_breads")
async def put_breads(breads_dict: dict):
    logging.info("Dict was received by router.")
    try:
        result = await deta_bases.breads_db.put(breads_dict)
        return {"result": result}
    except Exception as e:
        return {"error message": f"Dict already exists. {e}"}


@app.get("/update_csv")
async def update_csv():
    new_rows = await deta_bases.get_itemsdb_new_rows()
    if not new_rows:
        return {"result": "ok"}

    for new_row in new_rows:
        new_row.pop("csv")

    logging.info(f"{new_rows}")

    csv_file = deta_drive.get_last_csv()
    logging.info(f"{csv_file = }")

    # merge new rows and csv
    new_string_io_data = merge_list_csv(csv_file, new_rows)

    encoded = str(new_string_io_data.getvalue()).encode("utf-8")
    deta_drive.save_csv("1_csv.csv", encoded)
    # upload the new csv with date of now
    return {"result": "ok"}


@app.get("/get_csv")
async def get_csv():
    pass
