# data_access_interface.py
from abc import ABC, abstractmethod

class DataAccessInterface(ABC):
    """Единый интерфейс для всех модулей доступа к данным"""
    
    @abstractmethod
    def get_masters(self):
        pass
    
    @abstractmethod
    def get_categories(self):
        pass
    
    @abstractmethod
    def get_bookings(self, client_name=None, master_id=None, date_from=None, date_to=None):
        pass
    
    @abstractmethod
    def get_booking_by_id(self, booking_id):
        pass
    
    @abstractmethod
    def create_booking(self, client_name, master_id, booking_date, booking_time, price):
        pass
    
    @abstractmethod
    def update_booking_price(self, booking_id, new_price):
        pass
    
    @abstractmethod
    def delete_booking(self, booking_id):  # логическое удаление
        pass
    
    @abstractmethod
    def get_booking_versions(self, booking_id):
        pass
    
    @abstractmethod
    def get_booking_version(self, booking_id, version):
        pass