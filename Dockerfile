# Utiliser une image de base officielle Python
FROM python:3.10.6-buster

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers de dépendances et installer les dépendances
COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copier le reste des fichiers de l'application dans le conteneur
COPY . .

# Commande pour exécuter l'application en utilisant uvicorn
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8080"]
#CMD uvicorn api.simple:app --host 0.0.0.0 --port $PORT
