import sqlite3
from pathlib import Path


CARPETA_DATABASE = Path(__file__).parent / "database"
RUTA_DATABASE = CARPETA_DATABASE / "facturacion.db"


def obtener_conexion():

    CARPETA_DATABASE.mkdir(
        exist_ok=True
    )

    conexion = sqlite3.connect(
        RUTA_DATABASE
    )

    return conexion


def inicializar_base_de_datos():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # ==========================================
    # USUARIOS
    # ==========================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            nombre TEXT
        )
    """)

    # ==========================================
    # CLIENTES
    # ==========================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            rnc TEXT,
            telefono TEXT,
            email TEXT,
            direccion TEXT
        )
    """)

    # ==========================================
    # PRODUCTOS
    # ==========================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER DEFAULT 0
        )
    """)

    # ==========================================
    # FACTURAS
    # ==========================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS facturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero TEXT UNIQUE,
            cliente_id INTEGER,
            cliente_nombre TEXT,
            cliente_rnc TEXT,
            fecha TEXT NOT NULL,
            subtotal REAL NOT NULL,
            itbis REAL NOT NULL,
            total REAL NOT NULL,
            FOREIGN KEY (cliente_id)
                REFERENCES clientes(id)
        )
    """)

    # ==========================================
    # MIGRACIÓN DE FACTURAS EXISTENTES
    # ==========================================

    cursor.execute("""
        PRAGMA table_info(facturas)
    """)

    columnas_facturas = {
        columna[1]
        for columna in cursor.fetchall()
    }

    if "cliente_nombre" not in columnas_facturas:

        cursor.execute("""
            ALTER TABLE facturas
            ADD COLUMN cliente_nombre TEXT
        """)

    if "cliente_rnc" not in columnas_facturas:

        cursor.execute("""
            ALTER TABLE facturas
            ADD COLUMN cliente_rnc TEXT
        """)

    # ==========================================
    # DETALLE DE FACTURA
    # ==========================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detalle_factura (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            factura_id INTEGER NOT NULL,
            producto_id INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL,
            subtotal REAL NOT NULL,
            FOREIGN KEY (factura_id)
                REFERENCES facturas(id),
            FOREIGN KEY (producto_id)
                REFERENCES productos(id)
        )
    """)

    # ==========================================
    # CONFIGURACIÓN
    # ==========================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS configuracion (
            id INTEGER PRIMARY KEY,
            nombre_empresa TEXT,
            rnc TEXT,
            telefono TEXT,
            email TEXT,
            direccion TEXT
        )
    """)

    conexion.commit()
    conexion.close()

    print(
        "Base de datos inicializada correctamente."
    )