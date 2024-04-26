import os

from dotenv import load_dotenv

from deta import Deta

from loggers import DetaLogger

logging = DetaLogger(__name__)
load_dotenv()




def get_deta_db(db_name):
    DETA_PROJECT_KEY = os.getenv("DETA_PROJECT_KEY")
    DETA_PROJECT_ID = os.getenv("DETA_PROJECT_ID")
    logging.info(f"Deta key is: {DETA_PROJECT_KEY}")
    deta = Deta(project_key=DETA_PROJECT_KEY, project_id=DETA_PROJECT_ID)
    db = deta.AsyncBase(db_name)

    return db
