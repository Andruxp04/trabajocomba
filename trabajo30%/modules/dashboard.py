import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from config import COLOR_FONDO
from modules.database import (
    total_productos,
    total_clientes,
    total_proveedores,
    total_ventas,
    total_ventas_dinero,
    productos_bajo_stock,
    productos_mas_vendidos,
    ultimas_ventas,
    resumen_inventario
)

# Paleta oficial de Luffy
LUFFY_RED = "#D62828"
LUFFY_BLUE = "#003049"
LUFFY_YELLOW = "#FDF0D5"
LUFFY_GOLD = "#F77F00"
LUFFY_DARK = "#1E1E1E"
LUFFY_VINOTINTO = "#971F1F"

class DashboardFrame(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_FONDO)
        self.crear_dashboard()

    def crear_tarjeta(self, parent, titulo, valor, color_fondo, color_texto="white"):
        card = tk.Frame(parent, bg=color_fondo, width=200, height=90)
        card.pack_propagate(False)

        tk.Label(
            card, text=titulo, bg=color_fondo, fg=color_texto, font=("Segoe UI", 9, "bold")
        ).pack(pady=(12, 2))

        tk.Label(
            card, text=str(valor), bg=color_fondo, fg=color_texto, font=("Segoe UI", 18, "bold")
        ).pack()

        return card

    def crear_dashboard(self):
        # Título principal
        titulo = tk.Label(
            self,
            text="🏴‍☠️ DASHBOARD PRINCIPAL 🏴‍☠️",
            bg=COLOR_FONDO,
            fg=LUFFY_VINOTINTO,
            font=("Segoe UI", 18, "bold"),
        )
        titulo.pack(pady=10)

        # ----------------------------------------------------
        # SEC-1: TARJETAS KPI RESUMEN
        # ----------------------------------------------------
        resumen = resumen_inventario()
        ventas_dinero = f"${total_ventas_dinero():,.0f}"
        valor_inv = f"${resumen['valor_inventario']:,.0f}"

        kpi_frame = tk.Frame(self, bg=COLOR_FONDO)
        kpi_frame.pack(fill="x", padx=15, pady=5)

        self.crear_tarjeta(kpi_frame, "INGRESOS VENTAS", ventas_dinero, LUFFY_RED).pack(side="left", padx=5)
        self.crear_tarjeta(kpi_frame, "VALOR INVENTARIO", valor_inv, LUFFY_BLUE).pack(side="left", padx=5)
        self.crear_tarjeta(kpi_frame, "TOTAL PRODUCTOS", resumen['total_items'], LUFFY_GOLD).pack(side="left", padx=5)
        self.crear_tarjeta(kpi_frame, "UNIDADES EN STOCK", resumen['total_unidades'], LUFFY_VINOTINTO).pack(side="left", padx=5)
        self.crear_tarjeta(kpi_frame, "CLIENTES", total_clientes(), LUFFY_DARK).pack(side="left", padx=5)

        # ----------------------------------------------------
        # SEC-2: ÁREA CENTRAL (GRÁFICO + ÚLTIMAS VENTAS)
        # ----------------------------------------------------
        mid_frame = tk.Frame(self, bg=COLOR_FONDO)
        mid_frame.pack(fill="both", expand=True, padx=15, pady=10)

        # Gráfico de Productos Más Vendidos (Matplotlib)
        chart_container = tk.Frame(mid_frame, bg="white", highlightbackground=LUFFY_BLUE, highlightthickness=1)
        chart_container.pack(side="left", fill="both", expand=True, padx=(0, 5))

        mas_vendidos = productos_mas_vendidos()
        nombres = [item[0] for item in mas_vendidos] if mas_vendidos else ["Sin Datos"]
        cantidades = [item[1] for item in mas_vendidos] if mas_vendidos else [0]

        fig, ax = plt.subplots(figsize=(5, 3), dpi=90)
        fig.patch.set_facecolor('white')
        ax.set_facecolor('white')

        bars = ax.barh(nombres, cantidades, color=LUFFY_RED)
        ax.set_title("Top 5 Productos Más Vendidos", fontsize=11, fontweight='bold', color=LUFFY_DARK)
        ax.invert_yaxis()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(LUFFY_DARK)
        ax.spines['bottom'].set_color(LUFFY_DARK)

        canvas = FigureCanvasTkAgg(fig, master=chart_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
        plt.close(fig)

        # Tabla Últimas Ventas
        ventas_container = tk.LabelFrame(
            mid_frame, text=" ÚLTIMAS VENTAS ", bg="white", fg=LUFFY_BLUE, font=("Segoe UI", 10, "bold")
        )
        ventas_container.pack(side="right", fill="both", expand=True, padx=(5, 0))

        tree_v = ttk.Treeview(
            ventas_container, columns=("num", "fecha", "total", "pago"), show="headings", height=6
        )
        tree_v.heading("num", text="N° Venta")
        tree_v.heading("fecha", text="Fecha")
        tree_v.heading("total", text="Total")
        tree_v.heading("pago", text="Pago")

        tree_v.column("num", width=80, anchor="center")
        tree_v.column("fecha", width=110, anchor="center")
        tree_v.column("total", width=90, anchor="e")
        tree_v.column("pago", width=90, anchor="center")
        tree_v.pack(fill="both", expand=True, padx=5, pady=5)

        for v in ultimas_ventas():
            tree_v.insert("", "end", values=(v[0], v[1], f"${v[2]:,.0f}", v[3]))

        # ----------------------------------------------------
        # SEC-3: TABLA PRODUCTOS CON BAJO STOCK
        # ----------------------------------------------------
        alert_frame = tk.LabelFrame(
            self, text=" ⚠️ ALERTA: PRODUCTOS CON BAJO STOCK (<= 10) ", bg="white", fg=LUFFY_RED, font=("Segoe UI", 10, "bold")
        )
        alert_frame.pack(fill="x", padx=15, pady=(0, 10))

        tree_stock = ttk.Treeview(
            alert_frame, columns=("codigo", "nombre", "precio", "stock"), show="headings", height=4
        )
        tree_stock.heading("codigo", text="Código")
        tree_stock.heading("nombre", text="Producto")
        tree_stock.heading("precio", text="Precio")
        tree_stock.heading("stock", text="Stock Actual")

        tree_stock.column("codigo", width=100, anchor="center")
        tree_stock.column("nombre", width=400)
        tree_stock.column("precio", width=120, anchor="e")
        tree_stock.column("stock", width=100, anchor="center")
        tree_stock.pack(fill="both", expand=True, padx=5, pady=5)

        # Cargar productos de bajo stock directamente usando la función existente
        for prod in productos_bajo_stock(limite=10):
            tree_stock.insert("", "end", values=(prod[0], prod[1], f"${prod[2]:,.0f}", prod[3]))