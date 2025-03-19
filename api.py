from fastapi import FastAPI, File, UploadFile
import tensorflow as tf
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from io import BytesIO
from PIL import Image
import joblib
from pydantic import BaseModel
from params import *
from fastapi import FastAPI, File, UploadFile
import tensorflow as tf
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from io import BytesIO
import matplotlib.pyplot as plt
from PIL import Image
from params import DL_MODEL_PATH
from Deep_learning.dl_preprocess import extract_features, preprocess_input  # ✅ Importation de extract_features
from fastapi import FastAPI, File, UploadFile
import tensorflow as tf
from tensorflow.keras.models import load_model
from Deep_learning.dl_model import RandomFixedDense  # ✅ Importation de la couche personnalisée
from params import DL_MODEL_PATH

# Initialiser l'API
app = FastAPI()

# ✅ Charger le modèle en spécifiant la couche personnalisée
print("🔄 Chargement du modèle de deep learning...")
model = load_model(DL_MODEL_PATH, custom_objects={"RandomFixedDense": RandomFixedDense})
print("✅ Modèle DL chargé avec succès.")

# Chargement du feature extractor (VGG16)
feature_extractor = tf.keras.applications.VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3), pooling="avg")

# Fonction de prétraitement d'image
def preprocess_image(image_input):
    """
    Charge et prétraite une image depuis un fichier ou un objet BytesIO.
    """
    img = load_img(image_input, target_size=(224, 224))
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Ajouter une dimension batch
    img_array = preprocess_input(img_array)  # Prétraitement pour VGG16
    return img_array


# Endpoint de prédiction
@app.post("/predict_dl")
async def predict(file: UploadFile = File(...)):
    try:
        # Lire l'image et la convertir
        image_bytes = BytesIO(await file.read())
        img_array = preprocess_image(image_bytes)

        # Extraction des features avec la fonction existante
        features, _ = extract_features(feature_extractor, [(img_array, np.zeros(1))])
         # `_` car pas besoin des labels

        # Prédiction avec le modèle edRVFL
        res = model.predict(features, verbose=0)[0][0]

        # Interprétation du résultat
        diagnostic = "Positif" if res >= 0.45 else "Négatif"
        # prob = res if res >= 0.5 else 1 - res

        # # Afficher l'image avec la prédiction
        # img = Image.open(image_bytes)
        # plt.figure(figsize=(6, 6))
        # plt.imshow(img)
        # plt.axis("off")
        # plt.title(f"{diagnostic} ({prob:.2%})", fontsize=14)

        # Retourner la réponse
        response = {"diagnostic": diagnostic}
        print("✅ Réponse envoyée :", response)  # Debugging
        return response

    except Exception as e:
        print("❌ Erreur API :", str(e))
        return {"error": str(e)}


# ------------------- Machine Learning Prediction -------------------

# Charger le modèle Machine Learning
#ML_MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),"Machine_learning", "models_saved", "ml_best_model.pkl")
#SCALER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),"Machine_learning", "models_saved", "ml_scaler.pkl")
ML_MODEL_PATH = "Machine_Learning/models_saved/ml_best_model.pkl"
SCALER_PATH = "Machine_Learning/models_saved/ml_scaler.pkl"

print("Chargement du modèle de Machine Learning...")
ml_model = joblib.load(ML_MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
print("✅ Modèle de Machine Learning chargé avec succès.")

# Définir un schéma pour les données entrantes
class PredictionInput(BaseModel):
    features: list[float]

# Endpoint pour prédire sur des données tabulaires
@app.post("/predict_ml")
async def predict_ml(data: PredictionInput):
    """
    Reçoit une liste de caractéristiques, les prétraite et effectue une prédiction avec le modèle ML.
    """
    try:
        # Convertir en DataFrame avec les noms des colonnes attendus
        input_data = pd.DataFrame([data.features], columns=scaler.feature_names_in_)

        # Appliquer le scaling
        input_scaled = scaler.transform(input_data)

        # Faire la prédiction
        prediction = ml_model.predict(input_scaled)[0]
        diagnostic = "1= Malin (Cancer)" if prediction == 1 else "0= Bénin (Sans Cancer)"

        return {"diagnostic": diagnostic}

    except Exception as e:
        return {"error": str(e)}
