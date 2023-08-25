from fastapi import status, HTTPException, APIRouter, Depends
from app import authentication, models, schema, database
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(
    prefix="/book",
    tags=["Book"]

)


@router.post("/", status_code=status.HTTP_201_CREATED, 
             response_model=schema.BookCreate 
             ,summary="Book Can be Created Frome Here"
             ,description="Creates a new book in the library.",
             ) 
def create_book(book: schema.BookCreate, db: Session = Depends(database.get_db),
                current_user=Depends(authentication.get_current_user)):
    user = db.query(models.User).filter(models.User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")
    newbook = models.Book(author_id=user.id, **dict(book))
    db.add(newbook)
    db.commit()
    db.refresh(newbook)
    return newbook


@router.delete("/{id}/")
def delete_book(id: int, db: Session = Depends(database.get_db),
                current_user=Depends(authentication.get_current_user),
                active_book=Depends(authentication.active_book),
                check_user=Depends(authentication.check_user)):
    post = db.query(models.Book).filter(models.Book.id == id)
    post.delete(synchronize_session=False)
    db.commit()
    return {"msg": "deleted"}


@router.put("/{id}/")
def update_book(id: int, book: schema.BookCreate,
                db: Session = Depends(database.get_db),
                current_user=Depends(authentication.get_current_user),
                active_book=Depends(authentication.active_book),
                permission=Depends(authentication.check_user)):
    book_query = db.query(models.Book).filter(models.Book.id == id)
    book_query.update(dict(book), synchronize_session=False)
    db.commit()
    return {"msg": "Updated"}


@router.get("/", response_model=List[schema.BookDetail])
def read_books(db: Session = Depends(database.get_db),
               current_user=Depends(authentication.get_current_user),
               limit: int = 3,
               search: Optional[str] = ""):
    books = db.query(models.Book).filter(models.Book.title.contains(search)).limit(limit).all()
    return books


@router.get("/{id}/", response_model=schema.BookDetail)
def read_book(id: int, db: Session = Depends(database.get_db),
              current_user=Depends(authentication.get_current_user),
              active_book=Depends(authentication.active_book)):
    book = db.query(models.Book).filter(models.Book.id == id).first()
    return book
