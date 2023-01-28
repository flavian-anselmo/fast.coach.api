from typing import List
from fastapi import APIRouter
from sqlalchemy.orm import session
from app.database import get_db
from fastapi import Depends, HTTPException, status
from app import models, schemas, oauth2
from app.africas_talking import SMS, PaymentService





router = APIRouter(
  
    prefix = '/payments',
    tags = ['payments']
)






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

  
        







async def payment_process_via_africans_talking(db, curr_user_id:int, ticket_id:int, amount:float):
    '''
    - actual payment process initation 
    - (stkpush via africas_talking api)

    '''
    try:
        user = db.query(models.User).filter(models.User.user_id == curr_user_id).first()
        if user:
            await PaymentService().checkout(
                productName = 'Fast.Coach.API',
                phoneNumber = user.phone_number,
                currencyCode = 'KES',
                amount = amount
            )
            await notify_passenger_via_sms(
                db,
                curr_user_id,
            )
            await change_paid_status(
                db,
                ticket_id,
            )
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))






# -------------------------[Payment Endpoint]------------------------------------
@router.post('/stkpush', response_model=schemas.PaymentResponse)
async def pay_for_ticket(payament:schemas.PaymentCreate, db:session = Depends(get_db), curr_user = Depends(oauth2.get_current_user_logged_in)):
    '''
    - initiate payment with africas talking stkpush  
    - After payments are successfull a message is sent to the passenger notifying them of the booking 

    '''
    try:
        pay = models.Payments( **payament.dict(), user_id = curr_user.user_id)
     

        ''' initiate payment '''
        await payment_process_via_africans_talking(
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