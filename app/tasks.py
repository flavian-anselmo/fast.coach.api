from celery import  Celery
from celery.utils.log import get_task_logger
from fastapi import Depends, HTTPException, status
from app import models
from app.africas_talking import SMS, PaymentService
from sqlalchemy.orm import session
from datetime import datetime



celery_log = get_task_logger(__name__)



celery_app = Celery(
    'app',
    broker = 'amqp://guest:guest@localhost:5672',
    #backend = 'rabbitmq'
    incude=["app.tasks"]
)



@celery_app.task
def add(x:int, y:int):
    ''' test '''
    import time
    time.sleep(5)
    res = x + y
    celery_log.info(f"Order Complete!")
    return {"message":f"then answ is {res}"}




@celery_app.task
async def change_paid_status(db, ticket_id:int):
    '''
    - change the paid status in booking table to paid = True
    - This methos is initiated only when the payment process is succefull 

    '''
    try:
        paid_status = db.query(models.BookTicket).filter(models.BookTicket.ticket_id == ticket_id).first()
        if paid_status.is_paid == False:
            paid_status.is_paid = True
            db.commit()
            db.refresh(paid_status)
            return paid_status.is_paid
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))



@celery_app.task
async def notify_passenger_via_sms(db, curr_user_id:int):
    '''
    - after the user has paid notify them via sm 
    - Notify them if the payment was succesfull or not 
    - if no -> then retyr the process after 5 minutes as a background task 

    '''

    user = db.query(models.User).filter(models.User.user_id == curr_user_id).first()
    if user:
        sms_response = await SMS().send_sms(
            recipient=[user.phone_number],
            msg= f'Hello {user.last_name}, thanks for booking with fastcoach!'
        )
        print(sms_response)
        return sms_response



@celery_app.task
async def make_payment(phoneNumber:str, amount:float):
    await PaymentService().checkout(
        productName = 'Fast.Coach.API',
        phoneNumber = phoneNumber,
        currencyCode = 'KES',
        amount = amount
    )






@celery_app.task
def change_travel_status_to_past(db:session):
    '''
    ------------------
    run every midnight 
    -------------------
    if travel_date < date.now:
        // the travel date passed 
        upcoming --> past
    else 
        // do nothing

    '''

    tickets = db.query(models.BookTicket).all()

    for ticket in tickets:
        if ticket.travel_date < datetime.utcnow():
            ticket.travel_status = 'past'
        db.commit()
        celery_log.info('Updated all rows succesfully')

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(60.0, change_travel_status_to_past.s(db))



