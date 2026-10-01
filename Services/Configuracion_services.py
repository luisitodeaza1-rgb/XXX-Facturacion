from database import obtener_conexion


def obtener_configuracion():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id,
            nombre_empresa,
            rnc,
            telefono,
            email,
            direccion
        FROM configuracion
        WHERE id = 1
    """)

    configuracion = cursor.fetchone()

    conexion.close()

    return configuracion


def guardar_configuracion(
    nombre_empresa,
    rnc,
    telefono,
    email,
    direccion
):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO configuracion
        (
            id,
            nombre_empresa,
            rnc,
            telefono,
            email,
            direccion
        )
        VALUES (1, ?, ?, ?, ?, ?)
        ON CONFLICT(id)
        DO UPDATE SET
            nombre_empresa = excluded.nombre_empresa,
            rnc = excluded.rnc,
            telefono = excluded.telefono,
            email = excluded.email,
            direccion = excluded.direccion
    """, (
        nombre_empresa,
        rnc,
        telefono,
        email,
        direccion
    ))

    conexion.commit()
    conexion.close()