'''
all endpoints regarding booking of a bus 


get req 
-----------
1. get bookings by status upcoming -- past etc 

2. bookigns are fteched according to logged in user 


'''


from datetime import datetime, timedelta
from typing import List
from fastapi import APIRouter
from sqlalchemy.orm import session
from app.database import get_db
from fastapi import Depends, HTTPException, status
from app import models, schemas, oauth2





router = APIRouter(
  
    prefix = '/ticket',
    tags = ['Book a ticket ']
)

# ------------[reduce number of seats]--------------------------------
async def reduce_no_seats(bus_id:int, db:session):
    ''' 
    reduce the number of seats 

    get the bus id to acess the exact bus 

    '''
    try:
        seat = db.query(models.Bus).filter(models.Bus.bus_id == bus_id).first()
        if seat.no_of_seats != None:

            # if the seats availability is not zero 
            seat.no_of_seats = seat.no_of_seats - 1
            db.commit()
            db.refresh(seat)
            return seat 
        return {'message':'The bus is fully booked'}    
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    

# ---------------------[track seats]--------------------------------------
async def track_seats(bus_id:int, seat_no:str,db:session):
    try:
        bus = db.query(models.BookedSeats).filter(models.BookedSeats.bus_id == bus_id).first()
        if bus:
            # update seat 
            bus.booked_seats.append(seat_no)
            db.commit()
            db.refresh(bus)
        else:
            await create_new_booked_seat(bus_id, seat_no, db)   
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

                 




# -------------------------[create the first booked seat]-----------------
async def create_new_booked_seat(bus_id: int, seat_no:str, db:session):
    try:
        new_booked_seat = models.BookedSeats(bus_id = bus_id, booked_seats = [seat_no]) 
        db.add(new_booked_seat)
        db.commit()
        db.refresh(new_booked_seat)
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED, detail=str(err))   





       
      
# ------------------------------------[book a seat]----------------------------------
@router.post('/book', status_code=status.HTTP_201_CREATED)
async def book_ticket(ticket:schemas.BookTicketCreate,  db:session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user_logged_in)):
    '''
    book a ticket 

    '''
    try:

        new_ticket = models.BookTicket(**ticket.dict())
        seat = db.query(models.Bus).filter(models.Bus.bus_id == ticket.bus_id).first()
        if seat.no_of_seats != None:
            db.add(new_ticket)
            db.commit()
            await reduce_no_seats(
                ticket.bus_id,
                db,
            )
            
            await track_seats(
                ticket.bus_id,
                ticket.seat_no,
                db,
            )
            db.refresh(new_ticket)
            return {'message':'Ticket Booked Successfully'}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='The bus is fully booked')    
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))







@router.get('/book', response_model=List[schemas.BookTicketResponse])
async def get_ticket_booked(db:session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user_logged_in)):
    '''
    only the login user will be able to get a ticket 

    '''
    try:

        ticket = db.query(models.BookTicket).filter(models.BookTicket.passenger_id == curr_user.user_id).all()
        if not ticket:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='ticket not found')
        return ticket    
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    
    

    
@router.get('/bus', response_model=List[schemas.DepatureResponse])
async def get_bus_routes(leaving_from:str, going_to:str, db:session =  Depends(get_db), curr_user:int = Depends(oauth2.get_current_user_logged_in)):
    '''
    get a bus to book with specific filter with travel location 

    - leaving_from (depature)
    - going_to (destination)
    - depature_time (based on the date placed)

    '''
    
    bus_routes_join = db.query(models.Depature).join(models.TravelRoute, models.Depature.route_id == models.TravelRoute.route_id)
    bus_routes =  bus_routes_join.filter(models.TravelRoute.going_to.__eq__(going_to) and models.TravelRoute.leaving_from.__eq__(leaving_from)).all()
    if not bus_routes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='routes not found')
    return bus_routes



# ------------------------------------------------------[SEAT TRACKING]---------------------------------------------------------------------------------------------------------
@router.get('/bookedseats', response_model= List[schemas.BookedSeatsResponse])
async def get_all_booked_seats(db:session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user_logged_in)):
    '''
    get all booked seats     except Exception as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

    '''
    try:

        booked_seats = db.query(models.BookedSeats).all()
        if booked_seats:
            return booked_seats
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail='no booked seats')
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    
 
# ----------------------------------------------[Depature]-------------------------------------------------------------------------------------
@router.get('/depature', response_model= List[schemas.DepatureResponse])
async def get_all_depatures(db:session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user_logged_in)):
    '''
    get all booked seats 

    '''
    try:

        depature = db.query(models.Depature).all()
        if depature:
            return depature
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail='Sorry, we do not have any buses for your selection at the momen')
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    

# --------------------------------------[upcoming travels]------------------------------------------------------------------------------
@router.get('/bookings/upcoming', response_model = List[schemas.BookTicketResponse])
async def get_all_upcoming_travels(db:session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user_logged_in)):
    '''
    get all the upcoming travels 

    '''
    
    upcoming = db.query(models.BookTicket).filter(models.BookTicket.travel_status == schemas.TravelStatus.upcoming).all()
    if not upcoming:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail='No upcoming travels, Kindly Book travel')
    return upcoming
   



# -------------------------------------[past travels]-----------------------------------------------------------------------------
@router.get('/bookings/past', response_model = List[schemas.BookTicketResponse])
async def get_all_past_travels(db:session = Depends(get_db), curr_user = Depends(oauth2.get_current_user_logged_in)):
    '''
    get the travel history of a user 

    '''
    past_travel = db.query(models.BookTicket).filter(models.BookTicket.travel_status == schemas.TravelStatus.past).all()
    if not past_travel:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail='No past travels, Kindly Book travel')
    return past_travel
    

