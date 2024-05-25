from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from orders.models import Order


@shared_task
def send_order_email(order_id: int, *args, **kwargs):
    """Отправка email администратору, о созданном заказе."""
    order = Order.objects.get(id=order_id)
    subject = f"Новый заказ №{order.id}"
    printy_url = settings.HOST + order.printy.get_absolute_url()
    stamp_url = settings.HOST + order.stamp.get_absolute_url()
    html_message = render_to_string(
        "order_email_template.html",
        {
            "order": order,
            "printy_url": printy_url,
            "stamp_url": stamp_url,
        },
    )
    return send_mail(
        subject=subject,
        message=None,
        html_message=html_message,
        from_email=settings.EMAIL_HOST_USER,
        auth_user=settings.EMAIL_HOST_USER,
        auth_password=settings.EMAIL_HOST_PASSWORD,
        recipient_list=(settings.ADMIN_EMAIL,),
        fail_silently=False,
    )
