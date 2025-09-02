import joblib
import os
import wandb
import datetime
from fastapi import Request, HTTPException


def load_model():
    try:
        # Load model from WandB
        WANDB_LOGIN_KEY = os.environ.get('WANDB_LOGIN_KEY')
        wandb.login(key=WANDB_LOGIN_KEY)
        run = wandb.init(project='my_fastapi_backend_repo',
                        name=f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}+training_run")

        artifact = run.use_artifact(
            'ayenyeinsan2904-chiang-mai-university-org/wandb-registry-model/senior_project_myanmar_senti:latest', type='model')
        artifact_dir = artifact.download()

        print(f"Artifact downloaded to: {artifact_dir}")

        
    
        model = None
        for file in os.listdir(artifact_dir):
            if file.endswith('.h5') or file.endswith('.pkl'):
                model = os.path.join(artifact_dir, file)
                break


       
        model = joblib.load(model)
        print("✅ Sentiment model loaded successfully.", model)
            
            
    except Exception as e:
            model = None
            
            print(f"❌ Failed to load model: {e}")
    finally:
            run.finish()
        
    return model


def get_model(request: Request):
    model = request.app.state.model
    if model is None:
        raise HTTPException(
            status_code=503, detail="Sentiment model  is not loaded")
    return model
