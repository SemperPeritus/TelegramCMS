import telegram
from celery import shared_task


@shared_task
def add(x, y):
    return x + y


@shared_task
def send_messages(message):
    channel = message.channel
    bot_model = channel.bot
    token = bot_model.token
    bot = telegram.Bot(token=token)

    bot.send_message(chat_id=channel.id, text=message.text)
