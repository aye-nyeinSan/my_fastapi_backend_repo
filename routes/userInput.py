import csv
import io
import os
from typing import List, Optional

from LLMmodels.deploy_model_20250615_133439 import predict_sentiment
from pydantic import BaseModel, Field
from starlette import status

from fastapi import APIRouter, HTTPException

router = APIRouter()


class UserInputRequest(BaseModel):
    text: str = ""
    uploadedFiles: Optional[List[str]] = Field(default_factory=list)


class SentimentResult(BaseModel):
    id: str
    text: str
    sentiment: str
    confidence: float


async def perform_sentiment_analysis(text: str):
    # Placeholder for sentiment analysis logic
    print(f"Performing sentiment analysis on: {text}")
    result = predict_sentiment(text)
    return result
    
 


@router.post("/userinput", status_code=status.HTTP_201_CREATED)
async def submit_user_input(input_data: UserInputRequest):
    """
    Endpoint to handle user input.
    """
    if input_data.text:
        print(f"Received text: {input_data.text}")

        # perform the sentiment analysis process with input_data.text

        return {"message": "Text received", "text": input_data.text}
    
        #multiple files case
    elif input_data.uploadedFiles:
        # print("Received files for processing.")
        # print(f"Received files: {input_data.uploadedFiles}")

        result = []  
        for file in input_data.uploadedFiles:
            # print(f"Processing file: {file}")
            csv_file = io.StringIO(file)
            reader = csv.reader(csv_file)
            # print(f"Reader: {reader.__next__()}")  # Print the first row for debugging

            # read the rowdata from the files
            for row_data in reader:
                if row_data:  
                    text_to_analyze = row_data[0]
                    
                    # perform the sentiment analysis process with input_data.uploadedFiles's rowdata
                    analysis_result = await perform_sentiment_analysis(text_to_analyze)
                    result.append(analysis_result) 
                   
                else:
                    print("Skipping empty row in CSV.")
        return {
            "message": "Files processed",
            "results": result
        }
    
    elif not input_data.text and not input_data.uploadedFiles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid input: Please provide either text or files."
        )
