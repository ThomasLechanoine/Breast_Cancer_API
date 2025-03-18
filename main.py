import uvicorn
from fastapi import FastAPI, File, UploadFile
import numpy as np
import pandas as pd
from PIL import Image
from io import BytesIO
from PIL import Image
import joblib
from pydantic import BaseModel
from params import *
from io import BytesIO
#from tensorflow.keras.models import load_model
#from tensorflow.keras.preprocessing.image import load_img, img_to_array
#import tensorflow as tf


if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 8000))  # Fallback to 8000 if PORT not set
    uvicorn.run(app, host="0.0.0.0", port=port)

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World come back again"}

# Charger le modèle Machine Learning
ML_MODEL_PATH = ML_MODEL_PATH #<------------------------------------------------
SCALER_PATH = ML_SCALER_PATH #<------------------------------------------------
