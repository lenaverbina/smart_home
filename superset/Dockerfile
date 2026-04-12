FROM apache/superset:latest

USER root

COPY superset_config.py /app/superset_config.py
RUN rm -rf /app/superset_home/.local

# Устанавливаем драйвер системно
RUN pip install --no-cache-dir --target=/app/.venv/lib/python3.10/site-packages "clickhouse-connect>=0.6.0,<0.8.0"

USER superset

CMD ["/app/docker/entrypoints/run-server.sh"]