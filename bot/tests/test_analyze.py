from bot.core import orders_from_text

def test_orders_from_text():
    from pprint import pprint
    text = """
مشتری: علی فتاح
اقلام:
یک کیلو نان بلوط(۳۵۰) #نان
دو کیلو کشک (۵۴۰)
آدرس: فلان جا بهمان جا اینجا اونجا پلاک ۵
شماره تماس: 09120000000 
شیوه ارسال: تیپاکس
هزینه ارسال: ۲۵
مبلغ قابل پرداخت: ۹۱۵
توضیحات: کشک خوشمزه
"""

    items_dict, breads_dict = orders_from_text(text)
    with open("items.txt", "w") as file:
        file.write(str(items_dict))

    pprint(f"{items_dict = }\n\n\n{breads_dict = }")