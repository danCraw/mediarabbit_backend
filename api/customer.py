import psycopg2
from daiquiri import getLogger
from main import app, bot
from customer import Customer
from dataBase.connection import conn
from openpyxl.cell.cell import TYPE_ERROR
from psycopg2.errorcodes import UNIQUE_VIOLATION, UNDEFINED_TABLE
from flask import jsonify, request, Response
from psycopg2 import errors
from psycopg2.extras import RealDictCursor
from pydantic import ValidationError
from http import HTTPStatus


logger = getLogger(__name__)


@app.route('/api/customers', methods=['POST'])
def add_customer():
    try:
        customer = Customer.parse_obj(request.get_json())
    except ValidationError as e:
        logger.warning(f'error in added customer {e}')
        return 'validation error', HTTPStatus.BAD_GATEWAY
    try:
        cur = conn.cursor()
        cur.execute('''INSERT INTO customers (email, phone, name, bid_type)
                       VALUES (%s, %s, %s, %s);''', (customer.email, customer.phone,
                                                    customer.name, customer.bid_type))
        conn.commit()
        cur.close()
    except errors.lookup(UNIQUE_VIOLATION) as e:
        logger.warning(f'error in added customer {e}')
        return f'customer not added {e}', HTTPStatus.BAD_GATEWAY
    bid_type_map = {
        0: 'Разработка сайтов',
        1: 'Разработка телеграм бота',
        2: 'Дизайн'
    }
    bot.send_message(f'У вас новый заказ от {customer.name}, контакты: {customer.email} {customer.phone}, услуга: {bid_type_map.get(customer.bid_type)}')
    return 'customer added', HTTPStatus.OK


@app.route('/api/customers', methods=['GET'])
def get_customers() -> tuple[str, int] | tuple[Response, int]:
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cur.execute('SELECT * FROM customers;')
    except errors.lookup(UNDEFINED_TABLE) as e:
        logger.warning(f'error in getting customers {e}')
        return f'request error {e}', HTTPStatus.BAD_GATEWAY
    response = []
    for c in cur.fetchall():
        response.append(dict(c))
    return jsonify(response), HTTPStatus.OK


@app.route('/api/customers/<id>', methods=['GET'])
def get_customer_by_id(id: int) -> tuple[str, int] | tuple[Response, int]:
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cur.execute('''SELECT * FROM customers WHERE id = %s;''', id)
    except errors.lookup(TYPE_ERROR) as e:
        logger.warning(f'error in getting customer by id {e}')
        return f'get by id request error {e}', HTTPStatus.BAD_GATEWAY
    return jsonify(dict(cur.fetchone())), HTTPStatus.OK


@app.route('/api/customer_by_phone/<phone>', methods=['GET'])
def get_customer_by_phone(phone: str):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cur.execute('''SELECT * FROM customers WHERE phone = %s;''', phone)
        cur.close()
    except errors.lookup(UNDEFINED_TABLE) as e:
        logger.warning(f'error in getting customer by phone {e}')
        return f'get by phone request error {e}', HTTPStatus.BAD_GATEWAY
    return jsonify(dict(cur.fetchone())), HTTPStatus.OK


@app.route('/api/customers/<id>', methods=['DELETE'])
def delete_customer():
    cur = conn.cursor()
    try:
        cur.execute('''DELETE FROM customers WHERE id = %s;''', request.get_json()['id'])
        conn.commit()
        cur.close()
    except psycopg2.errors as e:
        logger.warning(f'error in deleting customer {e}')
        return f'delete request error {e}', HTTPStatus.BAD_GATEWAY
    return 'customer deleted', HTTPStatus.OK