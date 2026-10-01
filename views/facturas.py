import tkinter as tk
from tkinter import ttk, messagebox

from Services.Facturas_services import (
    obtener_clientes_para_factura,
    obtener_productos_para_factura,
    obtener_producto_por_id,
    crear_factura
)


class Facturacion:

    def __init__(self, padre):

        self.padre = padre

        self.productos = []
        self.items = []

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
            text="Cliente",
            font=("Arial", 11, "bold"),
            bg="white"
        ).pack(
            side="left",
            padx=(15, 10),
            pady=15
        )

        self.cliente_var = tk.StringVar()

        self.cliente_combo = ttk.Combobox(
            cliente_frame,
            textvariable=self.cliente_var,
            state="readonly",
            width=45
        )

        self.cliente_combo.pack(
            side="left",
            padx=10,
            pady=15
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
    # CLIENTES
    # ==========================================

    def cargar_clientes(self):

        clientes = obtener_clientes_para_factura()

        self.clientes = clientes

        opciones = []

        for cliente in clientes:

            rnc = cliente[2] or "Sin RNC"

            opciones.append(
                f"{cliente[0]} - {cliente[1]} - {rnc}"
            )

        self.cliente_combo["values"] = opciones

        if opciones:

            self.cliente_combo.current(0)

    # ==========================================
    # PRODUCTOS
    # ==========================================

    def cargar_productos(self):

        self.productos = obtener_productos_para_factura()

        opciones = []

        for producto in self.productos:

            codigo = producto[1] or "Sin código"

            opciones.append(
                f"{producto[0]} - {codigo} - {producto[2]} - "
                f"RD$ {producto[3]:,.2f} - Stock: {producto[4]}"
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
                "La cantidad debe ser un número entero mayor que 0."
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

        # ==========================================
        # VERIFICAR SI YA ESTÁ EN LA FACTURA
        # ==========================================

        for item in self.items:

            if item["producto_id"] == producto_id:

                nueva_cantidad = (
                    item["cantidad"] + cantidad
                )

                if nueva_cantidad > stock:

                    messagebox.showwarning(
                        "Stock insuficiente",
                        f"No puede agregar más de {stock} unidades."
                    )

                    return

                item["cantidad"] = nueva_cantidad

                item["subtotal"] = (
                    precio * nueva_cantidad
                )

                self.actualizar_tabla()

                return

        # ==========================================
        # NUEVO ITEM
        # ==========================================

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

        cliente_index = self.cliente_combo.current()

        if cliente_index == -1:

            messagebox.showwarning(
                "Cliente",
                "Seleccione un cliente."
            )

            return

        if not self.items:

            messagebox.showwarning(
                "Factura vacía",
                "Agregue al menos un producto."
            )

            return

        cliente = self.clientes[
            cliente_index
        ]

        cliente_id = cliente[0]

        try:

            resultado = crear_factura(
                cliente_id,
                self.items
            )

            messagebox.showinfo(
                "Factura creada",
                (
                    f"Factura {resultado['numero']} creada correctamente.\n\n"
                    f"Subtotal: RD$ {resultado['subtotal']:,.2f}\n"
                    f"ITBIS: RD$ {resultado['itbis']:,.2f}\n"
                    f"Total: RD$ {resultado['total']:,.2f}"
                )
            )

            self.items = []

            self.actualizar_tabla()

            self.cargar_productos()

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"No se pudo crear la factura.\n\n{error}"
            )