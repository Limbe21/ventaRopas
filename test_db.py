from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from sqlalchemy import text  # <-- Importar text

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

try:
    with app.app_context():
        # Usar text() para consultas SQL crudas
        db.session.execute(text("SELECT 1"))
    print("✅ Conexión a la base de datos exitosa")
except Exception as e:
    print("❌ Error de conexión:", e)
