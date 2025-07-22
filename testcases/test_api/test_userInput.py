from app.main import app
from fastapi.testclient import TestClient
import sys
import os
# Add root directory to Python path
print("System path:",sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../../../'))))






client = TestClient(app)


def test_post_api_submit_user_input():
    response = client.post("/userinput", json={
        "text": "This is a test input",
        "uploadedFiles": [""]
    })
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Sentiment analysis completed successfully."
