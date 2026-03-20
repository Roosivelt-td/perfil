import mysql.connector
from config import Config

class Database:
    def __init__(self):
        self.config = Config()
        self.init_db()

    def get_connection(self):
        """Crea una conexión a la base de datos MySQL"""
        return mysql.connector.connect(
            host=self.config.MYSQL_HOST,
            user=self.config.MYSQL_USER,
            password=self.config.MYSQL_PASSWORD,
            database=self.config.MYSQL_DB
        )

    def init_db(self):
        """Crea la base de datos y las tablas si no existen"""
        try:
            # Conexión inicial para crear DB
            conn = mysql.connector.connect(
                host=self.config.MYSQL_HOST,
                user=self.config.MYSQL_USER,
                password=self.config.MYSQL_PASSWORD
            )
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.config.MYSQL_DB}")
            conn.close()

            # Conectar a la DB y crear tablas
            conn = self.get_connection()
            cursor = conn.cursor()

            # --- TABLAS DE PERFIL ---
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS perfil (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    titulo VARCHAR(100),
                    fecha_nacimiento DATE,
                    descripcion TEXT,
                    frase_personal TEXT
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS habilidades (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    categoria VARCHAR(50),
                    nombre VARCHAR(50),
                    nivel INT
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS proyectos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(100),
                    descripcion TEXT,
                    tecnologias VARCHAR(255)
                )
            ''')

            # --- TABLA DE DOMINIOS (ADMINISTRACIÓN) ---
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS dominios (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(255) NOT NULL,
                    link VARCHAR(255),
                    fecha_registro DATE,
                    fecha_expiracion DATE,
                    proveedor VARCHAR(100),
                    estado VARCHAR(50) DEFAULT 'activo',
                    notas TEXT
                )
            ''')

            # Insertar datos iniciales si perfil está vacío
            cursor.execute("SELECT COUNT(*) FROM perfil")
            if cursor.fetchone()[0] == 0:
                self._insert_initial_data(cursor)
                conn.commit()

            conn.close()
            print("✅ Base de datos (Perfil y Dominios) inicializada correctamente.")

        except mysql.connector.Error as err:
            print(f"❌ Error conectando a MySQL: {err}")

    def _insert_initial_data(self, cursor):
        """Inserta los datos de Roosivelt Tupia"""
        cursor.execute('''
            INSERT INTO perfil (nombre, titulo, fecha_nacimiento, descripcion, frase_personal)
            VALUES (%s, %s, %s, %s, %s)
        ''', (
            "Roosivelt Tupia Dipaz",
            "Backend Developer | Estudiante de Ingeniería de Sistemas",
            "1996-03-26",
            "Hola, soy Roosivelt Tupia Dipaz. Soy estudiante de Ingeniería de Sistemas apasionado por el desarrollo de software, especialmente en el área de backend y arquitectura de sistemas. Me interesa crear plataformas completas que integren bases de datos, lógica de negocio y aplicaciones web funcionales. He trabajado en diversos proyectos tecnológicos como sistemas de gestión agrícola, plataformas tipo marketplace y sistemas administrativos. Además, tengo interés en el funcionamiento interno de los sistemas, la infraestructura tecnológica, los servidores y la administración de dominios.",
            '"Construir sistemas completos no es solo programar, es entender cómo funciona todo el ecosistema."'
        ))

        # Habilidades
        habilidades = [
            ("Lenguajes", "Java", 80), ("Lenguajes", "Python", 75), 
            ("Lenguajes", "PHP", 70), ("Lenguajes", "JavaScript", 85),
            ("Frameworks", "Spring Boot", 80), ("Frameworks", "Laravel", 75),
            ("Frameworks", "Node.js", 80), ("Frameworks", "React Native", 70),
            ("Base de Datos", "MySQL", 85), ("Base de Datos", "PostgreSQL", 75),
            ("Herramientas", "Git", 90), ("Herramientas", "Linux/Termux", 85)
        ]
        cursor.executemany("INSERT INTO habilidades (categoria, nombre, nivel) VALUES (%s, %s, %s)", habilidades)

        # Proyectos
        proyectos = [
            ("Sistema de Gestión Agrícola", "Plataforma para administrar terrenos, procesos agrícolas, costos, insumos y ventas. Incluye gestión de usuarios, control de procesos productivos y cálculo de ganancias.", "Spring Boot, MySQL, Tailwind"),
            ("Sistema de Distribución de Bebidas", "Sistema para gestionar inventario, compras, distribución de productos, vehículos de entrega y repartidores.", "Laravel, SQLite, Bootstrap"),
            ("Plataforma Marketplace", "Aplicación web y móvil inspirada en modelos tipo marketplace donde los usuarios pueden visualizar productos, registrarse y realizar compras.", "Node.js, React Native, PostgreSQL")
        ]
        cursor.executemany("INSERT INTO proyectos (nombre, descripcion, tecnologias) VALUES (%s, %s, %s)", proyectos)

    # --- MÉTODOS PARA PERFIL ---
    def get_perfil(self):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM perfil LIMIT 1")
        res = cursor.fetchone()
        conn.close()
        return res

    def get_habilidades(self):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM habilidades")
        res = cursor.fetchall()
        conn.close()
        grouped = {}
        for h in res:
            cat = h['categoria']
            if cat not in grouped: grouped[cat] = []
            grouped[cat].append(h)
        return grouped

    def get_proyectos(self):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM proyectos")
        res = cursor.fetchall()
        conn.close()
        return res

    # --- MÉTODOS PARA DOMINIOS (ADMINISTRACIÓN) ---
    def get_all_dominios(self):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM dominios ORDER BY fecha_expiracion ASC")
        res = cursor.fetchall()
        conn.close()
        return res
    
    def add_dominio(self, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO dominios (nombre, link, fecha_registro, fecha_expiracion, proveedor, estado, notas)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (data['nombre'], data.get('link'), data['fecha_registro'], data['fecha_expiracion'], data['proveedor'], data['estado'], data.get('notas')))
        conn.commit()
        conn.close()
        return True

    def update_dominio(self, id, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE dominios SET nombre=%s, link=%s, fecha_registro=%s, fecha_expiracion=%s, proveedor=%s, estado=%s, notas=%s
            WHERE id=%s
        ''', (data['nombre'], data.get('link'), data['fecha_registro'], data['fecha_expiracion'], data['proveedor'], data['estado'], data.get('notas'), id))
        conn.commit()
        conn.close()
        return True

    def delete_dominio(self, id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM dominios WHERE id=%s", (id,))
        conn.commit()
        conn.close()
        return True
