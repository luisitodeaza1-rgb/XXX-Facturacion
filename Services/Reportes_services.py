from database import obtener_conexion


def obtener_resumen():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM facturas
    """)

    total_facturas = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COALESCE(SUM(total), 0)
        FROM facturas
    """)

    total_ventas = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM clientes
    """)

    total_clientes = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM productos
    """)

    total_productos = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COALESCE(SUM(stock), 0)
        FROM productos
    """)

    unidades_stock = cursor.fetchone()[0]

    conexion.close()

    return {
        "facturas": total_facturas,
        "ventas": total_ventas,
        "clientes": total_clientes,
        "productos": total_productos,
        "stock": unidades_stock
    }


def obtener_ventas_por_dia():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            DATE(fecha) AS dia,
            COUNT(*) AS facturas,
            COALESCE(SUM(total), 0) AS ventas
        FROM facturas
        GROUP BY DATE(fecha)
        ORDER BY dia DESC
        LIMIT 30
    """)

    resultados = cursor.fetchall()

    conexion.close()

    return resultados


def obtener_productos_mas_vendidos():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            p.nombre,
            SUM(df.cantidad) AS cantidad,
            SUM(df.subtotal) AS ventas
        FROM detalle_factura df
        INNER JOIN productos p
            ON df.producto_id = p.id
        GROUP BY p.id, p.nombre
        ORDER BY cantidad DESC
        LIMIT 10
    """)

    resultados = cursor.fetchall()

    conexion.close()

    return resultados