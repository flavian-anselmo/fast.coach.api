from celery import  Celery
from celery.utils.log import get_task_logger

celery_log = get_task_logger(__name__)



celery_app = Celery(
    'app',
    broker = 'amqp://papa:admin@localhost:5672',
    #backend = 'rabbitmq'
    incude=["app.tasks"]
)



@celery_app.task
def add(x:int, y:int):
    import time
    time.sleep(5)
    res = x + y
    celery_log.info(f"Order Complete!")
    return {"message":f"then answ is {res}"}