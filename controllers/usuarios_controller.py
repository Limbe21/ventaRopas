from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.models import Usuario

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/usuarios')
def listar():
    if not session.get('es_admin'):
        flash('No tienes permisos para acceder a esta página', 'danger')
        return redirect(url_for('productos.listar'))
    
    usuarios = Usuario.get_all()
    return render_template('usuarios/listar.html', usuarios=usuarios)

@usuarios_bp.route('/usuarios/agregar', methods=['GET', 'POST'])
def agregar():
    if not session.get('es_admin'):
        flash('No tienes permisos para acceder a esta página', 'danger')
        return redirect(url_for('productos.listar'))
    
    if request.method == 'POST':
        try:
            es_admin = 'administrador' in request.form
            Usuario.create(
                usuario=request.form['usuario'],
                password=request.form['password'],
                administrador=es_admin
            )
            flash('Usuario agregado correctamente', 'success')
            return redirect(url_for('usuarios.listar'))
        except Exception as e:
            flash(f'Error al agregar usuario: {str(e)}', 'danger')
    
    return render_template('usuarios/agregar.html')