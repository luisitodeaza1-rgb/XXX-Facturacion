import tkinter as tk

from database import inicializar_base_de_datos
from views.login import Login


def main():

    print("Iniciando XXX Facturador...")

    # Inicializar base de datos
    inicializar_base_de_datos()

    print("Base de datos OK")

    # Crear ventana
    root = tk.Tk()

    root.title("XXX Facturador - Login")
    root.geometry("400x350")
    root.resizable(False, False)

    print("Ventana de Login creada")

    # Cargar Login
    Login(root)

    print("Login cargado")

    # Mantener aplicación abierta
    root.mainloop()


if __name__ == "__main__":
    main()