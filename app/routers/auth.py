from fastapi import APIRouter,Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import session
from app import schemas, models, schemas, utils,oauth2
from app.database import get_db



router = APIRouter(
    prefix='/login',
    tags=['Authentication']
)



@router.post('/', response_model = schemas.TokenResponse)
async def login(user_creds: OAuth2PasswordRequestForm = Depends(), db:session = Depends(get_db)):
    '''
    compare the emails too check whether they match 
    if yes we have a user .. if no we have invalid creds 
    '''
    try:

        user = db.query(models.User).filter(models.User.email == user_creds.username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credentials')
        if not utils.verify_password(user_creds.password, user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credentials')

        '''push the user_id as the payload'''
        access_token = oauth2.create_access_token(payload = {"user_id": user.user_id})
        # return the accesstoken 
        login_data =  {
            "access_token": access_token,
            "type": "Bearer"
        } 
        return  login_data
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

