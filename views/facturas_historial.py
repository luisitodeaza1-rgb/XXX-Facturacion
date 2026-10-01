import tkinter as tk
from tkinter import ttk, messagebox

from Services.Facturas_historial_services import (
    obtener_facturas,
    obtener_factura,
    obtener_detalle_factura,
    buscar_facturas,
    obtener_totales_facturas,
    eliminar_factura
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
            text="Consulta, revisión y gestión de facturas realizadas",
            font=("Arial", 11),
            bg="#f3f4f6",
            fg="#6b7280"
        )

        subtitulo.pack(
            anchor="w",
            padx=30
        )

        # ==========================================
        # RESUMEN
        # ==========================================

        resumen = tk.Frame(
            self.padre,
            bg="#f3f4f6"
        )

        resumen.pack(
            fill="x",
            padx=30,
            pady=(20, 5)
        )

        self.label_cantidad = tk.Label(
            resumen,
            text="Facturas: 0",
            font=("Arial", 11, "bold"),
            bg="#f3f4f6",
            fg="#374151"
        )

        self.label_cantidad.pack(
            side="left",
            padx=(0, 30)
        )

        self.label_subtotal = tk.Label(
            resumen,
            text="Subtotal: RD$ 0.00",
            font=("Arial", 11),
            bg="#f3f4f6",
            fg="#374151"
        )

        self.label_subtotal.pack(
            side="left",
            padx=(0, 30)
        )

        self.label_itbis = tk.Label(
            resumen,
            text="ITBIS: RD$ 0.00",
            font=("Arial", 11),
            bg="#f3f4f6",
            fg="#374151"
        )

        self.label_itbis.pack(
            side="left",
            padx=(0, 30)
        )

        self.label_total = tk.Label(
            resumen,
            text="Total facturado: RD$ 0.00",
            font=("Arial", 11, "bold"),
            bg="#f3f4f6",
            fg="#111827"
        )

        self.label_total.pack(
            side="left"
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
            pady=15
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
            width=220
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

        boton_eliminar = tk.Button(
            botones,
            text="Eliminar factura",
            command=self.eliminar_factura_seleccionada,
            width=18,
            bg="#dc2626",
            fg="white",
            activebackground="#b91c1c",
            activeforeground="white",
            relief="flat",
            cursor="hand2"
        )

        boton_eliminar.pack(
            side="left",
            padx=10
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

        self.actualizar_totales()

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
    # ACTUALIZAR TOTALES
    # ==========================================

    def actualizar_totales(self):

        cantidad, subtotal, itbis, total = (
            obtener_totales_facturas()
        )

        self.label_cantidad.config(
            text=f"Facturas: {cantidad}"
        )

        self.label_subtotal.config(
            text=f"Subtotal: RD$ {subtotal:,.2f}"
        )

        self.label_itbis.config(
            text=f"ITBIS: RD$ {itbis:,.2f}"
        )

        self.label_total.config(
            text=f"Total facturado: RD$ {total:,.2f}"
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

        # Los totales siguen mostrando
        # el total general del sistema.

        self.actualizar_totales()

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

        if not factura:

            messagebox.showerror(
                "Factura no encontrada",
                "La factura seleccionada ya no existe."
            )

            self.cargar_facturas()

            return

        detalle = obtener_detalle_factura(
            factura_id
        )

        self.mostrar_detalle(
            factura,
            detalle
        )

    # ==========================================
    # ELIMINAR FACTURA
    # ==========================================

    def eliminar_factura_seleccionada(self):

        seleccion = self.tabla.selection()

        if not seleccion:

            messagebox.showwarning(
                "Seleccionar factura",
                "Seleccione una factura para eliminar."
            )

            return

        datos = self.tabla.item(
            seleccion[0],
            "values"
        )

        factura_id = datos[0]
        numero_factura = datos[1]
        cliente = datos[2]
        total = datos[7]

        confirmar = messagebox.askyesno(
            "Eliminar factura",
            (
                f"¿Está seguro de eliminar la factura "
                f"{numero_factura}?\n\n"
                f"Cliente: {cliente}\n"
                f"Total: {total}\n\n"
                "Esta acción eliminará la factura y su detalle "
                "y devolverá los productos al inventario."
            )
        )

        if not confirmar:

            return

        try:

            numero_eliminado = eliminar_factura(
                factura_id
            )

            messagebox.showinfo(
                "Factura eliminada",
                (
                    f"La factura {numero_eliminado} "
                    "fue eliminada correctamente.\n\n"
                    "El stock de los productos fue restaurado."
                )
            )

            self.cargar_facturas()

        except Exception as error:

            messagebox.showerror(
                "Error",
                (
                    "No fue posible eliminar la factura.\n\n"
                    f"{error}"
                )
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
        ).pack()

        tk.Label(
            ventana,
            text=f"RNC: {factura[3] or 'Sin RNC'}",
            font=("Arial", 10)
        ).pack(
            pady=(3, 20)
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