import logging
from logging.handlers import RotatingFileHandler
import os
import sys
from flask import Flask
from config import Config
from extensions import db, login_manager
from models import User
from flask_wtf.csrf import CSRFProtect

def create_app(config_class=Config):
    if getattr(sys, 'frozen', False):
        template_folder = os.path.join(sys._MEIPASS, 'templates')
        static_folder = os.path.join(sys._MEIPASS, 'static')
        app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
        base_dir = os.path.dirname(sys.executable)
    else:
        app = Flask(__name__)
        base_dir = os.path.abspath(os.path.dirname(__file__))
        
    app.config.from_object(config_class)


    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    login_manager.login_message = "Por favor inicie sesión para acceder a esta página."
    login_manager.login_message_category = "warning"
    

    csrf = CSRFProtect(app)


    logs_dir = os.path.join(base_dir, 'logs')
    if not os.path.exists(logs_dir):
        os.mkdir(logs_dir)
    log_file = os.path.join(logs_dir, 'aduanas.log')
    file_handler = RotatingFileHandler(log_file, maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Inicio de aplicación Aduanas')


    from routes import main_bp
    from errors import errors_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(errors_bp)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))


    with app.app_context():
        db.create_all()

        # Migración automática: agregar columna user_id si no existe
        from sqlalchemy import inspect, text
        inspector = inspect(db.engine)
        columns = [col['name'] for col in inspector.get_columns('tramite')]
        if 'user_id' not in columns:
            with db.engine.connect() as conn:
                conn.execute(text('ALTER TABLE tramite ADD COLUMN user_id INTEGER REFERENCES user(id)'))
                conn.commit()
            app.logger.info('Migración aplicada: columna user_id agregada a tramite')

        if User.query.count() == 0:
            from werkzeug.security import generate_password_hash
            users = [
                User(rut='pasajero', password_hash=generate_password_hash('123'), rol='pasajero'),
                User(rut='aduana', password_hash=generate_password_hash('123'), rol='aduana'),
                User(rut='pdi', password_hash=generate_password_hash('123'), rol='pdi'),
                User(rut='policia', password_hash=generate_password_hash('123'), rol='policia_arg')
            ]
            db.session.bulk_save_objects(users)
            db.session.commit()

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
