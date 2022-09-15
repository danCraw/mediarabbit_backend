import psycopg2
from http import HTTPStatus
from flask import Flask, jsonify, request
from flask_cors import CORS
from psycopg2.extras import RealDictCursor

import telegram_bot
from SwaggerDoc.generate_doc import generate_dock
from models import Customer
from connection import conn
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_url_path='')

cors = CORS(app, support_credentials=True, resources={r'/api/*': {"origins": "*"}})


@app.route('/api/customer', methods=['POST'])
def add_customer():
    try:
        customer = Customer.parse_obj(request.get_json())
    except Exception as e:
        return e

    cur = conn.cursor()
    cur.execute('''INSERT INTO customers (email, phone, name, bid_type)
                   VALUES (%s, %s, %s, %s);''', (customer.email, customer.phone,
                                                customer.name, customer.bid_type))
    conn.commit()
    cur.close()
    bot.send_message('У вас новый заказ')
    return 'customer added', HTTPStatus.OK


@app.route('/api/customer', methods=['GET'])
def get_customers():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM customers;')
    response = []
    for c in cur.fetchall():
        response.append(dict(c))
    cur.close()
    return jsonify(response), HTTPStatus.OK


@app.route('/api/customer/<id>', methods=['GET'])
def get_customer_by_id(id: int):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('''SELECT * FROM customers WHERE id = %s;''', id)
    return jsonify(cur.fetchone()), HTTPStatus.OK


@app.route('/api/customer_by_phone/<phone>', methods=['GET'])
def get_customer_by_phone(phone: str):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('''SELECT * FROM customers WHERE phone = %s;''', phone)
    return jsonify(cur.fetchone()), HTTPStatus.OK


@app.route('/api/customers', methods=['DELETE'])
def delete_customer():
    cur = conn.cursor()
    cur.execute('''DELETE FROM customers WHERE id = %s;''', request.get_json()['id'])
    conn.commit()
    cur.close()
    return 'customer deleted', HTTPStatus.OK


if __name__ == '__main__':
    generate_dock(app)
    bot = telegram_bot.MyBot(os.environ.get('BOT_TOKEN'))
    bot.add_user_to_send(677000194)
    app.run(debug=False, port=5000)
