import telegram
import time
import threading
import re
from collections import deque

SLEEP_TIME_STEP = 1

class Bot:
    __message_queue = deque([])
    __timer = 1
    __commands = {} #name : (cb, params, description)
    __bad_usage_message = 'Unrecognized command or parameters.'
    __bot = None
    __offset = None

    def __init__(self, token, bad_usage_message = None, timer = None):
        if not token:
            raise Exception('Invalid input token')
        if timer:
            self.__timer = timer
        if bad_usage_message:
            self.__bad_usage_message = bad_usage_message

        self.__bot = telegram.Bot(token=token)

    def set_timer(self, new_timer):
        self.__timer = new_timer

    def get_timer(self):
        return self.__timer

    def get_bot_commands(self):
        cmds = []
        for cmd in self.commands:
            cmd.append(cmd + " - " + self.commands[cmd][2])
        return cmds

    def set_bad_usage_message(self, new_message):
        self.__bad_usage_message = new_message

    def get_default_message(self):
        return self.__bad_usage_message

    def get_bot_name(self):
        return self.__bot.getMe().username

    def send_message(self, chat_id, message, markup):
        self.__bot.sendMessage(chat_id, message, reply_markup=markup)

    def wait_for_message(self, chat_id, timeout=5):
        updates = self.__bot.getUpdates(offset=self.__offset)
        time_passed = 1
        while not updates.results or time_passed <= timeout:
            time.sleep(SLEEP_TIME_STEP)
            time_passed += SLEEP_TIME_STEP
            updates = self.__bot.getUpdates(offset=self.__offset)



    def add_command(self, cmd_name, cmd_description, cmd_params, cmd_cb):
        pass

    def activate(self):
        pass

def main():

    #bot = Bot(token = '113022701:AAHsn9FiQoHHKIZ4b4OpLekFXTKZOc34lfs', timer = 1)
    #bot.printLastMessage()


if __name__ == "__main__":
    main()