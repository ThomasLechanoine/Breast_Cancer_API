import uvicorn
from fastapi import FastAPI, File, UploadFile
from tensorflow.keras.models import load_model
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
from tensorflow.keras.preprocessing.image import load_img, img_to_array
#import tensorflow as tf


if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 8000))  # Fallback to 8000 if PORT not set
    uvicorn.run(app, host="0.0.0.0", port=port)

app = FastAPI()

def preprocess_image(image: Image.Image):
    img = image.resize((224, 224))  # Adapter à la taille du modèle
    img_array = img_to_array(img) / 255.0  # Normalisation
    img_array = np.expand_dims(img_array, axis=0)  # Ajouter une dimension batch
    return img_array

@app.get("/")
def read_root():
    return {"Hello": "World come back again"}

@app.post("/predict_dl")
async def predict(file: UploadFile = File(...)):
    """
    Reçoit une image, la prétraite et effectue une prédiction avec le modèle de deep learning.
    """
    try:
        # Charger l'image depuis le fichier uploadé
        image = Image.open(BytesIO(await file.read()))

        # Prétraitement de l'image
        img_array = preprocess_image(image)
        img_array = np.repeat(img_array, 3, axis=-1)

        # Faire la prédiction
        model = load_model(DL_MODEL_PATH)
        res = model.predict(img_array)[0][0]
        # Ajout de logs pour comprendre la sortie du modèle
        #print(f"Valeur brute de la prédiction : {res}")  # Debugging

        # Interprétation du résultat
        diagnostic = "Positif" if res >= 0.5 else "Négatif"
        prob = res if res >= 0.5 else 1 - res

        return {
            "diagnostic": diagnostic,
            "probability": f"{prob:.2%}"
        }

    except Exception as e:
        return {"error": str(e)}


# Charger le modèle Machine Learning
DL_MODEL_PATH = "Deep_learning/models_saved/best_model.h5"
ML_MODEL_PATH = "/Machine_learning/models_saved/ml_best_model.pkl"
ML_SCALER_PATH = "/Machine_learning/models_saved/ml_scaler.pkl"
# ML_MODEL_PATH = ML_MODEL_PATH #<------------------------------------------------
# SCALER_PATH = ML_SCALER_PATH #<------------------------------------------------
