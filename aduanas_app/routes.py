from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from models import User, Tramite
from extensions import db
import logging

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for(f'main.dashboard_{current_user.rol}'))
        
    if request.method == 'POST':
        rut = request.form.get('rut')
        password = request.form.get('password')
        
        try:
            user = User.query.filter_by(rut=rut).first()
            if user and check_password_hash(user.password_hash, password):
                login_user(user)
                current_app.logger.info(f"Usuario {rut} (Rol: {user.rol}) inició sesión exitosamente.")
                flash(f'Bienvenido, {user.rol.replace("_", " ").title()}', 'success')
                return redirect(url_for(f'main.dashboard_{user.rol}'))
            else:
                current_app.logger.warning(f"Intento de inicio de sesión fallido para RUT: {rut}")
                flash('RUT o contraseña incorrectos', 'error')
        except Exception as e:
            current_app.logger.error(f"Error en login: {e}")
            flash('Error del sistema al intentar iniciar sesión. Intente más tarde.', 'error')
            
    return render_template('login.html')

@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Ha cerrado sesión exitosamente', 'success')
    return redirect(url_for('main.login'))

@main_bp.route('/pasajero')
@login_required
def dashboard_pasajero():
    if current_user.rol != 'pasajero':
        flash('Acceso denegado', 'error')
        return redirect(url_for('main.login'))
        
    page = request.args.get('page', 1, type=int)
    tramites = Tramite.query.filter_by(user_id=current_user.id).order_by(Tramite.id.desc()).paginate(page=page, per_page=5)
    return render_template('dashboard_pasajero.html', tramites=tramites.items, pagination=tramites)

@main_bp.route('/pdi')
@login_required
def dashboard_pdi():
    if current_user.rol != 'pdi':
        flash('Acceso denegado', 'error')
        return redirect(url_for('main.login'))
    page = request.args.get('page', 1, type=int)
    tramites = Tramite.query.order_by(Tramite.id.desc()).paginate(page=page, per_page=20)
    return render_template('dashboard_oficial.html', tramites=tramites.items, pagination=tramites)

@main_bp.route('/policia')
@login_required
def dashboard_policia_arg():
    if current_user.rol != 'policia_arg':
        flash('Acceso denegado', 'error')
        return redirect(url_for('main.login'))
    page = request.args.get('page', 1, type=int)
    tramites = Tramite.query.order_by(Tramite.id.desc()).paginate(page=page, per_page=20)
    return render_template('dashboard_oficial.html', tramites=tramites.items, pagination=tramites)

@main_bp.route('/aduana')
@login_required
def dashboard_aduana():
    if current_user.rol != 'aduana':
        flash('Acceso denegado', 'error')
        return redirect(url_for('main.login'))
    page = request.args.get('page', 1, type=int)
    tramites = Tramite.query.order_by(Tramite.id.desc()).paginate(page=page, per_page=20)
    return render_template('dashboard_oficial.html', tramites=tramites.items, pagination=tramites)

@main_bp.route('/tramite/nuevo', methods=['POST'])
@login_required
def nuevo_tramite():
    if current_user.rol != 'pasajero':
        return redirect(url_for('main.login'))
        
    nombre = request.form.get('nombre')
    documento = request.form.get('documento')
    patente = request.form.get('patente')
    origen = request.form.get('origen')
    destino = request.form.get('destino')
    bienes = request.form.get('bienes')
    

    if not all([nombre, documento, patente, origen, destino]):
        flash('Por favor complete todos los campos obligatorios.', 'error')
        return redirect(url_for('main.dashboard_pasajero'))
    
    try:
        nuevo = Tramite(
            user_id=current_user.id,
            nombre_pasajero=nombre,
            documento=documento,
            patente=patente,
            origen=origen,
            destino=destino,
            bienes_declarados=bienes
        )
        db.session.add(nuevo)
        db.session.commit()
        current_app.logger.info(f"Trámite creado exitosamente por pasajero {current_user.rut}.")
        flash('Trámite iniciado exitosamente. Las autoridades revisarán su solicitud.', 'success')
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error al crear trámite: {e}")
        flash('Ocurrió un error al intentar crear el trámite. Verifique sus datos o intente más tarde.', 'error')
        
    return redirect(url_for('main.dashboard_pasajero'))

@main_bp.route('/tramite/actualizar/<int:id>/<estado>', methods=['POST'])
@login_required
def actualizar_tramite(id, estado):
    if current_user.rol == 'pasajero':
        return redirect(url_for('main.login'))
        
    try:
        tramite = Tramite.query.get_or_404(id)
        if current_user.rol == 'pdi':
            tramite.estado_pdi = estado
        elif current_user.rol == 'policia_arg':
            tramite.estado_policia_arg = estado
        elif current_user.rol == 'aduana':
            tramite.estado_aduana = estado
            
        db.session.commit()
        current_app.logger.info(f"Trámite #{id} actualizado a estado '{estado}' por usuario {current_user.rut} ({current_user.rol}).")
        flash(f'Trámite #{id} marcado como {estado}', 'success')
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error al actualizar trámite #{id}: {e}")
        flash('Error al intentar actualizar el trámite.', 'error')
        
    return redirect(url_for(f'main.dashboard_{current_user.rol}'))
