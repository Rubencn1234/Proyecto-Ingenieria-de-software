import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv no está instalado. Ejecute 'pip install -r requirements.txt'")

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default_dev_key_fallback'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///aduanas.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
