from passlib.context import CryptContext
from datetime import datetime,timedelta
from dotenv import load_dotenv
from jose import jwt,JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException
from schemas.schemas import TokenData
import os


# load .env file
load_dotenv()

# get variables from environment
SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRED_MINUTES=os.getenv("ACCESS_TOKEN_EXPIRED_MINUTES")

# password hashing context
pwd_context= CryptContext(schemes=['bcrypt'],deprecated='auto')
# OAuth2 scheme
oauth2_scheme= OAuth2PasswordBearer(tokenUrl="login")

def hash_password(password:str)->str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# JWT token creation 
def generate_token(data:dict):
    to_encode= data.copy()
    expire= datetime.utcnow()+ timedelta(minutes=int(ACCESS_TOKEN_EXPIRED_MINUTES))
    to_encode.update({"exp":expire})
    encoded_jwt= jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt



def get_current_user(token:str=Depends(oauth2_scheme))->TokenData:
    credentials_exception= HTTPException(
        status_code=401,
        detail="Invalid auth credentials",
        headers={'WWW-Authenticate':"Bearer"},

    )
    try:
        payload= jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        email:str= payload.get('sub')
        if email is None:
            raise credentials_exception
        return TokenData(username=email)
    except JWTError:
        raise credentials_exception


