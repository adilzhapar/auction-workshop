from celery import shared_task
from back import settings
from back.celery import app
from .models import ItemOnSale, Item
from django.core.mail import send_mail

@app.task
def item_sold(item_on_sale_id):
    # do something here
    item_on_sale = ItemOnSale.objects.get(id=item_on_sale_id)
    item = Item.objects.get(id=item_on_sale.item.id)
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

