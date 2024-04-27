import re
from datetime import datetime

import pytz
from loggers import BotLogger

logging = BotLogger(__name__)


def tehran_time_now() -> str:
    tehran_tz = pytz.timezone("Asia/Tehran")
    current_time = datetime.now(tehran_tz)
    formatted_time = current_time.strftime("%Y/%m/%d %H:%M:%S")

    return formatted_time


def search_match(pattern, text, empty_place_holder=""):
    result = re.search(pattern=pattern, string=text)
    if result:
        return result.group(1)
    return empty_place_holder


def orders_from_text(text: str) -> tuple[dict]:
    """
    returns (items_dict, breads_dict)
    """
    # Regex Patterns
    patterns_dict = {
        "customer": r"مشتری:\s*(.*)",
        "items": r"(.*)\s*\(([^)]+)\)\s*(#نان)?",
        "address": r"آدرس:\s*(.*)",
        "phone_number": r"شماره تماس:\s*(.*)",
        "delivery_way": r"شیوه ارسال:\s*(.*)",
        "delivery_fee": r"هزینه ارسال:\s*(.*)",
        "total_fee": r"مبلغ قابل پرداخت:\s*(.*)",
        "description": r"توضیحات:\s*(.*)",
    }

    order_info = {}
    for field, pattern in patterns_dict.items():
        order_info[field] = search_match(pattern, text)
        logging.info(f"`{field}` extracted from text.")

    order_info["delivery_fee"] = float(order_info["delivery_fee"])
    order_info["total_fee"] = float(order_info["total_fee"])

    logging.info("Finished extracting data from text.")

    items = list()
    breads = list()
    for item_match in re.finditer(patterns_dict["items"], text):
        item_name, item_fee, is_bread = item_match.groups()
        items.append([item_name, float(item_fee)])

        if is_bread == "#نان":
            breads.append([item_name, float(item_fee)])

    tehran_time = tehran_time_now()

    items_dict = {
        **order_info,
        "items": items,
        "date": tehran_time,
    }

    breads_dict = items_dict.copy()
    breads_dict["items"] = breads

    return items_dict, breads_dict
