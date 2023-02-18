from typing import List
from fastapi import APIRouter
from sqlalchemy.orm import session
from app.database import get_db
from fastapi import Depends, HTTPException, status
from app import models, schemas, oauth2
from app.africas_talking import SMS, PaymentService
from app.tasks import change_paid_status, make_payment, notify_passenger_via_sms
# from app.tasks import change_paid_status, notify_passenger_via_sms, make_payment





router = APIRouter(
    prefix = '/payments',
    tags = ['payments']
)


def payment_process_via_africans_talking(db, curr_user_id:int, ticket_id:int, amount:float):
    '''
    - actual payment process initation 
    - (stkpush via africas_talking api)

    '''
    user = db.query(models.User).filter(models.User.user_id == curr_user_id).first()
    if user:
        # celery task 🚀
        make_payment.delay(
            phoneNumber=user.phone_number,
            amount=amount
        )
            
        # celery task 🤹
        notify_passenger_via_sms.delay(
            curr_user_id,
        )
        # celery task 🦊
        change_paid_status.delay(
            ticket_id,
        )
        return {'message':'Kindly wait as we process your request'}
   






# -------------------------[Payment Endpoint]------------------------------------
@router.post('/stkpush')
def pay_for_ticket(payament:schemas.PaymentCreate, db:session = Depends(get_db), curr_user = Depends(oauth2.get_current_user_logged_in)):
    '''
    - initiate payment with africas talking stkpush  
    - After payments are successfull a message is sent to the passenger notifying them of the booking 

    '''
    try:
        pay = models.Payments( **payament.dict(), user_id = curr_user.user_id)
        ''' initiate payment '''
        payment_process_via_africans_talking(
            db,
            curr_user.user_id,
            payament.ticket_id,
            payament.amount
        )
        db.add(pay)
        db.commit()
        db.refresh(pay)
        return {"message":"Kindly wait as we process your request"}
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(error))