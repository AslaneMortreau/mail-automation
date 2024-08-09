# Utiliser une image de base officielle de Python
FROM python:3.10

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier requirements.txt dans le répertoire de travail
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le contenu du répertoire courant dans le conteneur
COPY . .

# Exposer le port que Streamlit utilise
EXPOSE 8501

# Commande pour lancer l'application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
