from celery import shared_task
from django.utils import timezone
import logging
logger = logging.getLogger(__name__)

def calculate_alert(payment_date):
    # Get the current date
    current_date = timezone.now().date()
    # Calculate the days remaining until the payment date
    days_remaining = (payment_date - current_date).days

    # Determine the alert level
    if days_remaining <= 30 and days_remaining > 20:
        alert_level = "normal"

    elif days_remaining <= 20 and days_remaining > 10:
        alert_level = "warning"

    elif days_remaining <= 10 and days_remaining >= 0:
        alert_level = "danger"

    else:
        alert_level = "expired"
        
    return alert_level, days_remaining


@shared_task
def create_payment_alert(due_date):
    logger.info(f"========================================")
    
    # try:

    #     # Calculate the alert level and days remaining
    #     alert_level, days_remaining = calculate_alert(due_date)

    #     # # You can update the payment model with the alert level and days remaining
    #     # payment.alert_level = alert_level
    #     # payment.days_remaining = days_remaining
    #     # payment.save()

    #     # Log or send notifications as needed
    #     print(f"Alert created for Payment . Alert Level: {alert_level}. Days Remaining: {days_remaining}")
    # except : #Payment.DoesNotExist
    #     print(f"Payment with this id does not exist.")