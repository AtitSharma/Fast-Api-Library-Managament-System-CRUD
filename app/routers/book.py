from fastapi import status,HTTPException,APIRouter,Depends
from app import models,schema,database,oauth2
from sqlalchemy.orm import Session



router=APIRouter(
    prefix="/book",
    tags=["Book"]

)


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schema.BookCreate)
def create_book(book:schema.BookCreate,db : Session =Depends(database.get_db),current_user=Depends(oauth2.get_current_user)):
    user=db.query(models.User).filter(models.User.id==current_user.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User Not Found")
    newbook=models.Book(author_id=user.id,**dict(book))
    db.add(newbook)
    db.commit()
    db.refresh(newbook)
    
    return newbook
    
    