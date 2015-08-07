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

    def set_timer(self, new_timer):
        pass

    def get_timer(self):
        pass

    def get_bot_commands(self):
        pass

    def set_default_message(self, new_message):
        pass

    def get_default_message(self):
        pass

    def get_bot_name(self):
        pass

    def send_message(self, chat_id, message):
        pass

    def wait_for_message(self, chat_id):
        pass

    def add_command(self, cmd_name, cmd_description, cmd_params, cmd_cb):
        pass

    def activate(self):
        pass

def main():
    bot = Bot(token = '113022701:AAHsn9FiQoHHKIZ4b4OpLekFXTKZOc34lfs', timer = 1)
    bot.printLastMessage()


if __name__ == "__main__":
    main()