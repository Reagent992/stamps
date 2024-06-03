import logging

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from orders.models import Order

logger = logging.getLogger("__name__")


def get_order(order_id: int) -> Order:
    try:
        return Order.objects.select_related("printy", "stamp").get(id=order_id)
    except Order.DoesNotExist:
        logger.error(f"Order with id {order_id} does not exist")
        raise Order.DoesNotExist


@shared_task
def send_order_email(
    order_id: int, recipient: str = settings.ADMIN_EMAIL
) -> None:
    """Send email about new order.
    Emails with empty recipient will be send to admin."""
    order = get_order(order_id)
    subject = f"Новый заказ №{order.id}"
    printy_url = settings.HOST + order.printy.get_absolute_url()
    stamp_url = settings.HOST + order.stamp.get_absolute_url()
    html_message = render_to_string(
        settings.NEW_ORDER_EMAIL_TEMPLATE,
        {
            "item": order,
            "printy_url": printy_url,
            "stamp_url": stamp_url,
        },
    )
    logger.info(f"Sending email to {recipient}")
    try:
        send_mail(
            subject=subject,
            message=None,
            html_message=html_message,
            from_email=settings.EMAIL_HOST_USER,
            auth_user=settings.EMAIL_HOST_USER,
            auth_password=settings.EMAIL_HOST_PASSWORD,
            recipient_list=(recipient,),
            fail_silently=False,
        )
    except Exception as e:
        logger.error("Error occurred while sending email:", e)
    else:
        logger.info("Email sent successfully")
