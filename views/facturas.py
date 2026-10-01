import tkinter as tk
from tkinter import ttk, messagebox

from Services.Facturas_services import (
    obtener_clientes_para_factura,
    obtener_productos_para_factura,
    obtener_producto_por_id,
    crear_factura
)

from Services.Client_services import (
    obtener_cliente_por_rnc
)

from Services.RNC_services import consultar_rnc


class Facturacion:

    def __init__(self, padre):

        self.padre = padre

        self.productos = []
        self.items = []
        self.clientes = []

        # Cliente actualmente seleccionado.
        #
        # Ejemplo cliente registrado:
        # {
        #     "tipo": "registrado",
        #     "id": 1,
        #     "nombre": "...",
        #     "rnc": "..."
        # }
        #
        # Ejemplo particular:
        # {
        #     "tipo": "particular",
        #     "id": None,
        #     "nombre": "...",
        #     "rnc": "..."
        # }

        self.cliente_actual = None

        self.crear_interfaz()
        self.cargar_clientes()
        self.cargar_productos()

    # ==========================================
    # INTERFAZ PRINCIPAL
    # ==========================================

    def crear_interfaz(self):

        titulo = tk.Label(
            self.padre,
            text="Nueva factura",
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
            text="Crear factura y gestionar los productos vendidos",
            font=("Arial", 11),
            bg="#f3f4f6",
            fg="#6b7280"
        )

        subtitulo.pack(
            anchor="w",
            padx=30
        )

        # ==========================================
        # INFORMACIÓN DEL CLIENTE
        # ==========================================

        cliente_frame = tk.Frame(
            self.padre,
            bg="white",
            relief="solid",
            borderwidth=1
        )

        cliente_frame.pack(
            fill="x",
            padx=30,
            pady=20
        )

        tk.Label(
            cliente_frame,
            text="RNC del cliente",
            font=("Arial", 10, "bold"),
            bg="white"
        ).grid(
            row=0,
            column=0,
            padx=(15, 5),
            pady=(15, 5),
            sticky="w"
        )

        self.rnc_var = tk.StringVar()

        self.rnc_entry = tk.Entry(
            cliente_frame,
            textvariable=self.rnc_var,
            font=("Arial", 10),
            width=25
        )

        self.rnc_entry.grid(
            row=1,
            column=0,
            padx=(15, 5),
            pady=(0, 15),
            ipady=6
        )

        boton_consultar = tk.Button(
            cliente_frame,
            text="CONSULTAR DGAPI",
            command=self.consultar_dgapi,
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8
        )

        boton_consultar.grid(
            row=1,
            column=1,
            padx=5,
            pady=(0, 15)
        )

        tk.Label(
            cliente_frame,
            text="Cliente registrado",
            font=("Arial", 10, "bold"),
            bg="white"
        ).grid(
            row=0,
            column=2,
            padx=(20, 5),
            pady=(15, 5),
            sticky="w"
        )

        self.cliente_var = tk.StringVar()

        self.cliente_combo = ttk.Combobox(
            cliente_frame,
            textvariable=self.cliente_var,
            state="readonly",
            width=45
        )

        self.cliente_combo.grid(
            row=1,
            column=2,
            padx=(20, 15),
            pady=(0, 15)
        )

        # ==========================================
        # DATOS DEL CLIENTE
        # ==========================================

        self.cliente_info = tk.Label(
            cliente_frame,
            text="Cliente: Ninguno seleccionado",
            font=("Arial", 10),
            bg="white",
            fg="#374151"
        )

        self.cliente_info.grid(
            row=2,
            column=0,
            columnspan=3,
            padx=15,
            pady=(0, 15),
            sticky="w"
        )

        self.cliente_combo.bind(
            "<<ComboboxSelected>>",
            self.cliente_seleccionado
        )

        # ==========================================
        # AGREGAR PRODUCTO
        # ==========================================

        producto_frame = tk.Frame(
            self.padre,
            bg="white",
            relief="solid",
            borderwidth=1
        )

        producto_frame.pack(
            fill="x",
            padx=30,
            pady=(0, 20)
        )

        tk.Label(
            producto_frame,
            text="Producto",
            font=("Arial", 10, "bold"),
            bg="white"
        ).grid(
            row=0,
            column=0,
            padx=(15, 5),
            pady=15
        )

        self.producto_var = tk.StringVar()

        self.producto_combo = ttk.Combobox(
            producto_frame,
            textvariable=self.producto_var,
            state="readonly",
            width=40
        )

        self.producto_combo.grid(
            row=0,
            column=1,
            padx=5,
            pady=15
        )

        tk.Label(
            producto_frame,
            text="Cantidad",
            font=("Arial", 10, "bold"),
            bg="white"
        ).grid(
            row=0,
            column=2,
            padx=(20, 5)
        )

        self.cantidad = tk.Entry(
            producto_frame,
            width=8
        )

        self.cantidad.insert(
            0,
            "1"
        )

        self.cantidad.grid(
            row=0,
            column=3,
            padx=5
        )

        boton_agregar = tk.Button(
            producto_frame,
            text="+ Agregar",
            command=self.agregar_producto,
            bg="#2563eb",
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=6
        )

        boton_agregar.grid(
            row=0,
            column=4,
            padx=15
        )

        # ==========================================
        # TABLA DE PRODUCTOS
        # ==========================================

        tabla_frame = tk.Frame(
            self.padre,
            bg="#f3f4f6"
        )

        tabla_frame.pack(
            fill="both",
            expand=True,
            padx=30
        )

        columnas = (
            "producto",
            "cantidad",
            "precio",
            "subtotal"
        )

        self.tabla = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings"
        )

        self.tabla.heading(
            "producto",
            text="Producto"
        )

        self.tabla.heading(
            "cantidad",
            text="Cantidad"
        )

        self.tabla.heading(
            "precio",
            text="Precio"
        )

        self.tabla.heading(
            "subtotal",
            text="Subtotal"
        )

        self.tabla.column(
            "producto",
            width=300
        )

        self.tabla.column(
            "cantidad",
            width=100,
            anchor="center"
        )

        self.tabla.column(
            "precio",
            width=130,
            anchor="e"
        )

        self.tabla.column(
            "subtotal",
            width=150,
            anchor="e"
        )

        scrollbar = ttk.Scrollbar(
            tabla_frame,
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
        # PARTE INFERIOR
        # ==========================================

        inferior = tk.Frame(
            self.padre,
            bg="#f3f4f6"
        )

        inferior.pack(
            fill="x",
            padx=30,
            pady=20
        )

        boton_eliminar = tk.Button(
            inferior,
            text="Eliminar producto",
            command=self.eliminar_producto,
            width=18,
            cursor="hand2"
        )

        boton_eliminar.pack(
            side="left"
        )

        totales = tk.Frame(
            inferior,
            bg="#f3f4f6"
        )

        totales.pack(
            side="right"
        )

        self.label_subtotal = tk.Label(
            totales,
            text="Subtotal: RD$ 0.00",
            font=("Arial", 11),
            bg="#f3f4f6"
        )

        self.label_subtotal.pack(
            anchor="e"
        )

        self.label_itbis = tk.Label(
            totales,
            text="ITBIS: RD$ 0.00",
            font=("Arial", 11),
            bg="#f3f4f6"
        )

        self.label_itbis.pack(
            anchor="e"
        )

        self.label_total = tk.Label(
            totales,
            text="Total: RD$ 0.00",
            font=("Arial", 16, "bold"),
            bg="#f3f4f6",
            fg="#111827"
        )

        self.label_total.pack(
            anchor="e",
            pady=(5, 0)
        )

        boton_facturar = tk.Button(
            inferior,
            text="CREAR FACTURA",
            command=self.guardar_factura,
            bg="#16a34a",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10
        )

        boton_facturar.pack(
            side="right",
            padx=(20, 30)
        )

    # ==========================================
    # CONSULTAR DGAPI
    # ==========================================

    def consultar_dgapi(self):

        rnc = (
            self.rnc_var
            .get()
            .replace("-", "")
            .replace(" ", "")
            .strip()
        )

        if not rnc:

            messagebox.showwarning(
                "RNC requerido",
                "Introduzca el RNC del cliente."
            )

            return

        try:

            self.padre.config(
                cursor="watch"
            )

            self.padre.update()

            # ==========================================
            # PRIMERO BUSCAMOS EN CLIENTES REGISTRADOS
            # ==========================================

            cliente = obtener_cliente_por_rnc(rnc)

            if cliente:

                self.seleccionar_cliente(
                    cliente
                )

                messagebox.showinfo(
                    "Cliente registrado",
                    (
                        f"El cliente '{cliente[1]}' "
                        "ya está registrado en el sistema."
                    )
                )

                return

            # ==========================================
            # SI NO EXISTE, CONSULTAMOS DGAPI
            # ==========================================

            resultado = consultar_rnc(rnc)

            if not resultado:

                self.cliente_actual = None

                self.cliente_combo.set("")

                self.cliente_info.config(
                    text="Cliente: RNC no encontrado"
                )

                messagebox.showwarning(
                    "RNC no encontrado",
                    (
                        "DGAPI no encontró información "
                        "para el RNC indicado."
                    )
                )

                return

            # ==========================================
            # OBTENER NOMBRE
            # ==========================================

            nombre = (
                resultado.get("nombre_empresa")
                or resultado.get("nombre_comercial")
            )

            if not nombre:

                self.cliente_actual = None

                messagebox.showwarning(
                    "Datos incompletos",
                    (
                        "DGAPI no devolvió el nombre "
                        "del contribuyente."
                    )
                )

                return

            # ==========================================
            # PARTICULAR
            #
            # NO SE CREA EN clientes
            # ==========================================

            self.cliente_actual = {
                "tipo": "particular",
                "id": None,
                "nombre": nombre,
                "rnc": rnc
            }

            # Quitamos cualquier selección anterior
            self.cliente_combo.set("")

            # ==========================================
            # MOSTRAR INFORMACIÓN
            # ==========================================

            actividad = resultado.get(
                "actividad_economica",
                ""
            )

            estado = resultado.get(
                "estado",
                ""
            )

            regimen = resultado.get(
                "regimen",
                ""
            )

            self.cliente_info.config(
                text=(
                    f"Particular: {nombre} | "
                    f"RNC: {rnc}"
                )
            )

            mensaje = (
                f"Nombre: {nombre}\n"
                f"RNC: {rnc}"
            )

            if actividad:

                mensaje += (
                    f"\nActividad económica: {actividad}"
                )

            if estado:

                mensaje += (
                    f"\nEstado: {estado}"
                )

            if regimen:

                mensaje += (
                    f"\nRégimen: {regimen}"
                )

            messagebox.showinfo(
                "Particular encontrado",
                (
                    "El contribuyente fue encontrado "
                    "mediante DGAPI.\n\n"
                    "No fue agregado a la tabla de clientes.\n\n"
                    + mensaje
                )
            )

        except ValueError as error:

            messagebox.showwarning(
                "RNC inválido",
                str(error)
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                (
                    "No fue posible consultar el RNC.\n\n"
                    f"{error}"
                )
            )

        finally:

            self.padre.config(
                cursor=""
            )

    # ==========================================
    # SELECCIONAR CLIENTE REGISTRADO
    # ==========================================

    def seleccionar_cliente(self, cliente):

        for indice, elemento in enumerate(
            self.clientes
        ):

            if elemento[0] == cliente[0]:

                self.cliente_combo.current(
                    indice
                )

                self.cliente_var.set(
                    f"{cliente[0]} - "
                    f"{cliente[1]} - "
                    f"{cliente[2] or 'Sin RNC'}"
                )

                self.cliente_actual = {
                    "tipo": "registrado",
                    "id": cliente[0],
                    "nombre": cliente[1],
                    "rnc": cliente[2] or ""
                }

                self.cliente_info.config(
                    text=(
                        f"Cliente seleccionado: "
                        f"{cliente[1]} | "
                        f"RNC: {cliente[2] or 'Sin RNC'}"
                    )
                )

                break

    def cliente_seleccionado(self, event=None):

        indice = self.cliente_combo.current()

        if indice == -1:

            return

        cliente = self.clientes[indice]

        self.cliente_actual = {
            "tipo": "registrado",
            "id": cliente[0],
            "nombre": cliente[1],
            "rnc": cliente[2] or ""
        }

        self.cliente_info.config(
            text=(
                f"Cliente seleccionado: "
                f"{cliente[1]} | "
                f"RNC: {cliente[2] or 'Sin RNC'}"
            )
        )

        if cliente[2]:

            self.rnc_var.set(
                cliente[2]
            )

    # ==========================================
    # ACTUALIZAR LISTA DE CLIENTES
    # ==========================================

    def actualizar_lista_clientes(self):

        opciones = []

        for cliente in self.clientes:

            rnc = cliente[2] or "Sin RNC"

            opciones.append(
                f"{cliente[0]} - "
                f"{cliente[1]} - "
                f"{rnc}"
            )

        self.cliente_combo["values"] = opciones

    # ==========================================
    # CLIENTES
    # ==========================================

    def cargar_clientes(self):

        clientes = obtener_clientes_para_factura()

        self.clientes = clientes

        self.actualizar_lista_clientes()

        if clientes:

            self.cliente_combo.current(0)

            self.cliente_seleccionado()

    # ==========================================
    # PRODUCTOS
    # ==========================================

    def cargar_productos(self):

        self.productos = obtener_productos_para_factura()

        opciones = []

        for producto in self.productos:

            codigo = producto[1] or "Sin código"

            opciones.append(
                f"{producto[0]} - "
                f"{codigo} - "
                f"{producto[2]} - "
                f"RD$ {producto[3]:,.2f} - "
                f"Stock: {producto[4]}"
            )

        self.producto_combo["values"] = opciones

        if opciones:

            self.producto_combo.current(0)

    # ==========================================
    # AGREGAR PRODUCTO
    # ==========================================

    def agregar_producto(self):

        seleccion = self.producto_combo.current()

        if seleccion == -1:

            messagebox.showwarning(
                "Producto",
                "Seleccione un producto."
            )

            return

        try:

            cantidad = int(
                self.cantidad.get()
            )

            if cantidad <= 0:

                raise ValueError

        except ValueError:

            messagebox.showwarning(
                "Cantidad",
                (
                    "La cantidad debe ser un número "
                    "entero mayor que 0."
                )
            )

            return

        producto = self.productos[seleccion]

        producto_id = producto[0]
        nombre = producto[2]
        precio = float(producto[3])
        stock = int(producto[4])

        if cantidad > stock:

            messagebox.showwarning(
                "Stock insuficiente",
                f"Stock disponible de '{nombre}': {stock}"
            )

            return

        for item in self.items:

            if item["producto_id"] == producto_id:

                nueva_cantidad = (
                    item["cantidad"] + cantidad
                )

                if nueva_cantidad > stock:

                    messagebox.showwarning(
                        "Stock insuficiente",
                        (
                            f"No puede agregar más "
                            f"de {stock} unidades."
                        )
                    )

                    return

                item["cantidad"] = nueva_cantidad

                item["subtotal"] = (
                    precio * nueva_cantidad
                )

                self.actualizar_tabla()

                return

        item = {
            "producto_id": producto_id,
            "nombre": nombre,
            "cantidad": cantidad,
            "precio": precio,
            "subtotal": precio * cantidad
        }

        self.items.append(
            item
        )

        self.actualizar_tabla()

    # ==========================================
    # ACTUALIZAR TABLA
    # ==========================================

    def actualizar_tabla(self):

        for fila in self.tabla.get_children():

            self.tabla.delete(fila)

        for item in self.items:

            self.tabla.insert(
                "",
                "end",
                values=(
                    item["nombre"],
                    item["cantidad"],
                    f"RD$ {item['precio']:,.2f}",
                    f"RD$ {item['subtotal']:,.2f}"
                )
            )

        self.calcular_totales()

    # ==========================================
    # CALCULAR TOTALES
    # ==========================================

    def calcular_totales(self):

        subtotal = sum(
            item["subtotal"]
            for item in self.items
        )

        itbis = subtotal * 0.18

        total = subtotal + itbis

        self.label_subtotal.config(
            text=f"Subtotal: RD$ {subtotal:,.2f}"
        )

        self.label_itbis.config(
            text=f"ITBIS: RD$ {itbis:,.2f}"
        )

        self.label_total.config(
            text=f"Total: RD$ {total:,.2f}"
        )

    # ==========================================
    # ELIMINAR PRODUCTO
    # ==========================================

    def eliminar_producto(self):

        seleccion = self.tabla.selection()

        if not seleccion:

            messagebox.showwarning(
                "Seleccionar producto",
                "Seleccione un producto de la factura."
            )

            return

        indice = self.tabla.index(
            seleccion[0]
        )

        del self.items[indice]

        self.actualizar_tabla()

    # ==========================================
    # GUARDAR FACTURA
    # ==========================================

    def guardar_factura(self):

        if self.cliente_actual is None:

            messagebox.showwarning(
                "Cliente",
                (
                    "Seleccione un cliente registrado "
                    "o consulte un RNC mediante DGAPI."
                )
            )

            return

        if not self.items:

            messagebox.showwarning(
                "Factura vacía",
                "Agregue al menos un producto."
            )

            return

        cliente_id = self.cliente_actual["id"]
        cliente_nombre = self.cliente_actual["nombre"]
        cliente_rnc = self.cliente_actual["rnc"]

        try:

            resultado = crear_factura(
                cliente_id,
                self.items,
                cliente_nombre,
                cliente_rnc
            )

            messagebox.showinfo(
                "Factura creada",
                (
                    f"Factura {resultado['numero']} "
                    "creada correctamente.\n\n"
                    f"Cliente: {cliente_nombre}\n"
                    f"RNC: {cliente_rnc or 'Sin RNC'}\n\n"
                    f"Subtotal: RD$ "
                    f"{resultado['subtotal']:,.2f}\n"
                    f"ITBIS: RD$ "
                    f"{resultado['itbis']:,.2f}\n"
                    f"Total: RD$ "
                    f"{resultado['total']:,.2f}"
                )
            )

            self.items = []

            self.actualizar_tabla()

            self.cargar_productos()

        except Exception as error:

            messagebox.showerror(
                "Error",
                (
                    "No se pudo crear la factura.\n\n"
                    f"{error}"
                )
            )