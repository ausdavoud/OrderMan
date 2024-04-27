def get_messages_field() -> dict:
    message_fields = {
        "customer": "👤 مشتری",
        "items": "🛒 اقلام",
        "address": "📍 آدرس",
        "phone_number": "📞 شماره تماس",
        "delivery_way": "🚚 شیوه ارسال",
        "delivery_fee": "💰 هزینه ارسال",
        "total_fee": "💰 مبلغ قابل پرداخت",
        "description": "✍🏻 توضیحات",
    }

    return message_fields


def raw_dict_to_message(order: dict) -> str:
    custom_message_field = get_messages_field()
    custom_message_field.pop("customer")
    custom_message_field.pop("items")

    text = ""

    customer = order["customer"]
    text += f"👤 مشتری: {customer}\n\n"

    text += "🛒 "  # اقلام:\n"

    items = order["items"]
    print(f"{items = }")
    for item in items:
        print(f"{item = }")
        item_name, item_fee = item
        text += f"{item_name} - {item_fee} تومان\n"

    for english_key, farsi_key in custom_message_field.items():
        text += f"\n{farsi_key}: {order[english_key]}\n"

    text += "‌"  # Add this to make another extra line
    return text


def order_dict_to_message(order: dict) -> str:
    """converts a dictionary to a beautiful telegram message!"""

    text = "سفارش زیر را تایید می‌کنید؟\n\n"
    text += raw_dict_to_message(order)
    return text


def deta_result_to_message(result: dict) -> str:
    data: dict = result["result"]
    data.pop("csv")
    text = "سفارش زیر ثبت شد!\n\n"
    text += raw_dict_to_message(data)

    key = data["key"]
    text += f"\n🔑 کلید در دیتابیس: `{key}`\n"

    text += "‌"  # Add this to make another extra line

    return text
