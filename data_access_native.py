# data_access_native.py
import psycopg2
import psycopg2.extras
from data_access_interface import DataAccessInterface

class NativeSQLDataAccess(DataAccessInterface):
    
    def _get_db(self):
        return psycopg2.connect(
            host='localhost',
            port=5432,
            database='practika',
            user='postgres',
            password='1234',
            cursor_factory=psycopg2.extras.RealDictCursor
        )
    
    def get_masters(self):
        db = self._get_db()
        cur = db.cursor()
        cur.execute('SELECT * FROM masters WHERE is_deleted = FALSE')
        data = cur.fetchall()
        cur.close()
        db.close()
        return data
    
    def get_categories(self):
        db = self._get_db()
        cur = db.cursor()
        cur.execute('SELECT * FROM service_categories')
        data = cur.fetchall()
        cur.close()
        db.close()
        return data
    
    def get_bookings(self, client_name=None, master_id=None, date_from=None, date_to=None):
        db = self._get_db()
        cur = db.cursor()
        
        query = 'SELECT * FROM bookings WHERE is_deleted = FALSE'
        params = []
        
        if client_name:
            query += ' AND client_name = %s'
            params.append(client_name)
        if master_id:
            query += ' AND master_id = %s'
            params.append(master_id)
        if date_from:
            query += ' AND booking_date >= %s'
            params.append(date_from)
        if date_to:
            query += ' AND booking_date <= %s'
            params.append(date_to)
            
        query += ' ORDER BY id DESC'
        
        cur.execute(query, params)
        data = cur.fetchall()
        cur.close()
        db.close()
        return data
    
    def get_booking_by_id(self, booking_id):
        db = self._get_db()
        cur = db.cursor()
        cur.execute('SELECT * FROM bookings WHERE id = %s AND is_deleted = FALSE', (booking_id,))
        data = cur.fetchone()
        cur.close()
        db.close()
        return data
    
    def create_booking(self, client_name, master_id, booking_date, booking_time, price):
        db = self._get_db()
        cur = db.cursor()
        cur.execute('''
            INSERT INTO bookings (client_name, master_id, booking_date, booking_time, price)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        ''', (client_name, master_id, booking_date, booking_time, price))
        new_id = cur.fetchone()['id']
        db.commit()
        cur.close()
        db.close()
        return new_id
    
    def update_booking_price(self, booking_id, new_price):
        db = self._get_db()
        cur = db.cursor()
        cur.execute('UPDATE bookings SET price = %s WHERE id = %s', (new_price, booking_id))
        db.commit()
        cur.close()
        db.close()
        return True
    
    def delete_booking(self, booking_id):
        """Логическое удаление"""
        db = self._get_db()
        cur = db.cursor()
        cur.execute('UPDATE bookings SET is_deleted = TRUE WHERE id = %s', (booking_id,))
        db.commit()
        cur.close()
        db.close()
        return True
    
    def get_booking_versions(self, booking_id):
        db = self._get_db()
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
        return data
    
    def get_booking_version(self, booking_id, version):
        db = self._get_db()
        cur = db.cursor()
        cur.execute('''
            SELECT * FROM bookings_history 
            WHERE booking_id = %s AND version = %s
        ''', (booking_id, version))
        data = cur.fetchone()
        cur.close()
        db.close()
        return data