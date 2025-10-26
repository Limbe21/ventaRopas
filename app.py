from flask import Flask, request, session, redirect, url_for, flash
from config import Config
from controllers.auth_controller import auth_bp
from controllers.productos_controller import productos_bp
from controllers.usuarios_controller import usuarios_bp
from controllers.ventas_controller import ventas_bp
from controllers.dashboard_bp import dashboard_bp
from controllers.entregas_controller import entregas_bp
app = Flask(__name__)
app.config.from_object(Config)

# Registrar blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(productos_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(ventas_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(entregas_bp)

#Seguriad de q
@app.before_request
def require_login():
    rutas_publicas = ['auth.login', 'auth.logout', 'static']

    endpoint = request.endpoint  # puede ser None

    # Si el endpoint no existe, salir sin hacer nada
    if endpoint is None:
        return

    # Si el usuario no tiene sesión y no está accediendo a rutas públicas
    if 'user_id' not in session:
        # Si el endpoint no es público ni estático, redirigir al login
        if endpoint not in rutas_publicas and not endpoint.startswith('static'):
            return redirect(url_for('auth.login'))



# Página principal redirige al dashboard
@app.route('/')
def index():
    return redirect(url_for('dashboard.index'))


if __name__ == '__main__':
    app.run(debug=True)
