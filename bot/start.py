import os
import telegram


if __name__ == "__main__":
    bot = telegram.Bot(token=os.environ['TOKEN'])
    print(bot.get_me())
