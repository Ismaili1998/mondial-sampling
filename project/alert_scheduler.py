from datetime import datetime, timedelta
from apscheduler.schedulers.background import BlockingScheduler
from .models import Buyer

def calculate_alert(payment_date):
    current_date = datetime.now()
    days_remaining = (payment_date - current_date).days

    if days_remaining <= 30 and days_remaining > 20:
        alert_level = "normal"

    elif days_remaining <= 20 and days_remaining > 10:
        alert_level = "warning"

    elif days_remaining <= 10 and days_remaining >= 0:
        alert_level = "danger"

    else:
        alert_level = "expired"

    return alert_level, days_remaining

def create_payment_alert():
    due_date = datetime.now()
    alert_level, days_remaining = calculate_alert(due_date)
    b = Buyer(name="XXXXX", phone_number="028283", email="alal@gmail.Com")
    b.save()

def schedule_alert(run_date):
    run_date = datetime.now() + timedelta(seconds=10)
    scheduler = BlockingScheduler()
    scheduler.add_job(create_payment_alert, "date", run_date = run_date)
    scheduler.start()
















#     return a + b
    
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