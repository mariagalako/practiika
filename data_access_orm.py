# data_access_orm.py
from models import db, Master, ServiceCategory, Booking, BookingHistory
from data_access_interface import DataAccessInterface
from datetime import datetime

class ORMDataAccess(DataAccessInterface):
    
    def get_masters(self):
        return Master.query.all()
    
    def get_categories(self):
        return ServiceCategory.query.all()
    
    def get_bookings(self, client_name=None, master_id=None, date_from=None, date_to=None):
        query = Booking.query.filter_by(is_deleted=False)
        
        if client_name:
            query = query.filter_by(client_name=client_name)
        if master_id:
            query = query.filter_by(master_id=master_id)
        if date_from:
            query = query.filter(Booking.booking_date >= date_from)
        if date_to:
            query = query.filter(Booking.booking_date <= date_to)
            
        return query.order_by(Booking.id.desc()).all()
    
    def get_booking_by_id(self, booking_id):
        return Booking.query.filter_by(id=booking_id, is_deleted=False).first()
    
    def create_booking(self, client_name, master_id, booking_date, booking_time, price):
        booking = Booking(
            client_name=client_name,
            master_id=master_id,
            booking_date=booking_date,
            booking_time=booking_time,
            price=price
        )
        db.session.add(booking)
        db.session.commit()
        
        # Создать начальную версию в истории
        history = BookingHistory(
            booking_id=booking.id,
            version=1,
            client_name=client_name,
            master_id=master_id,
            price=price,
            booking_date=booking_date,
            booking_time=booking_time,
            change_type='CREATE',
            is_current=True
        )
        db.session.add(history)
        db.session.commit()
        
        return booking.id
    
    def update_booking_price(self, booking_id, new_price):
        booking = Booking.query.get(booking_id)
        if not booking:
            return False
        
        old_price = booking.price
        booking.price = new_price
        db.session.commit()
        
        # Триггер сам создаст версию, но для ORM добавим вручную
        # (или полагаемся на триггер в БД)
        return True
    
    def delete_booking(self, booking_id):
        booking = Booking.query.get(booking_id)
        if booking:
            booking.is_deleted = True
            db.session.commit()
            return True
        return False
    
    def get_booking_versions(self, booking_id):
        return BookingHistory.query.filter_by(booking_id=booking_id).order_by(BookingHistory.version.desc()).all()
    
    def get_booking_version(self, booking_id, version):
        return BookingHistory.query.filter_by(booking_id=booking_id, version=version).first()