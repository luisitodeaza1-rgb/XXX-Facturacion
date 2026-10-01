import tkinter as tk
from tkinter import messagebox

from Services.Configuracion_services import (
    obtener_configuracion,
    guardar_configuracion
)


class Configuracion:

    def __init__(self, padre):

        self.padre = padre

        self.crear_interfaz()
        self.cargar_configuracion()

    # ==========================================
    # INTERFAZ
    # ==========================================

    def crear_interfaz(self):

        titulo = tk.Label(
            self.padre,
            text="Configuración",
            font=("Arial", 26, "bold"),
            bg="#f3f4f6",
            fg="#111827"
        )

        titulo.pack(
            anchor="w",
            padx=30,
            pady=(30, 5)
        )

        subtitulo = tk.Label(
            self.padre,
            text="Datos generales del negocio",
            font=("Arial", 11),
            bg="#f3f4f6",
            fg="#6b7280"
        )

        subtitulo.pack(
            anchor="w",
            padx=30
        )

        # ==========================================
        # CONTENEDOR
        # ==========================================

        contenedor = tk.Frame(
            self.padre,
            bg="white",
            relief="solid",
            borderwidth=1
        )

        contenedor.pack(
            fill="x",
            padx=30,
            pady=25
        )

        # ==========================================
        # TÍTULO
        # ==========================================

        tk.Label(
            contenedor,
            text="Información de la empresa",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#111827"
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 5)
        )

        tk.Label(
            contenedor,
            text=(
                "Estos datos podrán utilizarse posteriormente "
                "en las facturas y documentos."
            ),
            font=("Arial", 10),
            bg="white",
            fg="#6b7280"
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 20)
        )

        # ==========================================
        # FORMULARIO
        # ==========================================

        formulario = tk.Frame(
            contenedor,
            bg="white"
        )

        formulario.pack(
            fill="x",
            padx=25,
            pady=(0, 20)
        )

        self.entradas = {}

        campos = [
            ("Nombre de la empresa", "nombre_empresa"),
            ("RNC", "rnc"),
            ("Teléfono", "telefono"),
            ("Email", "email"),
            ("Dirección", "direccion")
        ]

        for texto, clave in campos:

            tk.Label(
                formulario,
                text=texto,
                font=("Arial", 10),
                bg="white"
            ).pack(
                anchor="w",
                pady=(8, 3)
            )

            entrada = tk.Entry(
                formulario,
                font=("Arial", 10)
            )

            entrada.pack(
                fill="x",
                ipady=6
            )

            self.entradas[clave] = entrada

        # ==========================================
        # BOTÓN
        # ==========================================

        boton_guardar = tk.Button(
            contenedor,
            text="Guardar configuración",
            command=self.guardar,
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=9
        )

        boton_guardar.pack(
            anchor="e",
            padx=25,
            pady=(0, 25)
        )

    # ==========================================
    # CARGAR CONFIGURACIÓN
    # ==========================================

    def cargar_configuracion(self):

        configuracion = obtener_configuracion()

        if not configuracion:

            return

        self.entradas["nombre_empresa"].insert(
            0,
            configuracion[1] or ""
        )

        self.entradas["rnc"].insert(
            0,
            configuracion[2] or ""
        )

        self.entradas["telefono"].insert(
            0,
            configuracion[3] or ""
        )

        self.entradas["email"].insert(
            0,
            configuracion[4] or ""
        )

        self.entradas["direccion"].insert(
            0,
            configuracion[5] or ""
        )

    # ==========================================
    # GUARDAR
    # ==========================================

    def guardar(self):

        nombre_empresa = (
            self.entradas["nombre_empresa"]
            .get()
            .strip()
        )

        rnc = (
            self.entradas["rnc"]
            .get()
            .strip()
        )

        telefono = (
            self.entradas["telefono"]
            .get()
            .strip()
        )

        email = (
            self.entradas["email"]
            .get()
            .strip()
        )

        direccion = (
            self.entradas["direccion"]
            .get()
            .strip()
        )

        if not nombre_empresa:

            messagebox.showwarning(
                "Campo requerido",
                "Debe introducir el nombre de la empresa."
            )

            return

        try:

            guardar_configuracion(
                nombre_empresa,
                rnc,
                telefono,
                email,
                direccion
            )

            messagebox.showinfo(
                "Configuración guardada",
                "Los datos de la empresa fueron guardados correctamente."
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"No se pudo guardar la configuración.\n\n{error}"
            )