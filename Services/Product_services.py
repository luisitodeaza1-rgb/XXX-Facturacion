from database import obtener_conexion


def obtener_productos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, codigo, nombre, precio, stock
        FROM productos
        ORDER BY id DESC
    """)

    productos = cursor.fetchall()

    conexion.close()

    return productos


def obtener_producto(producto_id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, codigo, nombre, precio, stock
        FROM productos
        WHERE id = ?
    """, (producto_id,))

    producto = cursor.fetchone()

    conexion.close()

    return producto


def crear_producto(codigo, nombre, precio, stock):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO productos
        (codigo, nombre, precio, stock)
        VALUES (?, ?, ?, ?)
    """, (
        codigo,
        nombre,
        precio,
        stock
    ))

    conexion.commit()
    conexion.close()


def actualizar_producto(
    producto_id,
    codigo,
    nombre,
    precio,
    stock
):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        UPDATE productos
        SET
            codigo = ?,
            nombre = ?,
            precio = ?,
            stock = ?
        WHERE id = ?
    """, (
        codigo,
        nombre,
        precio,
        stock,
        producto_id
    ))

    conexion.commit()
    conexion.close()


def eliminar_producto(producto_id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        DELETE FROM productos
        WHERE id = ?
    """, (producto_id,))

    conexion.commit()
    conexion.close()


def buscar_productos(texto):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    texto_busqueda = f"%{texto}%"

    cursor.execute("""
        SELECT id, codigo, nombre, precio, stock
        FROM productos
        WHERE
            codigo LIKE ?
            OR nombre LIKE ?
        ORDER BY id DESC
    """, (
        texto_busqueda,
        texto_busqueda
    ))

    productos = cursor.fetchall()

    conexion.close()

    return productos