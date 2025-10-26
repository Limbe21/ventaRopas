from .database import Database
from psycopg2.extras import RealDictCursor

class Usuario:
    @staticmethod
    def get_all():
        conn = Database.get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('SELECT * FROM usuarios ORDER BY id')
        usuarios = cur.fetchall()
        cur.close()
        conn.close()
        return usuarios

    @staticmethod
    def get_by_username(usuario):
        conn = Database.get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('SELECT * FROM usuarios WHERE usuario = %s', (usuario,))
        usuario_data = cur.fetchone()
        cur.close()
        conn.close()
        return usuario_data

    @staticmethod
    def create(usuario, password, administrador=False):
        conn = Database.get_connection()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO usuarios (usuario, password, administrador)
            VALUES (%s, %s, %s)
        ''', (usuario, password, administrador))
        conn.commit()
        cur.close()
        conn.close()

class Producto:
    @staticmethod
    def get_all():
        conn = Database.get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('SELECT * FROM productos ORDER BY id')
        productos = cur.fetchall()
        cur.close()
        conn.close()
        return productos

    @staticmethod
    def get_by_id(producto_id):
        conn = Database.get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('SELECT * FROM productos WHERE id = %s', (producto_id,))
        producto = cur.fetchone()
        cur.close()
        conn.close()
        return producto

    @staticmethod
    def create(nombre, categoria, precio, cantidad, talla, descripcion):
        conn = Database.get_connection()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO productos (nombre, categoria, precio, cantidad, talla, descripcion)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (nombre, categoria, precio, cantidad, talla, descripcion))
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def update(producto_id, nombre, categoria, precio, cantidad, talla, descripcion):
        conn = Database.get_connection()
        cur = conn.cursor()
        cur.execute('''
            UPDATE productos 
            SET nombre=%s, categoria=%s, precio=%s, cantidad=%s, talla=%s, descripcion=%s
            WHERE id=%s
        ''', (nombre, categoria, precio, cantidad, talla, descripcion, producto_id))
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def delete(producto_id):
        conn = Database.get_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM productos WHERE id = %s', (producto_id,))
        conn.commit()
        cur.close()
        conn.close()


class Venta:

    @staticmethod
    def update(venta_id, producto_id, cliente, cantidad_vendida, total, pago, falta):
        """
        Actualizar una venta existente
        """
        conn = Database.get_connection()
        cur = conn.cursor()
        cur.execute('''
            UPDATE ventas 
            SET producto_id = %s, cliente = %s, cantidad_vendida = %s, 
                total = %s, pago = %s, falta = %s
            WHERE id = %s
        ''', (producto_id, cliente, cantidad_vendida, total, pago, falta, venta_id))
        conn.commit()
        cur.close()
        conn.close()
        
    @staticmethod
    def get_all():
        conn = Database.get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('''
            SELECT v.*, p.nombre AS producto_nombre, p.cantidad AS stock_actual
            FROM ventas v
            LEFT JOIN productos p ON v.producto_id = p.id
            ORDER BY v.fecha DESC
        ''')
        ventas = cur.fetchall()
        cur.close()
        conn.close()
        return ventas
 
    @staticmethod
    def get_by_id(venta_id):
        conn = Database.get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('SELECT * FROM ventas WHERE id=%s', (venta_id,))
        venta = cur.fetchone()
        cur.close()
        conn.close()
        return venta

    @staticmethod
    def create(producto_id, cliente, cantidad_vendida, total, pago, falta, fecha, entregado=False):
        """
        Crear una nueva venta. Por defecto, 'entregado' será False.
        """
        conn = Database.get_connection()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO ventas (producto_id, cliente, cantidad_vendida, total, pago, falta, fecha, entregado)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (producto_id, cliente, cantidad_vendida, total, pago, falta, fecha, entregado))
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def delete(venta_id):
        conn = Database.get_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM ventas WHERE id=%s', (venta_id,))
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def update_entregado(venta_id, entregado):
        """
        Actualiza el estado de entrega de una venta.
        """
        conn = Database.get_connection()
        cur = conn.cursor()
        cur.execute(
            'UPDATE ventas SET entregado = %s WHERE id = %s',
            (entregado, venta_id)
        )
        conn.commit()
        cur.close()
        conn.close()


class Entrega:
    @staticmethod
    def create(venta_id, direccion, es_envio=False):
        """
        Crear una nueva entrega a partir de una venta existente.
        """
        # Obtener la venta y el producto
        venta = Venta.get_by_id(venta_id)
        if not venta:
            raise ValueError(f"No se encontró la venta con id {venta_id}")
        
        producto_id = venta.get('producto_id')
        cliente = venta.get('cliente')  # nombre del cliente

        conn = Database.get_connection()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO entregas (cliente, producto_id, direccion, es_envio, venta_id)
            VALUES (%s, %s, %s, %s, %s)
        ''', (cliente, producto_id, direccion, es_envio, venta_id))
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def get_all():
        """
        Obtener todas las entregas con nombre del producto y cliente
        """
        conn = Database.get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('''
            SELECT e.*, p.nombre AS producto_nombre
            FROM entregas e
            LEFT JOIN productos p ON e.producto_id = p.id
            ORDER BY e.id DESC
        ''')
        entregas = cur.fetchall()
        cur.close()
        conn.close()
        return entregas

    @staticmethod
    def get_by_id(entrega_id):
        conn = Database.get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('SELECT * FROM entregas WHERE id = %s', (entrega_id,))
        entrega = cur.fetchone()
        cur.close()
        conn.close()
        return entrega

    @staticmethod
    def update(entrega_id, direccion=None, es_envio=None):
        """
        Actualizar una entrega: dirección o tipo de envío
        """
        conn = Database.get_connection()
        cur = conn.cursor()
        
        fields = []
        values = []
        if direccion is not None:
            fields.append("direccion=%s")
            values.append(direccion)
        if es_envio is not None:
            fields.append("es_envio=%s")
            values.append(es_envio)
        
        values.append(entrega_id)
        sql = f"UPDATE entregas SET {', '.join(fields)} WHERE id=%s"
        cur.execute(sql, tuple(values))
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def delete(entrega_id):
        conn = Database.get_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM entregas WHERE id = %s', (entrega_id,))
        conn.commit()
        cur.close()
        conn.close()