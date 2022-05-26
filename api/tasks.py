from celery import shared_task
from datetime import datetime as dt

from .models import Order, sync_array_to_bd, format_values
from .tools import read_google_sheet, notify

SYNC_ERROR = "{}: ошибка при выполнении синхронизации: {}."
SYNC_SUCCESSFULLY = "{} - {}: синхронизация БД с Google sheets успешно выполнена."
DELIVERY_DATE_EXPIRED = "Истёк срок поставки для заказов {}"


@shared_task
def get_sync():
    """
    Celery scheduler's task
    :return: Task's report or exception representation
    """
    start = dt.now().strftime("%Y-%m-%d %H:%m")
    try:
        sync_array_to_bd(Order, "own_id", read_google_sheet(), formatter=format_values)
    except Exception as exc:
        return SYNC_ERROR.format(start, exc.__repr__())
    end = dt.now().strftime("%Y-%m-%d %H:%m")
    return SYNC_SUCCESSFULLY.format(start, end)


@shared_task
def check_delivery_date():
    """
    Check delivery dates and notifies if they have expired
    :return: Task's report log of checking
    """
    expired_orders = tuple(o[0] for o in Order.objects.filter(delivery_date__lte=dt.now()).values_list("order_id"))
    if expired_orders:
        notify(DELIVERY_DATE_EXPIRED.format(expired_orders))
        return "Has expired orders. Notified."
    return "Hasn't expired orders."
