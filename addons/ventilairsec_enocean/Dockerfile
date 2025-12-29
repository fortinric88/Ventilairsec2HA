ARG BUILD_FROM
FROM $BUILD_FROM

# Installer les dépendances système
RUN apk add --no-cache \
    python3 \
    py3-pip \
    py3-requests \
    py3-serial \
    py3-cryptography \
    git \
    gcc \
    musl-dev \
    python3-dev

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
