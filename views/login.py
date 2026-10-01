import tkinter as tk
from tkinter import messagebox

from Services.auth_service import validar_usuario
from views.dashboard import Dashboard


class Login:

    def __init__(self, root):

        self.root = root

        self.root.title("XXX Facturador - Login")
        self.root.geometry("400x350")
        self.root.resizable(False, False)

        # ==========================================
        # TÍTULO
        # ==========================================

        titulo = tk.Label(
            self.root,
            text="XXX FACTURADOR",
            font=("Arial", 24, "bold")
        )

        titulo.pack(pady=30)

        # ==========================================
        # USUARIO
        # ==========================================

        tk.Label(
            self.root,
            text="Usuario",
            font=("Arial", 11)
        ).pack()

        self.usuario = tk.Entry(
            self.root,
            width=30
        )

        self.usuario.pack(pady=5)

        # ==========================================
        # CONTRASEÑA
        # ==========================================

        tk.Label(
            self.root,
            text="Contraseña",
            font=("Arial", 11)
        ).pack()

        self.password = tk.Entry(
            self.root,
            width=30,
            show="*"
        )

        self.password.pack(pady=5)

        # ==========================================
        # BOTÓN INICIAR SESIÓN
        # ==========================================

        boton = tk.Button(
            self.root,
            text="INICIAR SESIÓN",
            width=20,
            command=self.iniciar_sesion
        )

        boton.pack(pady=25)

    # ==========================================
    # VALIDAR LOGIN
    # ==========================================

    def iniciar_sesion(self):

        usuario = self.usuario.get().strip()
        password = self.password.get()

        print("BOTÓN PRESIONADO")
        print("Usuario:", usuario)
        print("Contraseña recibida:", password)

        # ==========================================
        # VALIDAR CAMPOS
        # ==========================================

        if not usuario or not password:

            messagebox.showwarning(
                "Campos vacíos",
                "Debe introducir usuario y contraseña."
            )

            return

        # ==========================================
        # CONSULTAR BASE DE DATOS
        # ==========================================

        try:

            resultado = validar_usuario(
                usuario,
                password
            )

            print("Resultado de la consulta:", resultado)

            # ==========================================
            # LOGIN CORRECTO
            # ==========================================

            if resultado:

                print("Usuario válido.")
                print("Abriendo Dashboard...")

                # Limpiar la ventana actual
                # para convertirla en Dashboard.

                for widget in self.root.winfo_children():
                    widget.destroy()

                # Cambiar tamaño de la ventana

                self.root.geometry("1100x650")
                self.root.minsize(900, 550)
                self.root.resizable(True, True)

                # Crear Dashboard

                Dashboard(
                    self.root,
                    resultado[2]
                )

                print("Dashboard cargado correctamente.")

            # ==========================================
            # LOGIN INCORRECTO
            # ==========================================

            else:

                print("Usuario o contraseña incorrectos.")

                messagebox.showerror(
                    "Acceso denegado",
                    "Usuario o contraseña incorrectos."
                )

        # ==========================================
        # ERROR
        # ==========================================

        except Exception as error:

            print("ERROR:", error)

            messagebox.showerror(
                "Error",
                f"Ocurrió un error:\n\n{error}"
            )