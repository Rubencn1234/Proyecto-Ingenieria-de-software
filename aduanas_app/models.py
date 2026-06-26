from flask_login import UserMixin
from extensions import db

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    rut = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    rol = db.Column(db.String(20), nullable=False)

class Tramite(db.Model):
    __tablename__ = 'tramite'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    nombre_pasajero = db.Column(db.String(100), nullable=False)
    documento = db.Column(db.String(20), nullable=False)
    patente = db.Column(db.String(20), nullable=False)
    origen = db.Column(db.String(50), nullable=False)
    destino = db.Column(db.String(50), nullable=False)
    bienes_declarados = db.Column(db.Text, nullable=True)
    estado_pdi = db.Column(db.String(20), default='Pendiente') # Pendiente, Aprobado, Rechazado
    estado_policia_arg = db.Column(db.String(20), default='Pendiente')
    estado_aduana = db.Column(db.String(20), default='Pendiente')
