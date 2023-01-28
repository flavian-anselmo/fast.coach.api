from typing import List
from fastapi import Depends, HTTPException, status, APIRouter
from psycopg2 import IntegrityError
from app import models, schemas, oauth2, utils
from app.database import get_db
from sqlalchemy.orm import session


router = APIRouter(
    prefix = '/users',
    tags =  ['users']
)







@router.post('/', status_code = status.HTTP_201_CREATED, response_model = schemas.UserResponse, description = ' user registration or sign-up')
async def register_user(user:schemas.UserCreate, db: session = Depends(get_db), ):
    '''
    register user into the system -> (passengers)

    '''
    try:
        hash_password  = utils.get_hashed_password(user.password)
        # set the hashed password 
        user.password = hash_password
        new_user = models.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user 
    except:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = f'user with email {user.email} already exists')
   






@router.get('/', description='get all users', response_model = List[schemas.UserResponse])
async def get_all_users(db:session= Depends(get_db), current_user:int  = Depends(oauth2.get_current_user_logged_in), ):
    '''
    get all the users  registered in the system 

    '''
    try:

        _user = db.query(models.User).all()
        if not _user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='no users registered')
        return _user
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    




@router.get('/{user_id}', status_code = status.HTTP_200_OK, response_model = schemas.UserResponse, description = 'get one user or curret user')
async def get_user_by_id(user_id:int , db: session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user_logged_in)):
    try:
        _user = db.query(models.User).filter(models.User.user_id == user_id).first()
        if not _user:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'user not found')
        return _user    
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))





    



