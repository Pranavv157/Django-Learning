from celery import shared_task
import time

@shared_task
def send_welcome_email(username):
    time.sleep(5)  # simulate heavy work
    print(f"Email sent to {username}")
