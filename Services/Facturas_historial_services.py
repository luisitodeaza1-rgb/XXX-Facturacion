from database import obtener_conexion


def obtener_facturas():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            f.id,
            f.numero,
            COALESCE(f.cliente_nombre, c.nombre, ''),
            COALESCE(f.cliente_rnc, c.rnc, ''),
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
            COALESCE(f.cliente_nombre, c.nombre, ''),
            COALESCE(f.cliente_rnc, c.rnc, ''),
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
            COALESCE(f.cliente_nombre, c.nombre, ''),
            COALESCE(f.cliente_rnc, c.rnc, ''),
            f.fecha,
            f.subtotal,
            f.itbis,
            f.total
        FROM facturas f
        LEFT JOIN clientes c
            ON f.cliente_id = c.id
        WHERE
            f.numero LIKE ?
            OR COALESCE(f.cliente_nombre, c.nombre, '') LIKE ?
            OR COALESCE(f.cliente_rnc, c.rnc, '') LIKE ?
        ORDER BY f.id DESC
    """, (
        texto_busqueda,
        texto_busqueda,
        texto_busqueda
    ))

    facturas = cursor.fetchall()

    conexion.close()

    return facturas


def obtener_totales_facturas():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            COUNT(*),
            COALESCE(SUM(subtotal), 0),
            COALESCE(SUM(itbis), 0),
            COALESCE(SUM(total), 0)
        FROM facturas
    """)

    totales = cursor.fetchone()

    conexion.close()

    return totales


def eliminar_factura(factura_id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:

        # ==========================================
        # VERIFICAR QUE LA FACTURA EXISTA
        # ==========================================

        cursor.execute("""
            SELECT id, numero
            FROM facturas
            WHERE id = ?
        """, (factura_id,))

        factura = cursor.fetchone()

        if not factura:

            raise ValueError(
                "La factura seleccionada no existe."
            )

        # ==========================================
        # OBTENER PRODUCTOS Y CANTIDADES
        # PARA DEVOLVER EL STOCK
        # ==========================================

        cursor.execute("""
            SELECT
                producto_id,
                cantidad
            FROM detalle_factura
            WHERE factura_id = ?
        """, (factura_id,))

        detalles = cursor.fetchall()

        # ==========================================
        # RESTAURAR STOCK
        # ==========================================

        for producto_id, cantidad in detalles:

            cursor.execute("""
                UPDATE productos
                SET stock = stock + ?
                WHERE id = ?
            """, (
                cantidad,
                producto_id
            ))

        # ==========================================
        # ELIMINAR DETALLE
        # ==========================================

        cursor.execute("""
            DELETE FROM detalle_factura
            WHERE factura_id = ?
        """, (factura_id,))

        # ==========================================
        # ELIMINAR FACTURA
        # ==========================================

        cursor.execute("""
            DELETE FROM facturas
            WHERE id = ?
        """, (factura_id,))

        if cursor.rowcount == 0:

            raise ValueError(
                "No fue posible eliminar la factura."
            )

        conexion.commit()

        return factura[1]

    except Exception:

        conexion.rollback()

        raise

    finally:

        conexion.close()