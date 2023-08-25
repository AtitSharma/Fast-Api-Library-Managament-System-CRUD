from fastapi import status, HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import schema, models, authentication

router = APIRouter(
    prefix="/library",
    tags=["Library"]

)


@router.post("/giverole")
def give_role(roles: schema.UserRole,
              db: Session = Depends(get_db),
              current_user=Depends(authentication.get_current_user),
              give_role_to_user_=Depends(authentication.give_role_to_user),
              isadmin=Depends(authentication.isadmin),
              check_unique=Depends(authentication.check_unique_fields),
              ):
    '''
        THIS IS TO GIVE ROLE TO THE USER  
    '''
    userrole = models.User_Role(**dict(roles))
    db.add(userrole)
    db.commit()
    db.refresh(userrole)
    return {"Successfully Provided the Role to the User"}


@router.post("/createrole")
def create_role(role: schema.RoleCreate,
                db: Session = Depends(get_db),
                current_user=Depends(authentication.get_current_user),
                isadmin=Depends(authentication.isadmin),
                check_role=Depends(authentication.check_role)):
    '''
    
        THIS IS TO CREATE ROLE IN THE DB
        
    '''

    new_role = models.Role(**dict(role))
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return {"Successfully Created Role ": new_role}


@router.delete("/deleterole/")
def delete_role(role_name:schema.Rolename,
                db: Session=Depends(get_db),
                current_user=Depends(authentication.get_current_user),
                is_admin=Depends(authentication.isadmin),
                active_role=Depends(authentication.check_role_name),  
                ):
    
    '''
        THIS IS TO DELETE ROLES FROM THE DATABASE
    '''
    
    role=db.query(models.Role).filter(models.Role.name == str(role_name.name).lower())
    role.delete(synchronize_session=False)
    db.commit()
    return {"msg":f"Successfully Deleted The Role "}




    
















