import os

##################  VARIABLES ENVIRONNEMENTALES  ##################
GCP_PROJECT = os.environ.get('GCP_PROJECT')
GCP_REGION = os.environ.get('GCP_REGION')
BUCKET_NAME = os.environ.get('BUCKET_NAME')
MODEL_TARGET = os.environ.get('MODEL_TARGET')
BUCKET_MODEL = os.environ.get('BUCKET_MODEL')

##################  CHEMINS DES DONNÉES  ##################
ML_DATA_PATH = "/home/bren/code/ThomasLechanoine/Breast_Cancer_Project/Data/Machine_learning.csv"
DL_ZIP_PATH = "Data/Data_prepros.zip"
DL_DATA_PATH = "Data/Data_Deep_Learning"

##################  CHEMINS DES MODÈLES  ##################
DL_MODEL_PATH = "Deep_learning/models_saved/best_model.h5"
ML_MODEL_PATH = "/home/bren/code/ThomasLechanoine/Breast_Cancer_Project/Machine_learning/models_saved/ml_best_model.pkl"
ML_SCALER_PATH = "/home/bren/code/ThomasLechanoine/Breast_Cancer_Project/Machine_learning/models_saved/ml_scaler.pkl"

##################  PARAMÈTRES D'ENTRAÎNEMENT  ##################
DL_BATCH_SIZE = 32
DL_IMG_SIZE = (224, 224)
DL_EPOCHS = 30
DL_OPTIMIZER = 'adam'
DL_LOSS_FUNCTION = 'binary_crossentropy'
DL_METRICS = ['accuracy', 'recall']

##################  CONFIGURATION API  ##################
DL_API_URL = "http://127.0.0.1:8000/predict"
ML_API_URL = "http://127.0.0.1:8000/predict_ml"


##################  PARAMÈTRES D'ENTRAÎNEMENT DU MODÈLE DL  ##################

DL_OPTIMIZER = "adam"  # Optimiseur du modèle (peut être 'adam', 'sgd', etc.)
DL_LOSS_FUNCTION = "binary_crossentropy"  # Fonction de perte pour classification binaire
DL_METRICS = ["accuracy", "recall"]  # Liste des métriques utilisées pour l'entraînement
