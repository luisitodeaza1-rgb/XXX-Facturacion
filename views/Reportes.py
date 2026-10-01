import tkinter as tk
from tkinter import ttk, messagebox

from Services.Reportes_services import (
    obtener_resumen,
    obtener_ventas_por_dia,
    obtener_productos_mas_vendidos
)


class Reportes:

    def __init__(self, padre):

        self.padre = padre

        self.crear_interfaz()
        self.cargar_datos()

    # ==========================================
    # INTERFAZ
    # ==========================================

    def crear_interfaz(self):

        titulo = tk.Label(
            self.padre,
            text="Reportes",
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
            text="Resumen de operaciones y rendimiento del negocio",
            font=("Arial", 11),
            bg="#f3f4f6",
            fg="#6b7280"
        )

        subtitulo.pack(
            anchor="w",
            padx=30
        )

        # ==========================================
        # TARJETAS
        # ==========================================

        tarjetas = tk.Frame(
            self.padre,
            bg="#f3f4f6"
        )

        tarjetas.pack(
            fill="x",
            padx=30,
            pady=25
        )

        self.facturas_valor = self.crear_tarjeta(
            tarjetas,
            "Facturas",
            0
        )

        self.ventas_valor = self.crear_tarjeta(
            tarjetas,
            "Ventas",
            "RD$ 0.00"
        )

        self.clientes_valor = self.crear_tarjeta(
            tarjetas,
            "Clientes",
            0
        )

        self.productos_valor = self.crear_tarjeta(
            tarjetas,
            "Productos",
            0
        )

        # ==========================================
        # BOTÓN ACTUALIZAR
        # ==========================================

        boton_actualizar = tk.Button(
            self.padre,
            text="Actualizar reportes",
            command=self.cargar_datos,
            bg="#2563eb",
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=7
        )

        boton_actualizar.pack(
            anchor="e",
            padx=30,
            pady=(0, 15)
        )

        # ==========================================
        # CONTENEDOR DE REPORTES
        # ==========================================

        contenido = tk.Frame(
            self.padre,
            bg="#f3f4f6"
        )

        contenido.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 20)
        )

        # ==========================================
        # VENTAS POR DÍA
        # ==========================================

        ventas_frame = tk.Frame(
            contenido,
            bg="white",
            relief="solid",
            borderwidth=1
        )

        ventas_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        tk.Label(
            ventas_frame,
            text="Ventas por día",
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#111827"
        ).pack(
            anchor="w",
            padx=15,
            pady=15
        )

        columnas_ventas = (
            "fecha",
            "facturas",
            "ventas"
        )

        self.tabla_ventas = ttk.Treeview(
            ventas_frame,
            columns=columnas_ventas,
            show="headings"
        )

        self.tabla_ventas.heading(
            "fecha",
            text="Fecha"
        )

        self.tabla_ventas.heading(
            "facturas",
            text="Facturas"
        )

        self.tabla_ventas.heading(
            "ventas",
            text="Ventas"
        )

        self.tabla_ventas.column(
            "fecha",
            width=120
        )

        self.tabla_ventas.column(
            "facturas",
            width=80,
            anchor="center"
        )

        self.tabla_ventas.column(
            "ventas",
            width=120,
            anchor="e"
        )

        self.tabla_ventas.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        # ==========================================
        # PRODUCTOS MÁS VENDIDOS
        # ==========================================

        productos_frame = tk.Frame(
            contenido,
            bg="white",
            relief="solid",
            borderwidth=1
        )

        productos_frame.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(10, 0)
        )

        tk.Label(
            productos_frame,
            text="Productos más vendidos",
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#111827"
        ).pack(
            anchor="w",
            padx=15,
            pady=15
        )

        columnas_productos = (
            "producto",
            "cantidad",
            "ventas"
        )

        self.tabla_productos = ttk.Treeview(
            productos_frame,
            columns=columnas_productos,
            show="headings"
        )

        self.tabla_productos.heading(
            "producto",
            text="Producto"
        )

        self.tabla_productos.heading(
            "cantidad",
            text="Cantidad"
        )

        self.tabla_productos.heading(
            "ventas",
            text="Ventas"
        )

        self.tabla_productos.column(
            "producto",
            width=200
        )

        self.tabla_productos.column(
            "cantidad",
            width=80,
            anchor="center"
        )

        self.tabla_productos.column(
            "ventas",
            width=120,
            anchor="e"
        )

        self.tabla_productos.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

    # ==========================================
    # TARJETA
    # ==========================================

    def crear_tarjeta(
        self,
        padre,
        titulo,
        valor
    ):

        tarjeta = tk.Frame(
            padre,
            bg="white",
            width=170,
            height=100,
            relief="solid",
            borderwidth=1
        )

        tarjeta.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        tarjeta.pack_propagate(False)

        tk.Label(
            tarjeta,
            text=titulo,
            font=("Arial", 10),
            bg="white",
            fg="#6b7280"
        ).pack(
            pady=(15, 5)
        )

        etiqueta = tk.Label(
            tarjeta,
            text=str(valor),
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#111827"
        )

        etiqueta.pack()

        return etiqueta

    # ==========================================
    # CARGAR DATOS
    # ==========================================

    def cargar_datos(self):

        try:

            resumen = obtener_resumen()

            self.facturas_valor.config(
                text=str(
                    resumen["facturas"]
                )
            )

            self.ventas_valor.config(
                text=f"RD$ {resumen['ventas']:,.2f}"
            )

            self.clientes_valor.config(
                text=str(
                    resumen["clientes"]
                )
            )

            self.productos_valor.config(
                text=str(
                    resumen["productos"]
                )
            )

            self.cargar_ventas()

            self.cargar_productos()

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"No se pudieron cargar los reportes.\n\n{error}"
            )

    # ==========================================
    # VENTAS
    # ==========================================

    def cargar_ventas(self):

        for fila in self.tabla_ventas.get_children():

            self.tabla_ventas.delete(fila)

        resultados = obtener_ventas_por_dia()

        for resultado in resultados:

            self.tabla_ventas.insert(
                "",
                "end",
                values=(
                    resultado[0],
                    resultado[1],
                    f"RD$ {resultado[2]:,.2f}"
                )
            )

    # ==========================================
    # PRODUCTOS
    # ==========================================

    def cargar_productos(self):

        for fila in self.tabla_productos.get_children():

            self.tabla_productos.delete(fila)

        resultados = obtener_productos_mas_vendidos()

        for resultado in resultados:

            self.tabla_productos.insert(
                "",
                "end",
                values=(
                    resultado[0],
                    resultado[1],
                    f"RD$ {resultado[2]:,.2f}"
                )
            )