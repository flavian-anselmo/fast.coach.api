from passlib.context import CryptContext


# configure it to use bycrypt 
password_conxt = CryptContext(schemes=['bcrypt'])

def  get_hashed_password(password:str) -> str:
    '''
    takes plain password and returns the hashed version 
    '''
    return password_conxt.hash(password)

def verify_password(password:str, hashed_password:str)-> str:
    '''
    confirms if the hash and the pswd match 
    
    '''
    return password_conxt.verify(password, hashed_password)     



    