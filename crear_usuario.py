from database import obtener_conexion


def crear_usuario():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO usuarios (usuario, password, nombre)
            VALUES (?, ?, ?)
            """,
            ("admin", "1234", "Administrador")
        )

        conexion.commit()

        print("Usuario creado correctamente.")
        print("Usuario: admin")
        print("Contraseña: 1234")

    except Exception as error:
        print("No se pudo crear el usuario.")
        print(error)

    finally:
        conexion.close()


if __name__ == "__main__":
    crear_usuario()