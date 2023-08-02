from jose import JWTError,jwt
from datetime import datetime,timedelta
from fastapi import status,HTTPException,Depends
from app import schema,models
from fastapi.security import OAuth2PasswordBearer
from app.database import get_db
from sqlalchemy.orm import Session
from app.config import settings
from sqlalchemy import or_,and_




oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expires_minutes


def create_access_token(data:dict):
    to_encode =data.copy()
    expires=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expires})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    
    return encoded_jwt


def verify_access_token(token:str,credential_expression):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id:int =payload.get("user_id")
        if id is None:
            raise credential_expression
        token_data=schema.TokenData(id=id)
    except JWTError:
        raise credential_expression
    return token_data



def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Couldn't Validate the User", headers={"WWW-Authenticate":"Bearer"})
    token=verify_access_token(token,credentials_exception)
    user=db.query(models.User).filter(models.User.id==token.id).first()
    return user


def activeuser(user: schema.UserRegister, db: Session = Depends(get_db)):
    
    ''' IF THE DB HAS SAME USER CREDENTIALS BEFORE OR NOT '''
    
    active_user=db.query(models.User).filter(or_(models.User.username == user.username,models.User.email==user.email)).first() 
    if active_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Aleady Exits Such User")
    return 


def active_book(id:int,db: Session= Depends(get_db),current_user=Depends(get_current_user)):
    
    ''' IF THE REQUEST USER IS THE BOOK AUTHOR OR NOT ,
    
        AND IF THE BOOK EXITS OR NOT '''
    
    updated_book=db.query(models.Book).filter(and_(models.Book.id==id ,models.Book.author_id==current_user.id))
    if not updated_book.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Book With id {id} Doesnt Exits or You might not be the Author Of the Book")
    
    return 
    
    











