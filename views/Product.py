import tkinter as tk
from tkinter import ttk, messagebox

from Services.Product_services import (
    obtener_productos,
    crear_producto,
    actualizar_producto,
    eliminar_producto,
    buscar_productos
)


class Productos:

    def __init__(self, padre):

        self.padre = padre

        self.crear_interfaz()
        self.cargar_productos()

    # ==========================================
    # INTERFAZ
    # ==========================================

    def crear_interfaz(self):

        titulo = tk.Label(
            self.padre,
            text="Productos",
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
            text="Gestión de productos e inventario",
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
            text="+ Nuevo producto",
            command=self.nuevo_producto,
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

        # ==========================================
        # BUSCADOR
        # ==========================================

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
            "Buscar producto..."
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
            "codigo",
            "nombre",
            "precio",
            "stock"
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
            "codigo",
            text="Código"
        )

        self.tabla.heading(
            "nombre",
            text="Producto"
        )

        self.tabla.heading(
            "precio",
            text="Precio"
        )

        self.tabla.heading(
            "stock",
            text="Stock"
        )

        # ==========================================
        # COLUMNAS
        # ==========================================

        self.tabla.column(
            "id",
            width=50,
            anchor="center"
        )

        self.tabla.column(
            "codigo",
            width=120
        )

        self.tabla.column(
            "nombre",
            width=250
        )

        self.tabla.column(
            "precio",
            width=120,
            anchor="e"
        )

        self.tabla.column(
            "stock",
            width=100,
            anchor="center"
        )

        # ==========================================
        # SCROLLBAR
        # ==========================================

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
        # BOTONES INFERIORES
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
            command=self.editar_producto,
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
            command=self.eliminar_producto,
            width=12,
            cursor="hand2"
        )

        boton_eliminar.pack(
            side="left"
        )

        self.tabla.bind(
            "<Double-1>",
            lambda evento: self.editar_producto()
        )

    # ==========================================
    # CARGAR PRODUCTOS
    # ==========================================

    def cargar_productos(self):

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        productos = obtener_productos()

        for producto in productos:

            valores = (
                producto[0],
                producto[1] or "",
                producto[2],
                f"RD$ {producto[3]:,.2f}",
                producto[4]
            )

            self.tabla.insert(
                "",
                "end",
                values=valores
            )

    # ==========================================
    # BÚSQUEDA
    # ==========================================

    def limpiar_placeholder(self, evento):

        if self.busqueda.get() == "Buscar producto...":

            self.busqueda.delete(
                0,
                tk.END
            )

    def buscar(self, evento=None):

        texto = self.busqueda.get().strip()

        if texto == "" or texto == "Buscar producto...":

            self.cargar_productos()

            return

        productos = buscar_productos(texto)

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        for producto in productos:

            valores = (
                producto[0],
                producto[1] or "",
                producto[2],
                f"RD$ {producto[3]:,.2f}",
                producto[4]
            )

            self.tabla.insert(
                "",
                "end",
                values=valores
            )

    # ==========================================
    # NUEVO PRODUCTO
    # ==========================================

    def nuevo_producto(self):

        self.abrir_formulario()

    # ==========================================
    # EDITAR PRODUCTO
    # ==========================================

    def editar_producto(self):

        seleccion = self.tabla.selection()

        if not seleccion:

            messagebox.showwarning(
                "Seleccionar producto",
                "Seleccione un producto para editar."
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

    def abrir_formulario(self, producto=None):

        ventana = tk.Toplevel(
            self.padre
        )

        ventana.title(
            "Editar producto"
            if producto
            else "Nuevo producto"
        )

        ventana.geometry(
            "450x450"
        )

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
                "Editar producto"
                if producto
                else "Nuevo producto"
            ),
            font=("Arial", 20, "bold")
        ).pack(
            pady=20
        )

        # ==========================================
        # FORMULARIO
        # ==========================================

        formulario = tk.Frame(
            ventana
        )

        formulario.pack(
            padx=30,
            fill="x"
        )

        campos = [
            ("Código", "codigo"),
            ("Nombre *", "nombre"),
            ("Precio *", "precio"),
            ("Stock", "stock")
        ]

        entradas = {}

        for texto, clave in campos:

            tk.Label(
                formulario,
                text=texto,
                font=("Arial", 10)
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
                ipady=5
            )

            entradas[clave] = entrada

        # ==========================================
        # CARGAR DATOS
        # ==========================================

        if producto:

            entradas["codigo"].insert(
                0,
                producto[1]
            )

            entradas["nombre"].insert(
                0,
                producto[2]
            )

            precio = producto[3].replace(
                "RD$ ",
                ""
            ).replace(
                ",",
                ""
            )

            entradas["precio"].insert(
                0,
                precio
            )

            entradas["stock"].insert(
                0,
                producto[4]
            )

        else:

            entradas["stock"].insert(
                0,
                "0"
            )

        # ==========================================
        # GUARDAR
        # ==========================================

        def guardar():

            codigo = entradas["codigo"].get().strip()
            nombre = entradas["nombre"].get().strip()
            precio = entradas["precio"].get().strip()
            stock = entradas["stock"].get().strip()

            # ------------------------------
            # VALIDAR NOMBRE
            # ------------------------------

            if not nombre:

                messagebox.showwarning(
                    "Campo requerido",
                    "El nombre del producto es obligatorio.",
                    parent=ventana
                )

                return

            # ------------------------------
            # VALIDAR PRECIO
            # ------------------------------

            try:

                precio = float(precio)

                if precio < 0:

                    raise ValueError

            except ValueError:

                messagebox.showwarning(
                    "Precio inválido",
                    "Introduzca un precio válido.",
                    parent=ventana
                )

                return

            # ------------------------------
            # VALIDAR STOCK
            # ------------------------------

            try:

                stock = int(stock)

                if stock < 0:

                    raise ValueError

            except ValueError:

                messagebox.showwarning(
                    "Stock inválido",
                    "El stock debe ser un número entero igual o mayor que 0.",
                    parent=ventana
                )

                return

            # ------------------------------
            # GUARDAR
            # ------------------------------

            try:

                if producto:

                    actualizar_producto(
                        producto[0],
                        codigo,
                        nombre,
                        precio,
                        stock
                    )

                    mensaje = (
                        "Producto actualizado correctamente."
                    )

                else:

                    crear_producto(
                        codigo,
                        nombre,
                        precio,
                        stock
                    )

                    mensaje = (
                        "Producto creado correctamente."
                    )

                messagebox.showinfo(
                    "Operación completada",
                    mensaje,
                    parent=ventana
                )

                ventana.destroy()

                self.cargar_productos()

            except Exception as error:

                messagebox.showerror(
                    "Error",
                    f"No se pudo guardar el producto.\n\n{error}",
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
            pady=25,
            ipady=5
        )

    # ==========================================
    # ELIMINAR PRODUCTO
    # ==========================================

    def eliminar_producto(self):

        seleccion = self.tabla.selection()

        if not seleccion:

            messagebox.showwarning(
                "Seleccionar producto",
                "Seleccione un producto para eliminar."
            )

            return

        datos = self.tabla.item(
            seleccion[0],
            "values"
        )

        producto_id = datos[0]
        nombre = datos[2]

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Está seguro de eliminar el producto:\n\n{nombre}?"
        )

        if not confirmar:

            return

        try:

            eliminar_producto(
                producto_id
            )

            self.cargar_productos()

            messagebox.showinfo(
                "Producto eliminado",
                "El producto fue eliminado correctamente."
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"No se pudo eliminar el producto.\n\n{error}"
            )