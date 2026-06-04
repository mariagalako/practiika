# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Master(db.Model):
    __tablename__ = 'masters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    avatar = db.Column(db.String(10), default='cat')
    rating = db.Column(db.Numeric(3,2), default=5.0)
    reviews_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ServiceCategory(db.Model):
    __tablename__ = 'service_categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('service_categories.id'))
    level = db.Column(db.Integer, default=0)
    
    children = db.relationship('ServiceCategory', backref=db.backref('parent', remote_side=[id]))

class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    client_avatar = db.Column(db.String(10), default='cat')
    master_id = db.Column(db.Integer, db.ForeignKey('masters.id'))
    service_category_id = db.Column(db.Integer, db.ForeignKey('service_categories.id'))
    booking_date = db.Column(db.Date, nullable=False)
    booking_time = db.Column(db.Time, nullable=False)
    price = db.Column(db.Integer, default=1500)
    status = db.Column(db.String(20), default='active')
    is_deleted = db.Column(db.Boolean, default=False)  # для логического удаления
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class BookingHistory(db.Model):
    __tablename__ = 'bookings_history'
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, nullable=False)
    version = db.Column(db.Integer, default=1)
    client_name = db.Column(db.String(100))
    master_id = db.Column(db.Integer)
    price = db.Column(db.Integer)
    booking_date = db.Column(db.Date)
    booking_time = db.Column(db.Time)
    change_type = db.Column(db.String(20))
    is_current = db.Column(db.Boolean, default=True)
    changed_at = db.Column(db.DateTime, default=datetime.utcnow)