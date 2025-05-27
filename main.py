
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
import os 
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
import requests

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

@app.get("/")
async def root():
    return {"message": "Hello aye "}

@app.post("/retrainmodel")
async def retrainmodel():
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    GITHUB_REPO_OWNER = os.getenv('GITHUB_REPO_OWNER')
    GITHUB_REPO_NAME = os.getenv('GITHUB_REPO_NAME')
    
    if not GITHUB_TOKEN:
        return { "error": "Github token is missing"},500
    if not GITHUB_REPO_OWNER or not GITHUB_REPO_NAME:
        return { "error": "Github repository is misconfigured"},500
    
    url = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/actions/workflows/retrain_model.yml/dispatches"
    
    headers = { 
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": f"{GITHUB_REPO_OWNER}",
               }
    
    try:
        response = requests.post(
            url,
            headers=headers,
            json={"ref": "main"}
        )
        response.raise_for_status()
        
        return {"message": "Model retraining started",
            "github_repo": f"{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}",
            "status_code": response.status_code}
        
    except requests.exceptions.RequestException as e:
        print(f"Error dispatching GitHub workflow: {e}")
        raise HTTPException(status_code=response.status_code, detail=str(e))
    
        
        
   

   
