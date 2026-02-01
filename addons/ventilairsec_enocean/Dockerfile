ARG BUILD_FROM=homeassistant/amd64-base:2024.01
FROM ${BUILD_FROM}

# Install system dependencies
RUN apk add --no-cache \
      python3 \
      py3-pip \
      bash \
      git

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application files
COPY rootfs /

# Fix permissions for startup script
RUN chmod a+x /run.sh

# Create required directories
RUN mkdir -p /var/log/ventilairsec \
             /var/lib/ventilairsec \
             /etc/ventilairsec

# Set entry point
ENTRYPOINT ["/run.sh"]
