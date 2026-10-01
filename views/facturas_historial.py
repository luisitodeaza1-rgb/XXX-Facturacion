import tkinter as tk
from tkinter import ttk, messagebox

from Services.Facturas_historial_services import (
    obtener_facturas,
    obtener_factura,
    obtener_detalle_factura,
    buscar_facturas
)


class HistorialFacturas:

    def __init__(self, padre):

        self.padre = padre

        self.crear_interfaz()
        self.cargar_facturas()

    # ==========================================
    # INTERFAZ
    # ==========================================

    def crear_interfaz(self):

        titulo = tk.Label(
            self.padre,
            text="Historial de facturas",
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
            text="Consulta y revisión de facturas realizadas",
            font=("Arial", 11),
            bg="#f3f4f6",
            fg="#6b7280"
        )

        subtitulo.pack(
            anchor="w",
            padx=30
        )

        # ==========================================
        # HERRAMIENTAS
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
            "Buscar factura..."
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

        contenedor = tk.Frame(
            self.padre,
            bg="#f3f4f6"
        )

        contenedor.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 20)
        )

        columnas = (
            "id",
            "numero",
            "cliente",
            "rnc",
            "fecha",
            "subtotal",
            "itbis",
            "total"
        )

        self.tabla = ttk.Treeview(
            contenedor,
            columns=columnas,
            show="headings"
        )

        encabezados = {
            "id": "ID",
            "numero": "Factura",
            "cliente": "Cliente",
            "rnc": "RNC",
            "fecha": "Fecha",
            "subtotal": "Subtotal",
            "itbis": "ITBIS",
            "total": "Total"
        }

        for columna, texto in encabezados.items():

            self.tabla.heading(
                columna,
                text=texto
            )

        self.tabla.column(
            "id",
            width=50,
            anchor="center"
        )

        self.tabla.column(
            "numero",
            width=100
        )

        self.tabla.column(
            "cliente",
            width=180
        )

        self.tabla.column(
            "rnc",
            width=120
        )

        self.tabla.column(
            "fecha",
            width=150
        )

        self.tabla.column(
            "subtotal",
            width=110,
            anchor="e"
        )

        self.tabla.column(
            "itbis",
            width=110,
            anchor="e"
        )

        self.tabla.column(
            "total",
            width=120,
            anchor="e"
        )

        scrollbar = ttk.Scrollbar(
            contenedor,
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
        # BOTÓN
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

        boton_ver = tk.Button(
            botones,
            text="Ver factura",
            command=self.ver_factura,
            width=15,
            cursor="hand2"
        )

        boton_ver.pack(
            side="left"
        )

        self.tabla.bind(
            "<Double-1>",
            lambda evento: self.ver_factura()
        )

    # ==========================================
    # CARGAR FACTURAS
    # ==========================================

    def cargar_facturas(self):

        for fila in self.tabla.get_children():

            self.tabla.delete(fila)

        facturas = obtener_facturas()

        self.insertar_facturas(
            facturas
        )

    # ==========================================
    # INSERTAR EN TABLA
    # ==========================================

    def insertar_facturas(self, facturas):

        for factura in facturas:

            self.tabla.insert(
                "",
                "end",
                values=(
                    factura[0],
                    factura[1],
                    factura[2] or "",
                    factura[3] or "",
                    factura[4],
                    f"RD$ {factura[5]:,.2f}",
                    f"RD$ {factura[6]:,.2f}",
                    f"RD$ {factura[7]:,.2f}"
                )
            )

    # ==========================================
    # BÚSQUEDA
    # ==========================================

    def limpiar_placeholder(self, evento):

        if self.busqueda.get() == "Buscar factura...":

            self.busqueda.delete(
                0,
                tk.END
            )

    def buscar(self, evento=None):

        texto = self.busqueda.get().strip()

        if texto == "" or texto == "Buscar factura...":

            self.cargar_facturas()

            return

        facturas = buscar_facturas(
            texto
        )

        for fila in self.tabla.get_children():

            self.tabla.delete(fila)

        self.insertar_facturas(
            facturas
        )

    # ==========================================
    # VER FACTURA
    # ==========================================

    def ver_factura(self):

        seleccion = self.tabla.selection()

        if not seleccion:

            messagebox.showwarning(
                "Seleccionar factura",
                "Seleccione una factura."
            )

            return

        datos = self.tabla.item(
            seleccion[0],
            "values"
        )

        factura_id = datos[0]

        factura = obtener_factura(
            factura_id
        )

        detalle = obtener_detalle_factura(
            factura_id
        )

        self.mostrar_detalle(
            factura,
            detalle
        )

    # ==========================================
    # VENTANA DETALLE
    # ==========================================

    def mostrar_detalle(
        self,
        factura,
        detalle
    ):

        ventana = tk.Toplevel(
            self.padre
        )

        ventana.title(
            f"Factura {factura[1]}"
        )

        ventana.geometry(
            "750x550"
        )

        ventana.resizable(
            False,
            False
        )

        ventana.transient(
            self.padre
        )

        # ==========================================
        # ENCABEZADO
        # ==========================================

        tk.Label(
            ventana,
            text=f"Factura {factura[1]}",
            font=("Arial", 22, "bold")
        ).pack(
            pady=(20, 5)
        )

        tk.Label(
            ventana,
            text=f"Fecha: {factura[4]}",
            font=("Arial", 10)
        ).pack()

        tk.Label(
            ventana,
            text=f"Cliente: {factura[2] or 'Sin cliente'}",
            font=("Arial", 10)
        ).pack(
            pady=(5, 20)
        )

        # ==========================================
        # TABLA DETALLE
        # ==========================================

        contenedor = tk.Frame(
            ventana
        )

        contenedor.pack(
            fill="both",
            expand=True,
            padx=30
        )

        columnas = (
            "codigo",
            "producto",
            "cantidad",
            "precio",
            "subtotal"
        )

        tabla = ttk.Treeview(
            contenedor,
            columns=columnas,
            show="headings"
        )

        tabla.heading(
            "codigo",
            text="Código"
        )

        tabla.heading(
            "producto",
            text="Producto"
        )

        tabla.heading(
            "cantidad",
            text="Cantidad"
        )

        tabla.heading(
            "precio",
            text="Precio"
        )

        tabla.heading(
            "subtotal",
            text="Subtotal"
        )

        tabla.column(
            "codigo",
            width=100
        )

        tabla.column(
            "producto",
            width=250
        )

        tabla.column(
            "cantidad",
            width=80,
            anchor="center"
        )

        tabla.column(
            "precio",
            width=110,
            anchor="e"
        )

        tabla.column(
            "subtotal",
            width=120,
            anchor="e"
        )

        tabla.pack(
            fill="both",
            expand=True
        )

        for item in detalle:

            tabla.insert(
                "",
                "end",
                values=(
                    item[0] or "",
                    item[1],
                    item[2],
                    f"RD$ {item[3]:,.2f}",
                    f"RD$ {item[4]:,.2f}"
                )
            )

        # ==========================================
        # TOTALES
        # ==========================================

        totales = tk.Frame(
            ventana
        )

        totales.pack(
            fill="x",
            padx=30,
            pady=20
        )

        tk.Label(
            totales,
            text=f"Subtotal: RD$ {factura[5]:,.2f}",
            font=("Arial", 11)
        ).pack(
            anchor="e"
        )

        tk.Label(
            totales,
            text=f"ITBIS: RD$ {factura[6]:,.2f}",
            font=("Arial", 11)
        ).pack(
            anchor="e"
        )

        tk.Label(
            totales,
            text=f"Total: RD$ {factura[7]:,.2f}",
            font=("Arial", 16, "bold")
        ).pack(
            anchor="e"
        )