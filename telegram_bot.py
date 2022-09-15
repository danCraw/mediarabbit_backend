from dataclasses import dataclass

from telebot import TeleBot

from main import *


@dataclass
class MyBot:
    bot: TeleBot
    chats: []

    def __init__(self, token):
        self.bot = TeleBot(token)
        self.chats = []

    def send_message(self, message_text):
        for chat in self.chats:
            print('отправлено сообщение'),
            self.bot.send_message(chat, message_text)

    def add_user_to_send(self, user_id):
        self.chats.append(user_id)

    def delete_user_from_sending(self, user_id):
        try:
            self.chats.remove(user_id)
        except ValueError:
            print('user not found')

    def get_all_orders(self):
        print(get_customers)
        for customer in get_customers():
            self.send_message(customer)