import os
from datetime import datetime

import pytz
from loggers import DetaLogger

from deta import Deta

logging = DetaLogger(__name__)


def tehran_time_now() -> str:
    tehran_tz = pytz.timezone("Asia/Tehran")
    current_time = datetime.now(tehran_tz)
    formatted_time = current_time.strftime("%Y/%m/%d %H:%M:%S")

    return formatted_time


class DetaDrive:
    def __init__(self, name="csv") -> None:
        DETA_PROJECT_KEY = os.getenv("DETA_PROJECT_KEY")
        self.deta = Deta(DETA_PROJECT_KEY)
        self.drive = self.deta.Drive(name)

    def get_last_csv_name(self):
        # Get list for the first time
        response = self.drive.list()

        while response.get("paging") and "last" in response["paging"]:
            last = response["paging"]["last"]
            response = self.drive.list(last=last)

        # If no additional pages or the last page is reached, return the last item
        logging.info(f"{response = }")
        if names := response["names"]:
            logging.info(f"{names = }")
            return names[-1]
        return None

    def get_last_csv(self):
        last_csv_name = self.get_last_csv_name()
        if last_csv_name:
            file = self.drive.get(last_csv_name)
            return file.read()
        return None

    def save_csv(self, file_name, csv_data):
        self.drive.put(file_name, csv_data)
