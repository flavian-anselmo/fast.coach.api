from celery import  Celery
from celery.utils.log import get_task_logger
from celery import shared_task
from fastapi import HTTPException, status
from app import models
from datetime import datetime
import pytz
from app.africas_talking import SMS, PaymentService


from app.database import SessionLocal





celery_log = get_task_logger(__name__)



celery_app = Celery(
    'app',
    broker = 'amqp://guest:guest@localhost:5672',
    #backend = 'rabbitmq'
    incude=["app.tasks"]
)



@shared_task
def add(x:int, y:int):
    ''' test ⛑️'''
    import time
    time.sleep(5)
    res = x + y
    celery_log.info(f"Order Complete!")
    return {"message":f"then answ is {res}"}




@celery_app.task
def change_travel_status_to_past():
    '''
    ------------------
    run every midnight 🔥
    -------------------
    if travel_date < date.now:
        // the travel date passed 
        upcoming --> past
    else 
        // do nothing
    '''
 

    db = SessionLocal()

    tickets = db.query(models.BookTicket).all()

    for ticket in tickets:
        if ticket.travel_date < datetime.utcnow().replace(tzinfo=pytz.UTC):
            ticket.travel_status = 'past'
    db.commit()
    celery_log.info('Updated all rows succesfully')
@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(60.0, change_travel_status_to_past.s())

@celery_app.task
def notify_passenger_via_sms( curr_user_id:int):
    '''
    - after the user has paid notify them via sm 
    - Notify them if the payment was succesfull or not 
    - if no -> then retyr the process after 5 minutes as a background task 
    ✉️
    '''
    db = SessionLocal()

    user = db.query(models.User).filter(models.User.user_id == curr_user_id).first()
    if user:
        sms_response = SMS().send_sms(
            recipient=[user.phone_number],
            msg= f'Hello {user.last_name}, thanks for booking with fastcoach!'
        )
        print(sms_response)
    return {"detail":"wait a message is being sent"}