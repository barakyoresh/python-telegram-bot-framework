import telegram
import time
import threading
import re
from collections import deque

SLEEP_TIME_STEP = 1

class Bot:
    __message_queue = deque([])
    __initiated = False
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

    def get___bot_commands(self):
        cmds = []
        for cmd in self.commands:
            cmd.append(cmd + " - " + self.commands[cmd][2])
        return cmds

    def set_bad_usage_message(self, new_message):
        self.__bad_usage_message = new_message

    def get_default_message(self):
        return self.__bad_usage_message

    def get___bot_name(self):
        return self.__bot.getMe().username

    def send_message(self, chat_id, message, markup=None):
        if not markup:
            markup = telegram.ReplyKeyboardHide
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
        if not self.__initiated:
            self.__initiated = True
            updates = self.__bot.getUpdates(offset = None)
            if updates:
                self.__offset = updates[-1].update_id + 1
            print self.__offset
            self.__listen_loop()
        else:
            raise Exception('Bot already active')


    def __listen_loop(self):
        print 'listen loop'
        # add all unhandled messages to queue
        updates = self.__bot.getUpdates(offset=self.__offset)
        if updates:
                self.__offset = updates[-1].update_id + 1
                for u in updates:
                    self.__message_queue.append(u.message)
        print self.__message_queue


        # handle all messages in queue
        while self.__message_queue:
            message = self.__message_queue.popleft()
            command_and_params = message.text.split()
            if command_and_params[0] in self.__commands:
                self.__commands[command_and_params[0]](message.things, command_and_params[1:])
            else:
                print 'skipped command %s, not supported' % command_and_params[0]
                self.send_message(message.chat_id, self.__bad_usage_message)

        # call self
        threading.Timer(self.__timer, self.__listen_loop).start()

def main():
    bot = Bot(token = '113022701:AAHsn9FiQoHHKIZ4b4OpLekFXTKZOc34lfs', timer = 1)
    bot.activate()


if __name__ == "__main__":
    main()