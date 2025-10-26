import os

class Config:
    # Clave secreta para sesiones
    SECRET_KEY = os.environ.get('SECRET_KEY', 'tu-clave-secreta-muy-segura-aqui')

    # Conexión a la base de datos
    # Si existe la variable de entorno DATABASE_URL (Render), úsala
    if os.environ.get("DATABASE_URL"):
        SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    else:
        # Configuración local
        DB_HOST = 'localhost'
        DB_NAME = 'Tienda_Ropas'
        DB_USER = 'postgres'
        DB_PASSWORD = '123123123'
        DB_PORT = '5432'
        SQLALCHEMY_DATABASE_URI = (
            f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
