import os

SECRET_KEY = os.getenv('SUPERSET_SECRET_KEY', 'dev-key-change-me')
SQLALCHEMY_DATABASE_URI = 'sqlite:////app/superset_home/superset.db'
ROW_LIMIT = 5000
SUPERSET_WEBSERVER_PORT = 8088
SUPERSET_WEBSERVER_ADDRESS = '0.0.0.0'