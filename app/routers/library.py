from fastapi import status,HTTPException,APIRouter


router=APIRouter(
    prefix="/library",
    tags=["Library"]

)