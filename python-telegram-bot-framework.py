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
    __bad_usage_message = 'Unrecognized command - %s.'
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

    def send_message(self, chat_id, message, markup=None):
        if not markup:
            markup = telegram.ReplyKeyboardHide
        self.__bot.sendMessage(chat_id, message, reply_markup=markup)

    def wait_for_message(self, chat_id, timeout=5):
        #check in queue
        for msg in self.__message_queue:
            if msg.chat_id == chat_id:
                self.__message_queue.remove(msg)
                return msg, msg.text

        #check for updates
        updates = self.__bot.getUpdates(offset=self.__offset)
        time_passed = 1
        update_rcvd = chat_id in [u.message.chat_id for u in updates]
        while not update_rcvd and time_passed <= timeout:
            time.sleep(SLEEP_TIME_STEP)
            time_passed += SLEEP_TIME_STEP
            updates = self.__bot.getUpdates(offset=self.__offset)
            update_rcvd = chat_id in [u.message.chat_id for u in updates]

        message = None

        if update_rcvd:
            ind = [u.message.chat_id for u in updates].index(chat_id)
            message = updates[ind].message
            self.__offset = updates[ind].update_id + 1
            self.__enqueue_updates(updates[:ind])

        return message, message.text

    def __enqueue_updates(self, updates):
        for u in updates:
            self.__message_queue.append(u.message)


    def add_command(self, cmd_name, cmd_cb, cmd_description = None):
        self.__commands[cmd_name] = (cmd_cb, cmd_description)

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
                self.__enqueue_updates(updates)
        print self.__message_queue


        # handle all messages in queue
        while self.__message_queue:
            message = self.__message_queue.popleft()
            command_and_params = message.text.split()
            if command_and_params[0] in self.__commands:
                self.__commands[command_and_params[0]][0](message, message.text[message.text.find(' '):] if len(command_and_params) > 1 else None)
            else:
                print 'skipped command %s, not supported' % command_and_params[0]
                self.send_message(message.chat_id, self.__bad_usage_message % command_and_params[0])

        # call self
        threading.Timer(self.__timer, self.__listen_loop).start()



def main():
    global bot
    bot = Bot(token = '113022701:AAHsn9FiQoHHKIZ4b4OpLekFXTKZOc34lfs', timer = 1)
    bot.add_command(cmd_name='/cmd', cmd_cb=callback)
    bot.activate()

def callback(message, params):
    if not params:
        bot.send_message(chat_id=message.chat_id, message='wrong params %s, put in number - ' % message.chat.first_name)
        msg, params = bot.wait_for_message(chat_id=message.chat_id, timeout=10)

    if not params:
        params = 'none'
    print 'params - ', params
    bot.send_message(chat_id=message.chat_id, message='%s ? kthxbye' % params)



if __name__ == "__main__":
    main()