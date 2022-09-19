#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2
from http import HTTPStatus
from flask import Flask, jsonify, request
from flask_cors import CORS
from psycopg2.extras import RealDictCursor
from pydantic import ValidationError

from telegram_bot import MyBot
from SwaggerDoc.generate_doc import generate_dock
from models import Customer
from connection import conn
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_url_path='')

cors = CORS(app, support_credentials=True, resources={r'/api/*': {"origins": "*"}})

bot = MyBot(os.environ.get('BOT_TOKEN'))


@app.route('/api/customers', methods=['POST'])
def add_customer():
    try:
        customer = Customer.parse_obj(request.get_json())
    except ValidationError as e:
        return e

    cur = conn.cursor()
    cur.execute('''INSERT INTO customers (email, phone, name, bid_type)
                   VALUES (%s, %s, %s, %s);''', (customer.email, customer.phone,
                                                customer.name, customer.bid_type))
    conn.commit()
    cur.close()
    bid_type_map = {
        0: 'Разработка сайтов',
        1: 'Разработка телеграм бота',
        2: 'Дизайн'
    }
    bot.send_message(f'У вас новый заказ от {customer.name}, контакты: {customer.email} {customer.phone}, услуга: {bid_type_map.get(customer.bid_type)}')
    return 'customer added', HTTPStatus.OK


@app.route('/api/customers', methods=['GET'])
def get_customers():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM customers;')
    response = []
    for c in cur.fetchall():
        response.append(dict(c))
    cur.close()
    bot.send_message('пользователи')
    return jsonify(response), HTTPStatus.OK


@app.route('/api/customers/<id>', methods=['GET'])
def get_customer_by_id(id: int):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('''SELECT * FROM customers WHERE id = %s;''', id)
    return jsonify(cur.fetchone()), HTTPStatus.OK


@app.route('/api/customer_by_phone/<phone>', methods=['GET'])
def get_customer_by_phone(phone: str):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('''SELECT * FROM customers WHERE phone = %s;''', phone)
    return jsonify(cur.fetchone()), HTTPStatus.OK


@app.route('/api/customers/<id>', methods=['DELETE'])
def delete_customer():
    cur = conn.cursor()
    cur.execute('''DELETE FROM customers WHERE id = %s;''', request.get_json()['id'])
    conn.commit()
    cur.close()
    return 'customer deleted', HTTPStatus.OK


if __name__ == '__main__':
    generate_dock(app)
    bot.add_user_to_send(677000194)
    # bot.add_user_to_send(792137742)
    app.run(debug=False)
