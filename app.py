from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import psycopg2
import psycopg2.extras
import os

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)

def get_db():
    return psycopg2.connect(
        host='localhost',
        port=5432,
        database='practika',
        user='postgres',
        password='1234',
        cursor_factory=psycopg2.extras.RealDictCursor
    )

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/masters')
def get_masters():
    db = get_db()
    cur = db.cursor()
    cur.execute('SELECT * FROM masters')
    data = cur.fetchall()
    cur.close()
    db.close()
    return jsonify(data)

@app.route('/api/categories')
def get_categories():
    db = get_db()
    cur = db.cursor()
    cur.execute('SELECT * FROM service_categories')
    data = cur.fetchall()
    cur.close()
    db.close()
    return jsonify(data)

@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    client_name = request.args.get('client_name')
    db = get_db()
    cur = db.cursor()
    
    if client_name:
        cur.execute('SELECT id, client_name, master_id, booking_date, booking_time::text, price, is_deleted FROM bookings WHERE client_name = %s ORDER BY id DESC', (client_name,))
    else:
        cur.execute('SELECT id, client_name, master_id, booking_date, booking_time::text, price, is_deleted FROM bookings ORDER BY id DESC')
    
    data = cur.fetchall()
    cur.close()
    db.close()
    return jsonify(data)

@app.route('/api/bookings', methods=['POST'])
def create_booking():
    data = request.json
    db = get_db()
    cur = db.cursor()
    cur.execute('''
        INSERT INTO bookings (client_name, master_id, booking_date, booking_time, price)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
    ''', (data['client_name'], data['master_id'], data['booking_date'], data['booking_time'], data['price']))
    new_id = cur.fetchone()['id']
    db.commit()
    cur.close()
    db.close()
    return jsonify({'id': new_id}), 201

@app.route('/api/bookings/<int:booking_id>', methods=['PUT'])
def update_booking(booking_id):
    data = request.json
    db = get_db()
    cur = db.cursor()
    cur.execute('UPDATE bookings SET price = %s WHERE id = %s', (data['price'], booking_id))
    db.commit()
    cur.close()
    db.close()
    return jsonify({'message': 'OK'})

@app.route('/api/bookings/<int:booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    db = get_db()
    cur = db.cursor()
    cur.execute('UPDATE bookings SET is_deleted = TRUE WHERE id = %s', (booking_id,))
    db.commit()
    cur.close()
    db.close()
    return jsonify({'message': 'Deleted'})

@app.route('/api/bookings/<int:booking_id>/versions', methods=['GET'])
def get_versions(booking_id):
    db = get_db()
    cur = db.cursor()
    cur.execute('''
        SELECT version, price, changed_at, change_type, is_current 
        FROM bookings_history 
        WHERE booking_id = %s 
        ORDER BY version DESC
    ''', (booking_id,))
    data = cur.fetchall()
    cur.close()
    db.close()
    
    for row in data:
        if 'changed_at' in row and row['changed_at']:
            row['changed_at'] = str(row['changed_at'])
    
    return jsonify(data)

@app.route('/api/bookings/<int:booking_id>/versions/<int:version>', methods=['GET'])
def get_booking_version(booking_id, version):
    db = get_db()
    cur = db.cursor()
    cur.execute('''
        SELECT * FROM bookings_history 
        WHERE booking_id = %s AND version = %s
    ''', (booking_id, version))
    data = cur.fetchone()
    cur.close()
    db.close()
    
    if data and 'changed_at' in data and data['changed_at']:
        data['changed_at'] = str(data['changed_at'])
    
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
