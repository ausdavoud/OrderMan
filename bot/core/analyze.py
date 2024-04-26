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
    customer_pattern = r"مشتری:\s*(.*)"
    item_pattern = r"(.*)\s*\(([^)]+)\)\s*(#نان)?"
    address_pattern = r"آدرس:\s*(.*)"
    phone_number_pattern = r"شماره تماس:\s*(.*)"
    delivery_way_pattern = r"شیوه ارسال:\s*(.*)"
    delivery_fee_pattern = r"هزینه ارسال:\s*(.*)"
    total_fee_pattern = r"مبلغ قابل پرداخت:\s*(.*)"
    description_pattern = r"توضیحات:\s*(.*)"

    customer = search_match(customer_pattern, text)
    logging.info("Customer found in text.")
    address = search_match(address_pattern, text)
    logging.info("Address found in text.")
    phone_number = search_match(phone_number_pattern, text)
    logging.info("Phone Number found in text.")

    delivery_way = search_match(delivery_way_pattern, text)
    logging.info("Delivery Way found in text.")

    delivery_fee = float(search_match(delivery_fee_pattern, text))
    logging.info("Delivery Fee found in text.")

    total_fee = float(search_match(total_fee_pattern, text))
    logging.info("Total Fee found in text.")

    description = search_match(description_pattern, text)
    logging.info("Description found in text.")


    items = list()
    breads = list()
    for item_match in re.finditer(item_pattern, text):
        item_name, item_fee, is_bread = item_match.groups()
        items.append([item_name, float(item_fee)])
        logging.info(f"{is_bread = }")
        if is_bread == "#نان":
            breads.append([item_name, float(item_fee)])

    items_dict = {
        "Customer": customer,
        "Items": items,
        "Address": address,
        "Phone Number": phone_number,
        "Delivery Way": delivery_way,
        "Delivery Fee": delivery_fee,
        "Total Fee": total_fee,
        "Description": description,
        "Date": tehran_time_now(),
    }

    breads_dict = {
        "Customer": customer,
        "Items": breads,
        "Address": address,
        "Phone Number": phone_number,
        "Delivery Way": delivery_way,
        "Delivery Fee": delivery_fee,
        "Total Fee": total_fee,
        "Description": description,
        "Date": tehran_time_now(),
    }

    return items_dict, breads_dict


