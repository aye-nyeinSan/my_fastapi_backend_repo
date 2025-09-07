
import os
from pathlib import Path

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException,Depends
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from app.repository.db import test_engine,engine,Base
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncEngine

from app.settings import AWS_Settings, s3_client
from app.routes import retrain,auth,userInput,predict,apikeys_management,uploadToS3

from contextlib import asynccontextmanager
from app.utils.load_model import load_model
from app.utils.api_services import CustomRateLimitMiddleware

load_dotenv(dotenv_path=Path(
    __file__).resolve().parent / ".env", override=True)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost"
]
rate_limits = {
    "/predict": (5, 60),
}  # 5 requests per 60 seconds

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    try:
        print("Loading ML model and initializing database...")
        #load model 
        app.state.model =  load_model()
        async with engine.begin() as conn:
             await conn.run_sync(Base.metadata.create_all)
       # Only run test DB init if in test mode
        if os.getenv("TESTING") == "1":
            async with test_engine.connect() as test_conn:
                await test_conn.run_sync(Base.metadata.create_all)
        print("Application startup: Database tables created (or already exist).")
        yield 
    finally:
        print("Application shutdown: Disposing database engine...")
        await engine.dispose()
        if test_engine:
            test_engine.dispose()  # Properly closes all pooled connections
        print("Application shutdown: Database engine disposed.")


app = FastAPI(title="MyanSen Language Processing API",lifespan=lifespan, contact={
    "name": "Ayen Nyein San",
    "email": "aye2904@gmail.com"})
        
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_middleware(CustomRateLimitMiddleware, limits=rate_limits)
# Routers
app.include_router(auth.router)
app.include_router(predict.router)
app.include_router(retrain.router)
app.include_router(userInput.router)
app.include_router(apikeys_management.router)
app.include_router(uploadToS3.router, prefix="/api/v1")

   


