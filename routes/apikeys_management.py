from fastapi import APIRouter, HTTPException,Depends
from starlette import status
from schemas.schemas import Api_Key as api_key_achema
from utils.auth import get_current_user
from typing import List, Optional
from schemas.schemas import TokenData
router = APIRouter()




@router.post("/api_key_creation", status_code=status.HTTP_201_CREATED)
async def generate_new_apikey(input_request,current_user: Optional[TokenData] = Depends(get_current_user)):
    
    request = input_request
    
    return {
     "message" : "API Key Generated!"
     "result": request
    }