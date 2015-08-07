import telegram
import time
import threading
import re
from collections import deque


class Bot:
    __message_queue = deque([])
    __initiated = False
    __offset = None
    timer = 10
    commands = {} #name : (cb, params, description)
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

    def wait_for_message(self, chat_id, timeout):
        pass

    def add_command(self, cmd_name, cmd_description, cmd_params, cmd_cb):
        pass

    def activate(self):
        if not self.__initiated:
            self.__initiated = True
            updates = self.bot.getUpdates(offset = None)
            if updates:
                self.__offset = updates[-1].update_id + 1
            print self.__offset
            self.__listen_loop()
        else:
            raise Exception('Bot already active')


    def __listen_loop(self):
        print 'listen loop'
        # add all unhandled messages to queue
        updates = self.bot.getUpdates(offset=self.__offset)
        if updates:
                self.__offset = updates[-1].update_id + 1
                for u in updates:
                    self.__message_queue.append(u.message)
        print self.__message_queue


        # handle all messages in queue
        while self.__message_queue:
            message = self.__message_queue.popleft()
            command_and_params = message.text.split()
            if command_and_params[0] in self.commands:
                self.commands[command_and_params[0]](message.things, command_and_params[1:])
            else:
                print 'skipped command %s, not supported' % command_and_params[0]
                self.send_message(message.chat_id, self.bad_usage_message)

        # call self
        threading.Timer(self.timer, self.__listen_loop).start()

def main():
    bot = Bot(token = '113022701:AAHsn9FiQoHHKIZ4b4OpLekFXTKZOc34lfs', timer = 1)
    bot.activate()


if __name__ == "__main__":
    main()