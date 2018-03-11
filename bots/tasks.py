import telegram
from celery import shared_task


@shared_task
def send_message(token, channel_id, message_text, message_image_path):
    bot = telegram.Bot(token=token)
    if message_image_path is None:
        bot.send_message(chat_id=channel_id, text=message_text)
    else:
        bot.send_photo(chat_id=channel_id, photo=open(message_image_path, 'rb'))
