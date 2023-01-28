from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, Float, ARRAY
from sqlalchemy.sql.expression import text
from app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.ext.mutable import MutableList




class BookTicket(Base):
    '''
    defines the table where the user 
    will be booking travel 

    '''
    __tablename__ = "book_ticket_tbl"

    ticket_id = Column(Integer, primary_key = True, nullable = False)
    leaving_from = Column(String, nullable = False)
    going_to = Column(String, nullable = False)
    travel_status = Column(String, nullable = False, server_default = 'upcoming')
    travel_type = Column(String, nullable = False, server_default = 'oneway')
    is_paid = Column(Boolean, nullable = False, server_default = 'FALSE')
    seat_no = Column(String, nullable = False)
    travel_date = Column(TIMESTAMP(timezone = True), nullable = True)
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'))
    passenger_id = Column(Integer, ForeignKey('users_tbl.user_id', ondelete="CASCADE"), nullable = False)
    passenger = relationship("User")
    bus_id = Column(Integer, ForeignKey('bus_tbl.bus_id', ondelete='CASCADE'), nullable = False)
    bus = relationship('Bus')






class User(Base):
    '''
    users specifically passengers who will be travelling upon booking a ticket 

    '''
    __tablename__ = "users_tbl"

    user_id =  Column(Integer, primary_key = True, nullable = False)
    email = Column(String , nullable = False, unique =  True )
    first_name = Column(String, nullable = True)
    last_name = Column(String, nullable = True)
    phone_number = Column(String, nullable = True)
    password = Column(String, nullable = False)
    is_passenger = Column(Boolean, nullable = False, server_default = 'TRUE')
    is_admin = Column(Boolean, nullable = False, server_default = 'False')
    created_at =  Column (TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'))




class TravelRoute(Base):
    '''
    define a route for a specifific bus eg a specific bus travels from nairobi to mombasa 
    Admin capabilities 


    '''
    __tablename__ = "travel_route_tbl"
    route_id = Column(Integer, primary_key = True, nullable = False)
    leaving_from = Column(String, nullable = False)
    going_to = Column(String, nullable = False)
    price = Column(Float, nullable = False)
    user_id = Column(Integer, ForeignKey('users_tbl.user_id', ondelete='CASCADE'), nullable = False)
    user = relationship('User')
    


class Bus(Base):
    '''
    Admin at fast coach will be  registering new buses 

    '''
    __tablename__ = "bus_tbl"
    bus_id = Column(Integer, primary_key = True, nullable = False)
    bus_name = Column(String, nullable = False)
    no_of_seats = Column(Integer, nullable = False)
    bus_capacity = Column(Integer, nullable = False)
    seat_arrangement = Column(String, nullable = False)
    route_id = Column(Integer, ForeignKey('travel_route_tbl.route_id', ondelete="CASCADE"), nullable = False)
    route = relationship('TravelRoute')
    user_id = Column(Integer, ForeignKey('users_tbl.user_id', ondelete='CASCADE'), nullable = False)
    user = relationship('User')






class Payments(Base):
    __tablename__ = "payments_tbl"
    '''
    payments 
    ----------------
    one to one relationship to bus tickets 
    many to one relaationship to users 

    '''
    payment_id = Column(Integer, primary_key = True, nullable = False)
    amount = Column(Float, nullable = False)
    is_payment_succesfull = Column(Boolean, nullable = False,server_default = 'FALSE')
    user_id = Column(Integer, ForeignKey('users_tbl.user_id', ondelete="CASCADE"), nullable = False)
    passenger = relationship('User')
    ticket_id = Column(Integer, ForeignKey('book_ticket_tbl.ticket_id', ondelete="CASCADE"), nullable = False, unique = True)
    booking = relationship('BookTicket', uselist = False, backref = 'payaments_tbl')
    paid_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'))

    



class Driver (Base):
    '''
    assign each driver a bus -> one to one relationship 

    '''
    __tablename__ = 'driver_tbl'
    driver_id =  Column(Integer, nullable = False, primary_key = True)
    first_name = Column(String, nullable = False)
    last_name = Column(String, nullable = False)
    phone_number = Column(String, nullable = False)
    bus_id = Column(Integer, ForeignKey('bus_tbl.bus_id'), nullable = False, unique = True)
    bus = relationship('Bus', uselist =  False)



class BookedSeats(Base):
    '''
    track the booked seats in each bus 
    the bus_id is unique but the list for each bus is upated once a passenger books  a seat 
    '''
    __tablename__ = 'bookedseats_tbl'
    seats_id = Column(Integer, primary_key = True, nullable = False)
    bus_id = Column(Integer, ForeignKey('bus_tbl.bus_id'), nullable = False, unique = True)
    bus = relationship('Bus', uselist =  False, backref = 'bookedseats_tbl')
    booked_seats = Column(MutableList.as_mutable(ARRAY(String)), nullable = False)

class Depature(Base):
    '''
    This table tracks the buses that are moving out that day 
    Admin will add the buses that will be leaving at a particular date 

    '''
    __tablename__ = 'depature_tbl'
    dep_id = Column(Integer, primary_key = True, nullable = False)
    bus_id = Column(Integer, ForeignKey('bus_tbl.bus_id'), nullable = False)
    route_id = Column(Integer, ForeignKey('travel_route_tbl.route_id'), nullable = False)
    route = relationship('TravelRoute')
    bus = relationship('Bus')
    depature_time = Column(TIMESTAMP(timezone = True), nullable = True)
