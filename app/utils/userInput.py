
from fastapi import  HTTPException, status, APIRouter, Depends
from app.repository.db import db_dependency
from app.schemas.schemas import SentimentResult, Probabilities
from app.repository.dataLayer.sentiment_results import insert_sentiment_results
from LLMmodels.deploy_model_20250615_133439 import predict_sentiment


# helper function for processing sentiment analysis and save to db object
async def process_text_for_sentiment(
    text: str,
    db: db_dependency,
    user_id: int
) -> SentimentResult:

    analysis_result = await perform_sentiment_analysis(text)
    confidence = analysis_result['probabilities'].get(
        f"class_{analysis_result['predicted_class']}", 0.0)

 # Create SentimentResult object
    sentiment_result = SentimentResult(
        text=text,
        predicted_label=analysis_result['predicted_label'],
        predicted_class=analysis_result['predicted_class'],
        probabilities=Probabilities(
            class_0=analysis_result['probabilities'].get(
                'class_0', 0.0),
            class_1=analysis_result['probabilities'].get(
                'class_1', 0.0),
            class_minus_1=analysis_result['probabilities'].get(
                'class_-1', 0.0)
        ),
        confidence=confidence
    )
    insert_db = await insert_sentiment_results(db, sentiment_result, user_id)
    if not insert_db:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to insert sentiment result into the database."
        )
    return sentiment_result


async def perform_sentiment_analysis(text: str):
    # Placeholder for sentiment analysis logic
    result = predict_sentiment(text)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="ML model failed to analyze"
        )
    return result
