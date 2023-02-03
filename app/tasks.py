from celery import  Celery
from celery.utils.log import get_task_logger
from app import models
from sqlalchemy.orm import session
from datetime import datetime
import pytz


from app.database import SessionLocal





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
def change_travel_status_to_past():
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
 

    db = SessionLocal()

    tickets = db.query(models.BookTicket).all()

    for ticket in tickets:
        if ticket.travel_date < datetime.utcnow().replace(tzinfo=pytz.UTC):
            celery_log.info('compare dates')
            ticket.travel_status = 'past'
    db.commit()
    celery_log.info('Updated all rows succesfully')


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # session instance 
    sender.add_periodic_task(60.0, change_travel_status_to_past.s())