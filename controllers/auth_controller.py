from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.models import Usuario

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']
        
        user = Usuario.get_by_username(usuario)
        
        if user and user['password'] == password:
            session['user_id'] = user['id']
            session['usuario'] = user['usuario']
            session['es_admin'] = user['administrador']
            flash('¡Inicio de sesión exitoso!', 'success')
            return redirect(url_for('dashboard.index'))
        else:
            flash('Usuario o contraseña incorrectos.', 'danger')
    
    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    # Limpiar toda la sesión
    session.clear()

    # Evitar que el usuario use el botón "Atrás" del navegador
    response = redirect(url_for('auth.login'))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'

    flash('Sesión cerrada correctamente.', 'info')
    return response
