from database import obtener_conexion


def validar_usuario(usuario, password):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT id, usuario, nombre
        FROM usuarios
        WHERE usuario = ? AND password = ?
        """,
        (usuario, password)
    )

    resultado = cursor.fetchone()

    conexion.close()

    return resultado