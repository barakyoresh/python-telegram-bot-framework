import telegram
import time
import threading
import re

class telegram_framework:

    def Bot(self):
        pass




bot = telegram.Bot(token='113022701:AAHsn9FiQoHHKIZ4b4OpLekFXTKZOc34lfs')

print bot.getUpdates(None, 10, 0)[-1].message