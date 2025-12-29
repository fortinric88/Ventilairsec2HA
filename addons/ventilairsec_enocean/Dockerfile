ARG BUILD_FROM=homeassistant/amd64-base:latest
FROM ${BUILD_FROM}

# Installer les dépendances système
RUN apk add --no-cache \
      python3 \
      py3-pip

# Définir le répertoire de travail
WORKDIR /app

# Copier les requirements
COPY requirements.txt .

# Installer les dépendances Python
RUN pip3 install --no-cache-dir -r requirements.txt

# Copier les fichiers de l'application
COPY rootfs /

# Permissions sur le script de démarrage
RUN chmod a+x /run.sh

# Définir le point d'entrée
ENTRYPOINT ["/run.sh"]
