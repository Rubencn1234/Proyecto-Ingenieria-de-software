import os
import sys

# Directorio base para archivos persistentes
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

try:
    from dotenv import load_dotenv
    # Buscar el .env en el BASE_DIR si existe
    env_path = os.path.join(BASE_DIR, '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
    else:
        load_dotenv()
except ImportError:
    print("Warning: python-dotenv no está instalado. Ejecute 'pip install -r requirements.txt'")

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default_dev_key_fallback'
    
    # Asegurar que la base de datos se guarda en el mismo lugar que el .exe
    db_path = os.path.join(BASE_DIR, 'aduanas.db')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or f'sqlite:///{db_path}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

