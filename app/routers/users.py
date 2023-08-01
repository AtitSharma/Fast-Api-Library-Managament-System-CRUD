from fastapi import status,HTTPException,APIRouter,Depends
from sqlalchemy.orm import Session
from app import schema
from app.database import get_db
from app import utils,models,oauth2
# from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router=APIRouter(
    prefix="/users",
    tags=["Users"]

)

@router.post("/register",status_code=status.HTTP_201_CREATED)
def register(user:schema.UserRegister,db: Session=Depends(get_db)):
    hashed_password=utils.hash(user.password)
    user.password=hashed_password
    new_user=models.User(**dict(user))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg":"Successfully Registered Proceed to login "}


@router.post("/login",status_code=status.HTTP_202_ACCEPTED)
def login(user_credentials:schema.UserLogin,db : Session=Depends(get_db)):
    user=db.query(models.User).filter(user_credentials.email == models.User.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid User")
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Incorrect Password")
    access_token=oauth2.create_access_token(data={"user_id":user.id})
    return {"token":access_token,"token_type":"bearer"}


    
    
    
