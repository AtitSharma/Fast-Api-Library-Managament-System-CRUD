from fastapi import status,HTTPException,APIRouter,Depends
from sqlalchemy.orm import Session
from app.database  import get_db
from app import schema,models,authentication

router=APIRouter(
    prefix="/library",
    tags=["Library"]

)

@router.post("/giverole")
def give_role(roles:schema.UserRole,db : Session = Depends(get_db),
              current_user=Depends(authentication.get_current_user),
              give_role_to_user_=Depends(authentication.give_role_to_user),
                isadmin=Depends(authentication.isadmin),
              check_unique=Depends(authentication.check_unique_fields),
              ):
    userrole=models.User_Role(**dict(roles))
    db.add(userrole)
    db.commit()
    db.refresh(userrole)
    return {"Successfully Provided the Role to the User"}
    