import csv
import io
import os
from typing import List, Optional


from LLMmodels.deploy_model_20250615_133439 import predict_sentiment
from pydantic import BaseModel, Field
from starlette import status
from schemas.schemas import UserInputRequest, SentimentResult, Probabilities, OverAllSentimentResult
from fastapi import APIRouter, HTTPException
from core.dataLayer.sentiment_results import insert_sentiment_results
from core.db import db_dependency

router = APIRouter()



async def perform_sentiment_analysis(text: str):
    # Placeholder for sentiment analysis logic
    result = predict_sentiment(text)
    return result
    
 


@router.post("/userinput", status_code=status.HTTP_201_CREATED,response_model=OverAllSentimentResult )
async def submit_user_input(input_data: UserInputRequest,db: db_dependency):
    """
    Endpoint to handle user input.
    """
    if input_data.text:
        # perform the sentiment analysis process with input_data.text

        return {"message": "Text received", "text": input_data.text}
    
        #multiple files case
    elif input_data.uploadedFiles:

        result = []
        for file in input_data.uploadedFiles:
            csv_file = io.StringIO(file)
            reader = csv.reader(csv_file)

            # read the rowdata from the files
            for row_data in reader:
                if row_data:  
                    text_to_analyze = row_data[0]
                    
                    # perform the sentiment analysis process with input_data.uploadedFiles's rowdata
                    analysis_result = await perform_sentiment_analysis(text_to_analyze)
            
                    #get confidence score 
                    confidence = analysis_result['probabilities'].get(
                        f"class_{analysis_result['predicted_class']}",0.0)
                    
                    # Create SentimentResult object
                    sentiment_result = SentimentResult(
                        text=text_to_analyze,
                        predicted_label=analysis_result['predicted_label'],
                        predicted_class=analysis_result['predicted_class'],
                        probabilities=Probabilities(
                            class_0=analysis_result['probabilities'].get('class_0', 0.0),
                            class_1=analysis_result['probabilities'].get('class_1', 0.0),
                            class_minus_1=analysis_result['probabilities'].get('class_-1', 0.0)
                        ),
                        confidence=confidence
                    )
                    
                    result.append(sentiment_result)
                    for sentiment_result in result:
                        # Insert the sentiment result into the database
                        await insert_sentiment_results(db,sentiment_result,user_id=1)
                    
                    
                   
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
