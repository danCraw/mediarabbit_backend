import psycopg2
from flask import Flask, jsonify, request
from psycopg2.extras import RealDictCursor

from SwaggerDoc.generate_doc import generate_dock
from models import Customer
from config import conn

app = Flask(__name__, static_url_path='')


@app.route('/api/save_customer', methods=['POST'])
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
    return 'customer added', 200


@app.route('/api/get_customers', methods=['GET'])
def get_customers():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM customers;')
    response = []
    for c in cur.fetchall():
        response.append(dict(c))
    cur.close()
    return jsonify(response), 200


@app.route('/api/get_customer/<id>', methods=['GET'])
def get_customer_by_id(id: int):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('''SELECT * FROM customers WHERE id = %s;''', id)
    return jsonify(cur.fetchone()), 200


@app.route('/api/get_customer/<phone>', methods=['GET'])
def get_customer_by_phone(phone: str):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('''SELECT * FROM customers WHERE phone = %s;''', phone)
    return jsonify(cur.fetchone()), 200


@app.route('/api/delete_customer', methods=['DELETE'])
def delete_customer():
    cur = conn.cursor()
    cur.execute('''DELETE FROM customers WHERE id = %s;''', request.get_json()['id'])
    conn.commit()
    cur.close()
    return 'customer deleted', 200


if __name__ == '__main__':
    generate_dock(app)
    app.run(debug=True, port=8000)
