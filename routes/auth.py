from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from core.db import SessionLocal
from models import Testing
from typing import List

router=APIRouter()

class TestingBase(BaseModel):
   title:str

class TestingResponse(BaseModel):
   id:int
   title:str

   class Config:
      orm_mode=True

# DB Session dependency
def get_db():
   db=SessionLocal()
   try:
      yield db
   finally:
      db.close()

# Post endpoint
@router.post("/testing/",response_model=TestingResponse)
async def create_testing(test:TestingBase, db:Session=Depends(get_db)):
   db_test= Testing(title=test.title)
   db.add(db_test)
   db.commit()
   db.refresh(db_test)
   return db_test

# Get endpoint
@router.get("/testing/",response_model=List[TestingResponse])
async def get_testing(db:Session=Depends(get_db)):
   return db.query(Testing).all()

