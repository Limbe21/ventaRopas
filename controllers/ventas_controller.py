from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.models import Venta, Producto
from datetime import datetime
ventas_bp = Blueprint('ventas', __name__)

@ventas_bp.route('/ventas')
def listar():
    ventas = Venta.get_all()
    return render_template('ventas/listar.html', ventas=ventas)

@ventas_bp.route('/ventas/crear', methods=['GET', 'POST'])
def crear():
    productos = Producto.get_all()
    producto_id_preseleccionado = request.args.get('producto_id', type=int)

    if request.method == 'POST':
        try:
            producto_id = int(request.form['producto_id'])
            cantidad_vendida = int(request.form['cantidad_vendida'])

            producto = Producto.get_by_id(producto_id)
            if not producto:
                flash('Producto no existe', 'danger')
                return redirect(url_for('ventas.crear'))

            producto['cantidad'] = int(producto['cantidad'])

            # No permitir venta si stock es 0
            if producto['cantidad'] <= 0:
                flash('Producto agotado, no se puede vender', 'danger')
                return redirect(url_for('ventas.crear'))

            # No permitir vender más que el stock disponible
            if cantidad_vendida > producto['cantidad']:
                flash('No hay suficiente stock para esta venta', 'danger')
                return redirect(url_for('ventas.crear'))

            # Usar el total calculado por el frontend
            total = float(request.form.get('total', 0))
            
            # Validar que el total sea correcto
            precio_unitario = float(producto['precio'])
            total_calculado = precio_unitario * cantidad_vendida
            
            # Si el total enviado es 0 o no coincide, usar el calculado
            if total == 0 or abs(total - total_calculado) > 0.01:
                total = total_calculado

            pago = float(request.form.get('pago', total))
            falta = total - pago
# CREAR FECHA ACTUAL
            fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # Crear venta con entregado = False
            Venta.create(
                producto_id=producto_id,
                cliente=request.form['cliente'],
                cantidad_vendida=cantidad_vendida,
                total=total,
                pago=pago,
                falta=falta,
                fecha=fecha
            )

            flash('Venta registrada correctamente', 'success')
            return redirect(url_for('ventas.listar'))

        except Exception as e:
            flash(f'Error al registrar venta: {str(e)}', 'danger')

    return render_template(
        'ventas/crear.html',
        productos=productos,
        producto_id_preseleccionado=producto_id_preseleccionado
    )

@ventas_bp.route('/ventas/entregado/<int:id>')
def entregado(id):
    try:
        venta = Venta.get_by_id(id)
        if not venta:
            flash('Venta no encontrada', 'danger')
            return redirect(url_for('ventas.listar'))

        # Marcar venta como entregada
        Venta.update_entregado(id, True)

        # Actualizar stock del producto
        producto = Producto.get_by_id(venta['producto_id'])
        if producto:
            producto['cantidad'] = int(producto['cantidad'])
            nuevo_stock = producto['cantidad'] - venta['cantidad_vendida']

            if nuevo_stock > 0:
                Producto.update(
                    producto_id=producto['id'],
                    nombre=producto['nombre'],
                    categoria=producto['categoria'],
                    precio=producto['precio'],
                    cantidad=nuevo_stock,
                    talla=producto['talla'],
                    descripcion=producto['descripcion']
                )
            else:
                Producto.delete(producto['id'])
                flash('Producto agotado y eliminado del inventario', 'warning')

        flash('Venta marcada como entregada', 'success')

    except Exception as e:
        flash(f'Error al completar venta: {str(e)}', 'danger')

    return redirect(url_for('ventas.listar'))


@ventas_bp.route('/ventas/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    try:
        venta = Venta.get_by_id(id)
        if not venta:
            flash('Venta no encontrada', 'danger')
            return redirect(url_for('ventas.listar'))

        # Si quieres, también puedes devolver el stock al producto al eliminar
        producto = Producto.get_by_id(venta['producto_id'])
        if producto:
            producto['cantidad'] = int(producto['cantidad']) + venta['cantidad_vendida']
            Producto.update(
                producto_id=producto['id'],
                nombre=producto['nombre'],
                categoria=producto['categoria'],
                precio=producto['precio'],
                cantidad=producto['cantidad'],
                talla=producto['talla'],
                descripcion=producto['descripcion']
            )

        # Eliminar la venta
        Venta.delete(id)
        flash('Venta eliminada correctamente', 'success')

    except Exception as e:
        flash(f'Error al eliminar venta: {str(e)}', 'danger')

    return redirect(url_for('ventas.listar'))
@ventas_bp.route('/ventas/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    venta = Venta.get_by_id(id)
    
    if not venta:
        flash('Venta no encontrada', 'danger')
        return redirect(url_for('ventas.listar'))

    productos = Producto.get_all()

    if request.method == 'POST':
        try:
            producto_id = int(request.form['producto_id'])
            cantidad_vendida = int(request.form['cantidad_vendida'])
            cliente = request.form['cliente']

            producto = Producto.get_by_id(producto_id)
            if not producto:
                flash('Producto no existe', 'danger')
                return redirect(url_for('ventas.editar', id=id))

            producto['cantidad'] = int(producto['cantidad'])

            # Validar stock (considerando la cantidad original de la venta)
            cantidad_original = venta['cantidad_vendida']
            stock_disponible = producto['cantidad'] + cantidad_original  # Stock + lo que se devuelve

            if cantidad_vendida > stock_disponible:
                flash(f'No hay suficiente stock. Stock disponible: {stock_disponible}', 'danger')
                return redirect(url_for('ventas.editar', id=id))

            # Calcular total
            precio_unitario = float(producto['precio'])
            total = precio_unitario * cantidad_vendida
            pago = float(request.form.get('pago', total))
            falta = total - pago

            # Actualizar la venta
            Venta.update(
                venta_id=id,
                producto_id=producto_id,
                cliente=cliente,
                cantidad_vendida=cantidad_vendida,
                total=total,
                pago=pago,
                falta=falta
            )

            flash('Venta actualizada correctamente', 'success')
            return redirect(url_for('ventas.listar'))

        except Exception as e:
            flash(f'Error al actualizar venta: {str(e)}', 'danger')

    return render_template(
        'ventas/editar.html',
        venta=venta,
        productos=productos
    )