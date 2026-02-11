from celery import shared_task
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_welcome_email(user_id):
    print(f"Welcome email sent to user {user_id}")
    logger.info(f"Welcome email sent to user {user_id}")
