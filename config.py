import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Configuración para la base de datos MySQL
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'root')
    MYSQL_DB = os.getenv('MYSQL_DB', 'perfil_db')
    MYSQL_PORT = os.getenv('MYSQL_PORT', 3306)
