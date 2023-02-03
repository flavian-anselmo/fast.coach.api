from typing import List
from fastapi import APIRouter
from sqlalchemy.orm import session
from app.database import get_db
from fastapi import Depends, HTTPException, status
from app import models, schemas, oauth2
from app.africas_talking import SMS, PaymentService
from app.tasks import notify_passenger_via_sms
# from app.tasks import change_paid_status, notify_passenger_via_sms, make_payment





router = APIRouter(
  
    prefix = '/payments',
    tags = ['payments']
)






def change_paid_status(db, ticket_id:int):
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









def make_payment(phoneNumber:str, amount:float):
    PaymentService().checkout(
        productName = 'Fast.Coach.API',
        phoneNumber = phoneNumber,
        currencyCode = 'KES',
        amount = amount
    )









def payment_process_via_africans_talking(db, curr_user_id:int, ticket_id:int, amount:float):
    '''
    - actual payment process initation 
    - (stkpush via africas_talking api)

    '''
    user = db.query(models.User).filter(models.User.user_id == curr_user_id).first()
    if user:
            # celery task
        make_payment(
            phoneNumber=user.phone_number,
            amount=amount
        )
            
        # celery task🤹
        notify_passenger_via_sms.delay(
            curr_user_id,
        )
            # celery task 
        change_paid_status(
            db,
            ticket_id,
        )
    return {'message':'Kindly wait as we process your request'}
   






# -------------------------[Payment Endpoint]------------------------------------
@router.post('/stkpush', response_model=schemas.PaymentResponse)
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
        try:
            db.add(pay)
            db.commit()
            db.refresh(pay)
            return pay
        except Exception as error:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(error))
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(error))