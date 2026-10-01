import tkinter as tk

from views.Cliente import Clientes
from views.Product import Productos
from views.facturas import Facturacion
from views.facturas_historial import HistorialFacturas
from views.Reportes import Reportes
from views.Configuracion import Configuracion

from Services.Client_services import obtener_clientes
from Services.Product_services import obtener_productos
from Services.Reportes_services import obtener_resumen


class Dashboard:

    def __init__(self, root, usuario):

        self.root = root
        self.usuario = usuario

        self.root.title("XXX Facturador - Dashboard")
        self.root.geometry("1100x650")
        self.root.minsize(900, 550)

        self.crear_interfaz()

    # ==========================================
    # INTERFAZ
    # ==========================================

    def crear_interfaz(self):

        self.sidebar = tk.Frame(
            self.root,
            width=220,
            bg="#1f2937"
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(False)

        titulo = tk.Label(
            self.sidebar,
            text="XXX\nFACTURADOR",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#1f2937"
        )

        titulo.pack(
            pady=30
        )

        botones = [
            ("Inicio", self.inicio),
            ("Clientes", self.clientes),
            ("Productos", self.productos),
            ("Facturación", self.facturacion),
            ("Historial", self.historial),
            ("Reportes", self.reportes),
            ("Configuración", self.configuracion)
        ]

        for texto, comando in botones:

            boton = tk.Button(
                self.sidebar,
                text=texto,
                command=comando,
                font=("Arial", 11),
                fg="white",
                bg="#374151",
                activebackground="#4b5563",
                activeforeground="white",
                relief="flat",
                anchor="w",
                padx=20,
                height=2,
                cursor="hand2"
            )

            boton.pack(
                fill="x",
                padx=10,
                pady=3
            )

        self.contenido = tk.Frame(
            self.root,
            bg="#f3f4f6"
        )

        self.contenido.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.mostrar_inicio()

    # ==========================================
    # INICIO
    # ==========================================

    def mostrar_inicio(self):

        self.limpiar_contenido()

        titulo = tk.Label(
            self.contenido,
            text="Dashboard",
            font=("Arial", 28, "bold"),
            bg="#f3f4f6",
            fg="#111827"
        )

        titulo.pack(
            anchor="w",
            padx=30,
            pady=(30, 5)
        )

        bienvenida = tk.Label(
            self.contenido,
            text=f"Bienvenido, {self.usuario}",
            font=("Arial", 14),
            bg="#f3f4f6",
            fg="#4b5563"
        )

        bienvenida.pack(
            anchor="w",
            padx=30
        )

        # ==========================================
        # OBTENER ESTADÍSTICAS
        # ==========================================

        try:

            resumen = obtener_resumen()

            total_clientes = resumen["clientes"]
            total_productos = resumen["productos"]
            total_facturas = resumen["facturas"]
            total_ventas = resumen["ventas"]

        except Exception:

            total_clientes = len(
                obtener_clientes()
            )

            total_productos = len(
                obtener_productos()
            )

            total_facturas = 0
            total_ventas = 0

        # ==========================================
        # TARJETAS
        # ==========================================

        tarjetas = tk.Frame(
            self.contenido,
            bg="#f3f4f6"
        )

        tarjetas.pack(
            fill="x",
            padx=30,
            pady=40
        )

        self.crear_tarjeta(
            tarjetas,
            "Clientes",
            str(total_clientes),
            0
        )

        self.crear_tarjeta(
            tarjetas,
            "Productos",
            str(total_productos),
            1
        )

        self.crear_tarjeta(
            tarjetas,
            "Facturas",
            str(total_facturas),
            2
        )

        self.crear_tarjeta(
            tarjetas,
            "Ventas",
            f"RD$ {total_ventas:,.2f}",
            3
        )

        # ==========================================
        # INFORMACIÓN
        # ==========================================

        informacion = tk.Frame(
            self.contenido,
            bg="white",
            relief="solid",
            borderwidth=1
        )

        informacion.pack(
            fill="x",
            padx=30,
            pady=10
        )

        tk.Label(
            informacion,
            text="XXX Facturador",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#111827"
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        tk.Label(
            informacion,
            text=(
                "Sistema de gestión para clientes, productos, "
                "inventario y facturación."
            ),
            font=("Arial", 10),
            bg="white",
            fg="#6b7280"
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 20)
        )

    # ==========================================
    # TARJETAS
    # ==========================================

    def crear_tarjeta(
        self,
        padre,
        titulo,
        valor,
        columna
    ):

        tarjeta = tk.Frame(
            padre,
            bg="white",
            width=180,
            height=120,
            relief="solid",
            borderwidth=1
        )

        tarjeta.grid(
            row=0,
            column=columna,
            padx=10,
            sticky="nsew"
        )

        tarjeta.grid_propagate(False)

        tk.Label(
            tarjeta,
            text=titulo,
            font=("Arial", 11),
            bg="white",
            fg="#6b7280"
        ).pack(
            pady=(20, 5)
        )

        tk.Label(
            tarjeta,
            text=valor,
            font=("Arial", 20, "bold"),
            bg="white",
            fg="#111827"
        ).pack()

    # ==========================================
    # LIMPIAR
    # ==========================================

    def limpiar_contenido(self):

        for widget in self.contenido.winfo_children():

            widget.destroy()

    # ==========================================
    # INICIO
    # ==========================================

    def inicio(self):

        self.mostrar_inicio()

    # ==========================================
    # CLIENTES
    # ==========================================

    def clientes(self):

        self.limpiar_contenido()

        Clientes(
            self.contenido
        )

    # ==========================================
    # PRODUCTOS
    # ==========================================

    def productos(self):

        self.limpiar_contenido()

        Productos(
            self.contenido
        )

    # ==========================================
    # FACTURACIÓN
    # ==========================================

    def facturacion(self):

        self.limpiar_contenido()

        Facturacion(
            self.contenido
        )

    # ==========================================
    # HISTORIAL
    # ==========================================

    def historial(self):

        self.limpiar_contenido()

        HistorialFacturas(
            self.contenido
        )

    # ==========================================
    # REPORTES
    # ==========================================

    def reportes(self):

        self.limpiar_contenido()

        Reportes(
            self.contenido
        )

    # ==========================================
    # CONFIGURACIÓN
    # ==========================================

    def configuracion(self):

        self.limpiar_contenido()

        Configuracion(
            self.contenido
        )