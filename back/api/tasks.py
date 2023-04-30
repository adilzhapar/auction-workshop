from celery import shared_task
from back import settings
from back.celery import app
from .models import ItemOnSale, Item
from django.core.mail import send_mail


@app.task
def item_sold(item_on_sale_id, current_price_on_call):
    # do something here
    item_on_sale = ItemOnSale.objects.get(id=item_on_sale_id)
    item = Item.objects.get(id=item_on_sale.item.id)
    if int(current_price_on_call) < int(item_on_sale.current_price):
        return
    else:
        item.status = Item.SOLD

        send_mail(
            'Your item has been sold!',
            item.name + ' is sold!' + ' Current price: ' + str(item_on_sale.current_price),
            settings.DEFAULT_FROM_EMAIL,
            [item.owner.email],
            fail_silently=False,
        )
        send_mail(
            'You have bought an item!',
            item.name + ' is sold!' + ' Current price: ' + str(item_on_sale.current_price),
            settings.DEFAULT_FROM_EMAIL,
            [item_on_sale.last_bidder.email],
            fail_silently=False,
        )
        item_on_sale.delete()
        return "Done"


# @shared_task
# def send_notification_email(topic, message, send_to):
#     send_mail(
#         topic,
#         message,
#         settings.DEFAULT_FROM_EMAIL,
#         send_to,
#         fail_silently=False,
#     )
#     return "Done"
