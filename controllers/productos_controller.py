from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models.models import Producto

productos_bp = Blueprint('productos', __name__)

@productos_bp.route('/')
@productos_bp.route('/productos')
def listar():
    productos = Producto.get_all()
    return render_template('productos/listar.html', productos=productos)

@productos_bp.route('/productos/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        try:
            Producto.create(
                nombre=request.form['nombre'],
                categoria=request.form['categoria'],
                precio=float(request.form['precio']),
                cantidad=int(request.form['cantidad']),
                talla=request.form['talla'],
                descripcion=request.form['descripcion']
            )
            flash('Producto agregado correctamente', 'success')
            return redirect(url_for('productos.listar'))
        except Exception as e:
            flash(f'Error al agregar producto: {str(e)}', 'danger')
    
    return render_template('productos/agregar.html')

@productos_bp.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    producto = Producto.get_by_id(id)
    
    if not producto:
        flash('Producto no encontrado', 'danger')
        return redirect(url_for('productos.listar'))
    
    if request.method == 'POST':
        try:
            Producto.update(
                producto_id=id,
                nombre=request.form['nombre'],
                categoria=request.form['categoria'],
                precio=float(request.form['precio']),
                cantidad=int(request.form['cantidad']),
                talla=request.form['talla'],
                descripcion=request.form['descripcion']
            )
            flash('Producto actualizado correctamente', 'success')
            return redirect(url_for('productos.listar'))
        except Exception as e:
            flash(f'Error al actualizar producto: {str(e)}', 'danger')
    
    return render_template('productos/editar.html', producto=producto)

@productos_bp.route('/productos/eliminar/<int:id>')
def eliminar(id):
    try:
        Producto.delete(id)
        flash('Producto eliminado correctamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar producto: {str(e)}', 'danger')
    
    return redirect(url_for('productos.listar'))