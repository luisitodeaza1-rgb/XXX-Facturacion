from database import obtener_conexion


def obtener_clientes():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, nombre, rnc, telefono, email, direccion
        FROM clientes
        ORDER BY id DESC
    """)

    clientes = cursor.fetchall()

    conexion.close()

    return clientes


def obtener_cliente(cliente_id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, nombre, rnc, telefono, email, direccion
        FROM clientes
        WHERE id = ?
    """, (cliente_id,))

    cliente = cursor.fetchone()

    conexion.close()

    return cliente


def obtener_cliente_por_rnc(rnc):

    rnc = (
        rnc
        .replace("-", "")
        .replace(" ", "")
        .strip()
    )

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, nombre, rnc, telefono, email, direccion
        FROM clientes
        WHERE REPLACE(REPLACE(rnc, '-', ''), ' ', '') = ?
    """, (rnc,))

    cliente = cursor.fetchone()

    conexion.close()

    return cliente


def crear_cliente(
    nombre,
    rnc,
    telefono="",
    email="",
    direccion=""
):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO clientes
        (nombre, rnc, telefono, email, direccion)
        VALUES (?, ?, ?, ?, ?)
    """, (
        nombre,
        rnc,
        telefono,
        email,
        direccion
    ))

    cliente_id = cursor.lastrowid

    conexion.commit()
    conexion.close()

    return cliente_id


def actualizar_cliente(
    cliente_id,
    nombre,
    rnc,
    telefono,
    email,
    direccion
):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        UPDATE clientes
        SET
            nombre = ?,
            rnc = ?,
            telefono = ?,
            email = ?,
            direccion = ?
        WHERE id = ?
    """, (
        nombre,
        rnc,
        telefono,
        email,
        direccion,
        cliente_id
    ))

    conexion.commit()
    conexion.close()


def eliminar_cliente(cliente_id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        DELETE FROM clientes
        WHERE id = ?
    """, (cliente_id,))

    conexion.commit()
    conexion.close()


def buscar_clientes(texto):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    texto_busqueda = f"%{texto}%"

    cursor.execute("""
        SELECT id, nombre, rnc, telefono, email, direccion
        FROM clientes
        WHERE
            nombre LIKE ?
            OR rnc LIKE ?
            OR telefono LIKE ?
            OR email LIKE ?
        ORDER BY id DESC
    """, (
        texto_busqueda,
        texto_busqueda,
        texto_busqueda,
        texto_busqueda
    ))

    clientes = cursor.fetchall()

    conexion.close()

    return clientes