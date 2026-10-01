from database import obtener_conexion


def obtener_facturas():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            f.id,
            f.numero,
            c.nombre,
            c.rnc,
            f.fecha,
            f.subtotal,
            f.itbis,
            f.total
        FROM facturas f
        LEFT JOIN clientes c
            ON f.cliente_id = c.id
        ORDER BY f.id DESC
    """)

    facturas = cursor.fetchall()

    conexion.close()

    return facturas


def obtener_factura(factura_id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            f.id,
            f.numero,
            c.nombre,
            c.rnc,
            f.fecha,
            f.subtotal,
            f.itbis,
            f.total
        FROM facturas f
        LEFT JOIN clientes c
            ON f.cliente_id = c.id
        WHERE f.id = ?
    """, (factura_id,))

    factura = cursor.fetchone()

    conexion.close()

    return factura


def obtener_detalle_factura(factura_id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            p.codigo,
            p.nombre,
            df.cantidad,
            df.precio,
            df.subtotal
        FROM detalle_factura df
        INNER JOIN productos p
            ON df.producto_id = p.id
        WHERE df.factura_id = ?
        ORDER BY df.id ASC
    """, (factura_id,))

    detalle = cursor.fetchall()

    conexion.close()

    return detalle


def buscar_facturas(texto):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    texto_busqueda = f"%{texto}%"

    cursor.execute("""
        SELECT
            f.id,
            f.numero,
            c.nombre,
            c.rnc,
            f.fecha,
            f.subtotal,
            f.itbis,
            f.total
        FROM facturas f
        LEFT JOIN clientes c
            ON f.cliente_id = c.id
        WHERE
            f.numero LIKE ?
            OR c.nombre LIKE ?
            OR c.rnc LIKE ?
        ORDER BY f.id DESC
    """, (
        texto_busqueda,
        texto_busqueda,
        texto_busqueda
    ))

    facturas = cursor.fetchall()

    conexion.close()

    return facturas