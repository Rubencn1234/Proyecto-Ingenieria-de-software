import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask
from config import Config
from extensions import db, login_manager
from models import User
from flask_wtf.csrf import CSRFProtect

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)


    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    login_manager.login_message = "Por favor inicie sesión para acceder a esta página."
    login_manager.login_message_category = "warning"
    

    csrf = CSRFProtect(app)


    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/aduanas.log', maxBytes=10240, backupCount=10)
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
        return User.query.get(int(user_id))


    with app.app_context():
        db.create_all()

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
