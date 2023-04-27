from celery import shared_task
from back import settings

@shared_task(bind=True)
def item_sold(self):
    # do something here
    pass
