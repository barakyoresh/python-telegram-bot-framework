import telegram
import time
import threading
import re


class Bot:
    timer = 1
    bad_usage_message = 'Unrecognized command or parameters.'
    bot = None

    def __init__(self, token = None, bad_usage_message = None, timer = None):
        self.bot = telegram.Bot(token=token)


    def printLastMessage(self):
        print self.bot.getUpdates()[-1].message





def main():
    bot = Bot(token = '113022701:AAHsn9FiQoHHKIZ4b4OpLekFXTKZOc34lfs', timer = 1)
    bot.printLastMessage()


if __name__ == "__main__":
    main()