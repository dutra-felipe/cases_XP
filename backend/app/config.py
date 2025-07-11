import os
from dotenv import load_dotenv
from urllib.parse import quote_plus


load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    if not SQLALCHEMY_DATABASE_URI:
        DB_USER = quote_plus(os.environ.get('POSTGRES_USER'))
        DB_PASSWORD = quote_plus(os.environ.get('POSTGRES_PASSWORD'))
        DB_HOST = os.environ.get('DB_HOST', 'db')
        DB_PORT = os.environ.get('DB_PORT', '5432')
        DB_NAME = os.environ.get('POSTGRES_DB')
        SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
