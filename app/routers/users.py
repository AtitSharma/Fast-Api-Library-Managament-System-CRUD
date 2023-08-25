from fastapi import status, HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session
from app import authentication, schema
from app.database import get_db
from app import utils, models
# from fastapi.security.oauth2 import OAuth2PasswordRequestForm
# import sqlalchemy
# from sqlalchemy import or_, and_

router = APIRouter(
    prefix="/users",
    tags=["Users"]

)


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: schema.UserRegister, db: Session = Depends(get_db),
             active_user_exits=Depends(authentication.activeuser),
             create_role=Depends(authentication.create_borrower_role)
             ):
    '''

        THIS IS TO REGISTER USER IN THE SYSTEM  
    
    '''
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**dict(user))
    db.add(new_user)
    db.commit()
    '''
        THIS IS DONE TO GIVE THE USER A ROLE OF BORROWER AS SOON AS USER IS CREATED
    '''
    
    role=db.query(models.Role).filter(models.Role.name=="borrower").first()
    new_role=models.User_Role(user_id=new_user.id,role_id=role.id)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    db.refresh(new_user)
    
    
    register_data=schema.UserDetails(
        email=new_user.email,
        username=new_user.email
    )


    response =schema.StatusSchema(
        code="200",
        status="OK",
        data = register_data,
        message ="Created"
    ).dict(exclude_none=True)
    return response


@router.post("/login", status_code=status.HTTP_202_ACCEPTED)
def login(user_credentials: schema.UserLogin, db: Session = Depends(get_db)):  
    '''
        THIS IS TO LOGIN USER AND PROVIDE JWT TOKEN TO THE USER AFTER LOGIN 
    '''
    user = db.query(models.User).filter(user_credentials.email == models.User.email).first()
    if not user:
        # raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid User")
        response=schema.StatusSchema(
            code="403",
            status="FORBIDDEN",
            data=[],
            message="Invalid User",
            
        )
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=response.__dict__)
    if not utils.verify(user_credentials.password, user.password):
        response=schema.StatusSchema(
            code="403",
            status="FORBIDDEN",
            data=[],
            message="Incorrect Password",
            
        )
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=response.__dict__)
    access_token = authentication.create_access_token(data={"user_id": user.id})
    return {"token": access_token, "token_type": "bearer"}


@router.delete("/delete/{id}/", status_code=status.HTTP_200_OK)
def delete_user(id: int, db: Session = Depends(get_db),
                current_user=Depends(authentication.get_current_user),
                isadmin=Depends(authentication.isadmin)):
    
    '''
        THIS IS TO DELETE THE PARTICULAR USER ON THE BASIS OF THE ID 
    '''
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No Such User Found")
    user.delete(synchronize_session=False)
    db.commit()
    return {"msg": "Deleted User Successfully"}
