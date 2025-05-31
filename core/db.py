import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# load .env file
load_dotenv()

# get variables from environment
POSTGRES_URL_NON_POOLING=os.getenv("POSTGRES_URL_NON_POOLING")
POSTGRES_USER=os.getenv("POSTGRES_USER")
POSTGRES_HOST=os.getenv("POSTGRES_HOST")
POSTGRES_PORT=os.getenv("POSTGRES_PORT")
SUPABASE_JWT_SECRET=os.getenv("SUPABASE_JWT_SECRET")

POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE")

DATABASE_URL=f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"

engine= create_engine(DATABASE_URL)
SessionLocal= sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()




