import os
from flask import Flask
from flask_cors import CORS
from SwaggerDoc.generate_doc import generate_dock

from dotenv import load_dotenv

from TelegramBot.bot import MyBot

load_dotenv()

app = Flask(__name__, static_url_path='')

bot = MyBot(os.environ.get('BOT_TOKEN'))

cors = CORS(app, support_credentials=True, resources={r'/api/*': {"origins": "*"}})


if __name__ == '__main__':
    generate_dock(app)
    bot.add_user_to_send(677000194)
    app.run(debug=False)
