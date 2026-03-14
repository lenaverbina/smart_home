FROM apache/airflow:2.8.1-python3.11

USER root

# Устанавливаем Docker CLI
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    docker.io \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow