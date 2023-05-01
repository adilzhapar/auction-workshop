import logging

from celery import shared_task
from back import settings
from .models import ItemOnSale, Item
from django.core.mail import send_mail


@shared_task()
def item_sold(item_on_sale_id, current_price_on_call):
    item_on_sale = ItemOnSale.objects.get(id=item_on_sale_id)
    item = item_on_sale.item
    if float(current_price_on_call) < float(item_on_sale.current_price):
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


@shared_task()
def send_notification_email(action, item_name, item_cur_price, item_last_bidder_name, item_owner_email):
    if action == 'create':
        topic = 'Your item is on sale!'
        message = f"{item_name}'s current price: {str(item_cur_price)}\nbidder is {item_last_bidder_name}",
    else:
        topic = 'Your bid was intercepted!'
        message = f"{item_name} Current price: {str(item_cur_price)}"
    payload = {
        'subject': topic,
        'message': str(message[0]),
        'from_email': settings.DEFAULT_FROM_EMAIL,
        'recipient_list': [item_owner_email],
        'fail_silently': False
    }
    send_mail(**payload)
    return "Done"
