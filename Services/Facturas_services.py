from database import obtener_conexion


def obtener_clientes_para_factura():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, nombre, rnc
        FROM clientes
        ORDER BY nombre ASC
    """)

    clientes = cursor.fetchall()

    conexion.close()

    return clientes


def obtener_productos_para_factura():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, codigo, nombre, precio, stock
        FROM productos
        WHERE stock > 0
        ORDER BY nombre ASC
    """)

    productos = cursor.fetchall()

    conexion.close()

    return productos


def obtener_producto_por_id(producto_id):

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


def generar_numero_factura():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT numero
        FROM facturas
        ORDER BY id DESC
        LIMIT 1
    """)

    ultima_factura = cursor.fetchone()

    conexion.close()

    if not ultima_factura:

        return "F-000001"

    numero_actual = ultima_factura[0]

    try:

        numero = int(
            numero_actual.replace("F-", "")
        )

        siguiente = numero + 1

        return f"F-{siguiente:06d}"

    except ValueError:

        return "F-000001"


def crear_factura(
    cliente_id,
    items,
    itbis_porcentaje=0.18
):

    if not items:

        raise ValueError(
            "La factura debe tener al menos un producto."
        )

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:

        subtotal = 0

        # ==========================================
        # VALIDAR PRODUCTOS Y CALCULAR SUBTOTAL
        # ==========================================

        for item in items:

            producto_id = item["producto_id"]
            cantidad = item["cantidad"]

            cursor.execute("""
                SELECT id, nombre, precio, stock
                FROM productos
                WHERE id = ?
            """, (producto_id,))

            producto = cursor.fetchone()

            if not producto:

                raise ValueError(
                    f"El producto con ID {producto_id} no existe."
                )

            precio = float(producto[2])
            stock = int(producto[3])

            if cantidad <= 0:

                raise ValueError(
                    f"La cantidad del producto '{producto[1]}' debe ser mayor que 0."
                )

            if cantidad > stock:

                raise ValueError(
                    f"No hay suficiente stock de '{producto[1]}'. "
                    f"Stock disponible: {stock}."
                )

            item_subtotal = precio * cantidad

            item["precio"] = precio
            item["subtotal"] = item_subtotal

            subtotal += item_subtotal

        # ==========================================
        # CALCULAR ITBIS
        # ==========================================

        itbis = subtotal * itbis_porcentaje

        total = subtotal + itbis

        # ==========================================
        # GENERAR NÚMERO
        # ==========================================

        numero_factura = generar_numero_factura()

        # ==========================================
        # FECHA
        # ==========================================

        from datetime import datetime

        fecha = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # ==========================================
        # GUARDAR FACTURA
        # ==========================================

        cursor.execute("""
            INSERT INTO facturas
            (
                numero,
                cliente_id,
                fecha,
                subtotal,
                itbis,
                total
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            numero_factura,
            cliente_id,
            fecha,
            subtotal,
            itbis,
            total
        ))

        factura_id = cursor.lastrowid

        # ==========================================
        # GUARDAR DETALLE Y DESCONTAR STOCK
        # ==========================================

        for item in items:

            producto_id = item["producto_id"]
            cantidad = item["cantidad"]
            precio = item["precio"]
            item_subtotal = item["subtotal"]

            cursor.execute("""
                INSERT INTO detalle_factura
                (
                    factura_id,
                    producto_id,
                    cantidad,
                    precio,
                    subtotal
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                factura_id,
                producto_id,
                cantidad,
                precio,
                item_subtotal
            ))

            cursor.execute("""
                UPDATE productos
                SET stock = stock - ?
                WHERE id = ?
            """, (
                cantidad,
                producto_id
            ))

        conexion.commit()

        return {
            "id": factura_id,
            "numero": numero_factura,
            "fecha": fecha,
            "subtotal": subtotal,
            "itbis": itbis,
            "total": total
        }

    except Exception:

        conexion.rollback()

        raise

    finally:

        conexion.close()