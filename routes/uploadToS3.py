from schemas.schemas import AWS_PreSigned_Response, AWS_PreSigned_Request
from fastapi import APIRouter, HTTPException
from settings import AWS_Settings
from main import s3_client

router = APIRouter()

@router.post("/presigned_url", response_model=AWS_PreSigned_Response)
async def get_presigned_url(file_name: str, file_type: str):
    """
    Generate a pre-signed URL for uploading files to S3.
    """
    try:  
        bucket_name = AWS_Settings.AWS_S3_BUCKET_NAME
        key = f"uploads/{file_name}"
        
        response = s3_client.generate_presigned_url(
            'put_object',
            Params={'Bucket': bucket_name, 'Key': key, 'ContentType': file_type},
            ExpiresIn=3600  # URL expires in 1 hour
        )
        
        return AWS_PreSigned_Response(url=response, key=key, bucket=bucket_name)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))