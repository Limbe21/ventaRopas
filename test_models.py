from models.models import Usuario, Producto, Venta, Entrega
from models.database import Database
from datetime import datetime

# --- FUNCIONES AUXILIARES ---
def clean_user(username):
    conn = Database.get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM usuarios WHERE usuario = %s", (username,))
    conn.commit()
    cur.close()
    conn.close()

def clean_product(nombre):
    conn = Database.get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM productos WHERE nombre = %s", (nombre,))
    conn.commit()
    cur.close()
    conn.close()

def clean_venta(cliente):
    conn = Database.get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM ventas WHERE cliente = %s", (cliente,))
    conn.commit()
    cur.close()
    conn.close()

def clean_entrega(cliente):
    conn = Database.get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM entregas WHERE cliente = %s", (cliente,))
    conn.commit()
    cur.close()
    conn.close()

# --- USUARIO ---
print("🔹 Probando USUARIOS")
clean_user("admin_test")  # eliminar si existe
Usuario.create("admin_test", "1234", True)
usuarios = Usuario.get_all()
print("Usuarios:", usuarios)

# --- PRODUCTO ---
print("\n🔹 Probando PRODUCTOS")
clean_product("Camiseta Test")  # eliminar si existe
Producto.create("Camiseta Test", "Ropa", 25.50, 10, "M", "Camiseta de algodón de prueba")
productos = Producto.get_all()
print("Productos:", productos)

# --- VENTA ---
print("\n🔹 Probando VENTAS")
clean_venta("Cliente Test")
producto_id = productos[-1]['id']  # usar último producto creado
Venta.create(producto_id, "Cliente Test", 2, 51.0, 51.0, 0.0, datetime.now(), entregado=False)
ventas = Venta.get_all()
print("Ventas:", ventas)

# Actualizar venta
venta_id = ventas[-1]['id']
Venta.update(venta_id, producto_id, "Cliente Test", 3, 76.5, 76.5, 0.0)
ventas = Venta.get_all()
print("Ventas después de actualizar:", ventas)

# --- ENTREGA ---
print("\n🔹 Probando ENTREGAS")
clean_entrega("Cliente Test")
Entrega.create(venta_id, "Calle Falsa 123", es_envio=True)
entregas = Entrega.get_all()
print("Entregas:", entregas)

# Actualizar entrega
entrega_id = entregas[-1]['id']
Entrega.update(entrega_id, direccion="Avenida Siempre Viva 742", es_envio=False)
entregas = Entrega.get_all()
print("Entregas después de actualizar:", entregas)

# --- LIMPIEZA FINAL ---
print("\n🔹 Limpiando registros de prueba")
clean_entrega("Cliente Test")
clean_venta("Cliente Test")
clean_product("Camiseta Test")
clean_user("admin_test")
print("✅ Prueba completa realizada y registros de prueba eliminados.")
