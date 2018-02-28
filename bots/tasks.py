import telegram
from celery import shared_task


@shared_task
def add(x, y):
    return x + y


@shared_task
def send_messages(token, channel_id, message_text):
    bot = telegram.Bot(token=token)
    bot.send_message(chat_id=channel_id, text=message_text)
