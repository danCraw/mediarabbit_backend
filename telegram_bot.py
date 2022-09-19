from dataclasses import dataclass

from telebot import TeleBot


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