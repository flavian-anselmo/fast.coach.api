from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, PositiveFloat, validator
from sqlalchemy import Enum

class UserCreate(BaseModel):
    email:EmailStr
    password:str 
    first_name:str
    last_name:str
    phone_number:str
    is_passenger:bool
    is_admin:bool
    
    
    


class UserResponse(BaseModel):
    user_id :int
    email: EmailStr
    is_passenger:bool
    is_admin:bool
    created_at:datetime
    class Config:
        orm_mode = True



class TokenResponse(BaseModel):
    access_token:str
    type:str
    class Config:        
        orm_mode = True
    
class TokenPayLoad(BaseModel):

    user_id:int




class TravelRouteCreate(BaseModel):
    leaving_from: str
    going_to: str 
    price: PositiveFloat
class TravelRouteResponse(TravelRouteCreate):
    route_id:int 

    class Config:
        orm_mode = True
  




class BusCreate(BaseModel):
    user_id:int 
    route_id: int
    bus_name: str
    no_of_seats: int 
    bus_capacity: int
    seat_arrangement: str


class BusResponse(BusCreate):
    bus_id:int 
    route_id:int 
    user_id:int 
    route: TravelRouteResponse
    class Config:
        orm_mode = True




class TravelStatus(str, Enum):
    upcoming = 'upcoming'
    past = 'past'






class BookTicketCreate(BaseModel):
    passenger_id:int 
    bus_id: int  
    leaving_from: str
    travel_date:datetime
    going_to:str
    seat_no: str
    travel_type:str
    travel_status: TravelStatus

class BookTicketResponse(BookTicketCreate):
    is_paid:bool
    travel_status:TravelStatus
    bus: BusResponse
    passenger:UserResponse
    class Config:
        orm_mode = True





class PaymentCreate(BaseModel):
    ticket_id: int 
    amount:PositiveFloat

class PaymentResponse(PaymentCreate):
    user_id:int 
    class Config:
        orm_mode = True







class DriverCreate(BaseModel):
    bus_id:int
    first_name:str
    last_name:str
    phone_number:str

    # @validator('phone_number')
    # def validate_phone_number():
    #     '''
    #     validate that the phone number is kenyan 
    #     +2547xxxxxxxx
    #     the length must be 
    #     '''
    #     return ''



class DriverResponse(DriverCreate):
    bus: BusResponse
    class Config:
        orm_mode = True






class BookedSeatsCreate(BaseModel):
    bus_id:int 
    booked_seats:list[str]
class BookedSeatsResponse(BookedSeatsCreate):
    class Config:
        orm_mode = True    






class DepatureCreate(BaseModel):
    bus_id:int 
    route_id: int
    depature_time:datetime    

class DepatureResponse(DepatureCreate):
    bus:BusResponse
    class Config:
        orm_mode = True

