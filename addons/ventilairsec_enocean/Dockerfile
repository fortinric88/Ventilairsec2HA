FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && pip install --no-cache-dir -r /app/requirements.txt \
    && apt-get remove -y ca-certificates \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Copy the openenoceand daemon shipped in the repository if available
COPY ../../ExemplePluginJeedom/openenocean/resources/openenoceand /openenoceand
COPY run.sh /app/run.sh
RUN chmod +x /app/run.sh

CMD ["/app/run.sh"]
