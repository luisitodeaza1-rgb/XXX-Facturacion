import tkinter as tk
from tkinter import ttk, messagebox

from Services.Client_services import (
    obtener_clientes,
    crear_cliente,
    actualizar_cliente,
    eliminar_cliente,
    buscar_clientes
)

from Services.RNC_services import consultar_rnc


class Clientes:

    def __init__(self, padre):

        self.padre = padre

        self.crear_interfaz()
        self.cargar_clientes()

    # ==========================================
    # INTERFAZ PRINCIPAL
    # ==========================================

    def crear_interfaz(self):

        titulo = tk.Label(
            self.padre,
            text="Clientes",
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
            text="Gestión de clientes",
            font=("Arial", 11),
            bg="#f3f4f6",
            fg="#6b7280"
        )

        subtitulo.pack(
            anchor="w",
            padx=30
        )

        # ==========================================
        # BARRA DE HERRAMIENTAS
        # ==========================================

        herramientas = tk.Frame(
            self.padre,
            bg="#f3f4f6"
        )

        herramientas.pack(
            fill="x",
            padx=30,
            pady=20
        )

        boton_nuevo = tk.Button(
            herramientas,
            text="+ Nuevo cliente",
            command=self.nuevo_cliente,
            font=("Arial", 10, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2"
        )

        boton_nuevo.pack(side="left")

        self.busqueda = tk.Entry(
            herramientas,
            width=35,
            font=("Arial", 10)
        )

        self.busqueda.pack(
            side="right",
            ipady=6
        )

        self.busqueda.insert(
            0,
            "Buscar cliente..."
        )

        self.busqueda.bind(
            "<FocusIn>",
            self.limpiar_placeholder
        )

        self.busqueda.bind(
            "<KeyRelease>",
            self.buscar
        )

        # ==========================================
        # TABLA
        # ==========================================

        contenedor_tabla = tk.Frame(
            self.padre,
            bg="#f3f4f6"
        )

        contenedor_tabla.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 20)
        )

        columnas = (
            "id",
            "nombre",
            "rnc",
            "telefono",
            "email",
            "direccion"
        )

        self.tabla = ttk.Treeview(
            contenedor_tabla,
            columns=columnas,
            show="headings"
        )

        self.tabla.heading(
            "id",
            text="ID"
        )

        self.tabla.heading(
            "nombre",
            text="Nombre"
        )

        self.tabla.heading(
            "rnc",
            text="RNC"
        )

        self.tabla.heading(
            "telefono",
            text="Teléfono"
        )

        self.tabla.heading(
            "email",
            text="Email"
        )

        self.tabla.heading(
            "direccion",
            text="Dirección"
        )

        self.tabla.column(
            "id",
            width=50,
            anchor="center"
        )

        self.tabla.column(
            "nombre",
            width=180
        )

        self.tabla.column(
            "rnc",
            width=120
        )

        self.tabla.column(
            "telefono",
            width=120
        )

        self.tabla.column(
            "email",
            width=180
        )

        self.tabla.column(
            "direccion",
            width=220
        )

        scrollbar = ttk.Scrollbar(
            contenedor_tabla,
            orient="vertical",
            command=self.tabla.yview
        )

        self.tabla.configure(
            yscrollcommand=scrollbar.set
        )

        self.tabla.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # ==========================================
        # BOTONES
        # ==========================================

        botones = tk.Frame(
            self.padre,
            bg="#f3f4f6"
        )

        botones.pack(
            fill="x",
            padx=30,
            pady=(0, 20)
        )

        boton_editar = tk.Button(
            botones,
            text="Editar",
            command=self.editar_cliente,
            width=12,
            cursor="hand2"
        )

        boton_editar.pack(
            side="left",
            padx=(0, 10)
        )

        boton_eliminar = tk.Button(
            botones,
            text="Eliminar",
            command=self.eliminar_cliente,
            width=12,
            cursor="hand2"
        )

        boton_eliminar.pack(
            side="left"
        )

        self.tabla.bind(
            "<Double-1>",
            lambda evento: self.editar_cliente()
        )

    # ==========================================
    # CARGAR CLIENTES
    # ==========================================

    def cargar_clientes(self):

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        clientes = obtener_clientes()

        for cliente in clientes:

            self.tabla.insert(
                "",
                "end",
                values=cliente
            )

    # ==========================================
    # BÚSQUEDA
    # ==========================================

    def limpiar_placeholder(self, evento):

        if self.busqueda.get() == "Buscar cliente...":

            self.busqueda.delete(
                0,
                tk.END
            )

    def buscar(self, evento=None):

        texto = self.busqueda.get().strip()

        if texto == "" or texto == "Buscar cliente...":

            self.cargar_clientes()

            return

        clientes = buscar_clientes(texto)

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        for cliente in clientes:

            self.tabla.insert(
                "",
                "end",
                values=cliente
            )

    # ==========================================
    # NUEVO CLIENTE
    # ==========================================

    def nuevo_cliente(self):

        self.abrir_formulario()

    # ==========================================
    # EDITAR CLIENTE
    # ==========================================

    def editar_cliente(self):

        seleccion = self.tabla.selection()

        if not seleccion:

            messagebox.showwarning(
                "Seleccionar cliente",
                "Seleccione un cliente para editar."
            )

            return

        datos = self.tabla.item(
            seleccion[0],
            "values"
        )

        self.abrir_formulario(datos)

    # ==========================================
    # FORMULARIO
    # ==========================================

    def abrir_formulario(self, cliente=None):

        ventana = tk.Toplevel(self.padre)

        ventana.title(
            "Editar cliente"
            if cliente
            else "Nuevo cliente"
        )

        ventana.geometry("500x650")

        ventana.resizable(
            False,
            False
        )

        ventana.transient(
            self.padre
        )

        ventana.grab_set()

        # ==========================================
        # TÍTULO
        # ==========================================

        tk.Label(
            ventana,
            text=(
                "Editar cliente"
                if cliente
                else "Nuevo cliente"
            ),
            font=("Arial", 20, "bold")
        ).pack(
            pady=20
        )

        formulario = tk.Frame(
            ventana
        )

        formulario.pack(
            padx=30,
            fill="x"
        )

        entradas = {}

        # ==========================================
        # NOMBRE
        # ==========================================

        tk.Label(
            formulario,
            text="Nombre *",
            font=("Arial", 10)
        ).pack(
            anchor="w",
            pady=(8, 3)
        )

        entradas["nombre"] = tk.Entry(
            formulario,
            font=("Arial", 10)
        )

        entradas["nombre"].pack(
            fill="x",
            ipady=5
        )

        # ==========================================
        # RNC
        # ==========================================

        tk.Label(
            formulario,
            text="RNC",
            font=("Arial", 10)
        ).pack(
            anchor="w",
            pady=(8, 3)
        )

        fila_rnc = tk.Frame(
            formulario
        )

        fila_rnc.pack(
            fill="x"
        )

        entradas["rnc"] = tk.Entry(
            fila_rnc,
            font=("Arial", 10)
        )

        entradas["rnc"].pack(
            side="left",
            fill="x",
            expand=True,
            ipady=5
        )

        # ==========================================
        # TELÉFONO
        # ==========================================

        tk.Label(
            formulario,
            text="Teléfono",
            font=("Arial", 10)
        ).pack(
            anchor="w",
            pady=(8, 3)
        )

        entradas["telefono"] = tk.Entry(
            formulario,
            font=("Arial", 10)
        )

        entradas["telefono"].pack(
            fill="x",
            ipady=5
        )

        # ==========================================
        # EMAIL
        # ==========================================

        tk.Label(
            formulario,
            text="Email",
            font=("Arial", 10)
        ).pack(
            anchor="w",
            pady=(8, 3)
        )

        entradas["email"] = tk.Entry(
            formulario,
            font=("Arial", 10)
        )

        entradas["email"].pack(
            fill="x",
            ipady=5
        )

        # ==========================================
        # DIRECCIÓN
        # ==========================================

        tk.Label(
            formulario,
            text="Dirección",
            font=("Arial", 10)
        ).pack(
            anchor="w",
            pady=(8, 3)
        )

        entradas["direccion"] = tk.Entry(
            formulario,
            font=("Arial", 10)
        )

        entradas["direccion"].pack(
            fill="x",
            ipady=5
        )

        # ==========================================
        # INFORMACIÓN DGAPI
        # ==========================================

        informacion_dgapi = tk.LabelFrame(
            formulario,
            text="Información DGAPI",
            font=("Arial", 9, "bold"),
            padx=10,
            pady=5
        )

        informacion_dgapi.pack(
            fill="x",
            pady=(15, 5)
        )

        etiquetas_dgapi = {}

        campos_dgapi = [
            ("Nombre comercial", "nombre_comercial"),
            ("Actividad económica", "actividad_economica"),
            ("Fecha de inicio", "fecha_inicio"),
            ("Estado", "estado"),
            ("Régimen de pago", "regimen")
        ]

        for texto, clave in campos_dgapi:

            fila = tk.Frame(
                informacion_dgapi
            )

            fila.pack(
                fill="x",
                pady=2
            )

            tk.Label(
                fila,
                text=f"{texto}:",
                width=22,
                anchor="w",
                font=("Arial", 9)
            ).pack(
                side="left"
            )

            etiqueta = tk.Label(
                fila,
                text="",
                anchor="w",
                font=("Arial", 9)
            )

            etiqueta.pack(
                side="left",
                fill="x",
                expand=True
            )

            etiquetas_dgapi[clave] = etiqueta

        # ==========================================
        # CONSULTAR DGAPI
        # ==========================================

        def consultar_dgapi():

            rnc = entradas["rnc"].get().strip()

            if not rnc:

                messagebox.showwarning(
                    "RNC requerido",
                    "Introduzca un RNC para realizar la consulta.",
                    parent=ventana
                )

                return

            try:

                boton_dgapi.config(
                    state="disabled",
                    text="Consultando..."
                )

                ventana.update_idletasks()

                datos = consultar_rnc(rnc)

                if datos is None:

                    messagebox.showinfo(
                        "RNC no encontrado",
                        f"No se encontró información para el RNC {rnc}.",
                        parent=ventana
                    )

                    return

                # ======================================
                # RNC NORMALIZADO
                # ======================================

                entradas["rnc"].delete(
                    0,
                    tk.END
                )

                entradas["rnc"].insert(
                    0,
                    datos.get("rnc", rnc)
                )

                # ======================================
                # NOMBRE
                # ======================================

                nombre = datos.get(
                    "nombre_empresa",
                    ""
                )

                if nombre:

                    entradas["nombre"].delete(
                        0,
                        tk.END
                    )

                    entradas["nombre"].insert(
                        0,
                        nombre
                    )

                # ======================================
                # INFORMACIÓN ADICIONAL
                # ======================================

                for clave, etiqueta in etiquetas_dgapi.items():

                    valor = datos.get(
                        clave,
                        ""
                    )

                    etiqueta.config(
                        text=valor or "No disponible"
                    )

                messagebox.showinfo(
                    "Consulta completada",
                    "La información del RNC fue obtenida correctamente desde DGAPI.",
                    parent=ventana
                )

            except ValueError as error:

                messagebox.showwarning(
                    "RNC inválido",
                    str(error),
                    parent=ventana
                )

            except RuntimeError as error:

                messagebox.showerror(
                    "Error de DGAPI",
                    str(error),
                    parent=ventana
                )

            except Exception as error:

                messagebox.showerror(
                    "Error",
                    f"Ocurrió un error durante la consulta.\n\n{error}",
                    parent=ventana
                )

            finally:

                boton_dgapi.config(
                    state="normal",
                    text="Consultar DGAPI"
                )

        boton_dgapi = tk.Button(
            fila_rnc,
            text="Consultar DGAPI",
            command=consultar_dgapi,
            bg="#111827",
            fg="white",
            activebackground="#374151",
            activeforeground="white",
            relief="flat",
            cursor="hand2"
        )

        boton_dgapi.pack(
            side="left",
            padx=(8, 0),
            ipady=4
        )

        # ==========================================
        # CARGAR DATOS SI ES EDICIÓN
        # ==========================================

        if cliente:

            entradas["nombre"].insert(
                0,
                cliente[1]
            )

            entradas["rnc"].insert(
                0,
                cliente[2] or ""
            )

            entradas["telefono"].insert(
                0,
                cliente[3] or ""
            )

            entradas["email"].insert(
                0,
                cliente[4] or ""
            )

            entradas["direccion"].insert(
                0,
                cliente[5] or ""
            )

        # ==========================================
        # GUARDAR
        # ==========================================

        def guardar():

            nombre = entradas["nombre"].get().strip()
            rnc = entradas["rnc"].get().strip()
            telefono = entradas["telefono"].get().strip()
            email = entradas["email"].get().strip()
            direccion = entradas["direccion"].get().strip()

            if not nombre:

                messagebox.showwarning(
                    "Campo requerido",
                    "El nombre del cliente es obligatorio.",
                    parent=ventana
                )

                return

            try:

                if cliente:

                    actualizar_cliente(
                        cliente[0],
                        nombre,
                        rnc,
                        telefono,
                        email,
                        direccion
                    )

                    mensaje = "Cliente actualizado correctamente."

                else:

                    crear_cliente(
                        nombre,
                        rnc,
                        telefono,
                        email,
                        direccion
                    )

                    mensaje = "Cliente creado correctamente."

                messagebox.showinfo(
                    "Operación completada",
                    mensaje,
                    parent=ventana
                )

                ventana.destroy()

                self.cargar_clientes()

            except Exception as error:

                messagebox.showerror(
                    "Error",
                    f"No se pudo guardar el cliente.\n\n{error}",
                    parent=ventana
                )

        # ==========================================
        # BOTÓN GUARDAR
        # ==========================================

        boton_guardar = tk.Button(
            ventana,
            text="Guardar",
            command=guardar,
            width=18,
            bg="#2563eb",
            fg="white",
            relief="flat",
            cursor="hand2"
        )

        boton_guardar.pack(
            pady=20,
            ipady=5
        )

    # ==========================================
    # ELIMINAR CLIENTE
    # ==========================================

    def eliminar_cliente(self):

        seleccion = self.tabla.selection()

        if not seleccion:

            messagebox.showwarning(
                "Seleccionar cliente",
                "Seleccione un cliente para eliminar."
            )

            return

        datos = self.tabla.item(
            seleccion[0],
            "values"
        )

        cliente_id = datos[0]
        nombre = datos[1]

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Está seguro de eliminar al cliente:\n\n{nombre}?"
        )

        if not confirmar:
            return

        try:

            eliminar_cliente(cliente_id)

            self.cargar_clientes()

            messagebox.showinfo(
                "Cliente eliminado",
                "El cliente fue eliminado correctamente."
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"No se pudo eliminar el cliente.\n\n{error}"
            )