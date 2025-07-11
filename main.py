
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from core.db import engine
import models
from routes import retrain,auth

models.Base.metadata.create_all(bind=engine)

load_dotenv()
app = FastAPI()
origins = [
    "http://localhost:5173",
    "https://127.0.0.1:5173",
    "http://localhost"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(retrain.router)
app.include_router(auth.router)


    
    
    
        
        
   

   
