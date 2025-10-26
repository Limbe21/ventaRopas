from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models.models import Entrega, Producto, Venta
from flask import send_file
from io import BytesIO
from datetime import datetime
import pandas as pd
from fpdf import FPDF
from flask import send_file, flash, redirect, url_for, request



entregas_bp = Blueprint('entregas', __name__, url_prefix='/entregas')

# Listar entregas
@entregas_bp.route('/')
def index():
    entregas = Entrega.get_all()
    return render_template('entregas/index.html', entregas=entregas)

# Crear entrega
@entregas_bp.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        venta_id = request.form.get('venta_id')
        direccion = request.form.get('direccion')
        es_envio = request.form.get('es_envio') == 'on'

        try:
            Entrega.create(venta_id, direccion, es_envio)
            flash('Entrega creada exitosamente', 'success')
            return redirect(url_for('entregas.index'))
        except Exception as e:
            flash(f'Error al crear la entrega: {e}', 'danger')
            return redirect(url_for('entregas.crear'))

    # Obtener todas las ventas para seleccionar
    ventas = Venta.get_all()
    return render_template('entregas/crear.html', ventas=ventas)

# Editar entrega
@entregas_bp.route('/editar/<int:entrega_id>', methods=['GET', 'POST'])
def editar(entrega_id):
    entrega = Entrega.get_by_id(entrega_id)
    if not entrega:
        flash('Entrega no encontrada', 'danger')
        return redirect(url_for('entregas.index'))

    if request.method == 'POST':
        direccion = request.form.get('direccion')
        es_envio = request.form.get('es_envio') == 'on'

        try:
            Entrega.update(entrega_id, direccion=direccion, es_envio=es_envio)
            flash('Entrega actualizada', 'success')
            return redirect(url_for('entregas.index'))
        except Exception as e:
            flash(f'Error al actualizar la entrega: {e}', 'danger')
            return redirect(url_for('entregas.editar', entrega_id=entrega_id))

    return render_template('entregas/editar.html', entrega=entrega)

# Eliminar entrega
@entregas_bp.route('/eliminar/<int:entrega_id>')
def eliminar(entrega_id):
    try:
        Entrega.delete(entrega_id)
        flash('Entrega eliminada', 'success')
    except Exception as e:
        flash(f'Error al eliminar entrega: {e}', 'danger')
    return redirect(url_for('entregas.index'))


@entregas_bp.route('/descargar', methods=['GET'])
def descargar():
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')

    # Convertir fechas de string a datetime
    try:
        fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d') if fecha_inicio else None
        fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d') if fecha_fin else None
    except ValueError:
        flash("Formato de fecha inválido", "danger")
        return redirect(url_for('entregas.index'))

    # Obtener todas las entregas
    entregas = Entrega.get_all()

    # Filtrar por fechas usando created_at
    if fecha_inicio_dt:
        entregas = [e for e in entregas if e['created_at'] >= fecha_inicio_dt]
    if fecha_fin_dt:
        entregas = [e for e in entregas if e['created_at'] <= fecha_fin_dt]

    # Generar PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Reporte de Entregas", ln=True, align='C')
    pdf.ln(10)

    # Encabezados de la tabla
    pdf.set_font("Arial", "B", 12)
    pdf.cell(50, 10, "Cliente", border=1)
    pdf.cell(50, 10, "Producto", border=1)
    pdf.cell(80, 10, "Dirección", border=1)
    pdf.ln()

    # Contenido de la tabla
    pdf.set_font("Arial", "", 12)
    for e in entregas:
        cliente = e['cliente']
        direccion = e['direccion']

        # Obtener nombre del producto
        producto_obj = Producto.get_by_id(e['producto_id'])
        nombre_producto = producto_obj['nombre'] if producto_obj else 'Desconocido'

        pdf.cell(50, 10, str(cliente), border=1)
        pdf.cell(50, 10, str(nombre_producto), border=1)
        pdf.cell(80, 10, str(direccion), border=1)
        pdf.ln()

    # Convertir PDF a bytes para enviar
    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    pdf_output = BytesIO(pdf_bytes)
    pdf_output.seek(0)

    return send_file(pdf_output, download_name="entregas.pdf", as_attachment=True)
