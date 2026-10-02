import tkinter as tk
from config import *
from modules.database import crear_tablas, insertar_productos_prueba
from modules.dashboard import DashboardFrame
from modules.inventario import InventarioFrame
from modules.clientes import ClientesFrame
from modules.proveedores import ProveedoresFrame
from modules.ventas import VentasFrame

# Paleta oficial de Luffy
LUFFY_RED = "#D62828"
LUFFY_BLUE = "#003049"
LUFFY_YELLOW = "#FDF0D5"
LUFFY_GOLD = "#F77F00"
LUFFY_DARK = "#1E1E1E"
LUFFY_VINOTINTO = "#971F1F"

# Asignación de colores por pestaña/módulo
COLORES_MODULOS = {
    "Dashboard": LUFFY_VINOTINTO,
    "Ventas": LUFFY_VINOTINTO,
    "Inventario": LUFFY_VINOTINTO,
    "Clientes": LUFFY_VINOTINTO,
    "Proveedores": LUFFY_VINOTINTO,
    "Cuentas por Cobrar": LUFFY_VINOTINTO,
    "Cuentas por Pagar": LUFFY_VINOTINTO,
    "Reportes": LUFFY_VINOTINTO,
    "Auditoría": LUFFY_VINOTINTO,
    "Cerrar Sesión": LUFFY_VINOTINTO,
}




class ERPApp:

    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("1366x768")
        self.root.configure(bg=COLOR_FONDO)

        self.botones_menu = {}
        self.crear_interfaz()

    def crear_interfaz(self):
        # SIDEBAR
        sidebar = tk.Frame(self.root, bg=COLOR_SECUNDARIO, width=220)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # LOGO
        tk.Label(
            sidebar,
            text="ERP EMPRESARIAL",
            bg=COLOR_SECUNDARIO,
            fg="white",
            font=("Segoe UI", 13, "bold"),
        ).pack(pady=(20, 5))

        tk.Label(
            sidebar, text="Versión 1.0", bg=COLOR_SECUNDARIO, fg="#94A3B8"
        ).pack()

        # MENÚ
        menus = [
            "Dashboard",
            "Ventas",
            "Inventario",
            "Clientes",
            "Proveedores",
            "Cuentas por Cobrar",
            "Cuentas por Pagar",
            "Reportes",
            "Auditoría",
            "Cerrar Sesión",
        ]

        for opcion in menus:
            btn = tk.Button(
                sidebar,
                text=opcion,
                bg=COLOR_SECUNDARIO,
                fg="white",
                relief="flat",
                anchor="w",
                padx=15,
                activebackground="#334155",
                activeforeground="white",
                command=lambda op=opcion: self.cargar_modulo(op),
            )
            btn.pack(fill="x", padx=1)
            self.botones_menu[opcion] = btn

        # FOOTER SIDEBAR
        footer = tk.Frame(sidebar, bg="#0F172A")
        footer.pack(side="bottom", fill="x")

        tk.Label(footer, text=EMPRESA, bg="#0F172A", fg="white").pack(
            anchor="w", padx=10, pady=(10, 7)
        )

        tk.Label(
            footer, text=f"NIT: {NIT}", bg="#0F172A", fg="#94A3B8"
        ).pack(anchor="w", padx=10, pady=(0, 10))

        # ÁREA CENTRAL
        self.workspace = tk.Frame(self.root, bg=COLOR_FONDO)
        self.workspace.pack(expand=True, fill="both")

        # Cargar módulo inicial
        self.cargar_modulo("Dashboard")

    def limpiar_workspace(self):
        for widget in self.workspace.winfo_children():
            widget.destroy()

    def cargar_modulo(self, modulo):
        # 1. Actualizar colores de selección en el menú
        for op, btn in self.botones_menu.items():
            btn.config(bg=COLOR_SECUNDARIO, activebackground="#334155")

        if modulo in self.botones_menu:
            color_pestana = COLORES_MODULOS.get(modulo, LUFFY_RED)
            self.botones_menu[modulo].config(
                bg=color_pestana, activebackground=color_pestana
            )

        # 2. Renderizar contenido en el workspace
        self.limpiar_workspace()

        if modulo == "Dashboard":
            DashboardFrame(self.workspace).pack(expand=True, fill="both")
        elif modulo == "Inventario":
            InventarioFrame(self.workspace).pack(expand=True, fill="both")
        elif modulo == "Clientes":
            ClientesFrame(self.workspace).pack(expand=True, fill="both")
        elif modulo == "Proveedores":
            ProveedoresFrame(self.workspace).pack(expand=True, fill="both")
        elif modulo == "Ventas":
            VentasFrame(self.workspace).pack(expand=True, fill="both")
        else:
            tk.Label(
                self.workspace,
                text=f"Módulo {modulo} en construcción",
                bg=COLOR_FONDO,
                font=("Segoe UI", 18, "bold"),
            ).pack(pady=100)


# INICIO DE APLICACIÓN
if __name__ == "__main__":
    crear_tablas()
    insertar_productos_prueba()
    root = tk.Tk()
    root.iconbitmap("icono.ico")  # Asegúrate de poner la ruta de tu archivo
    app = ERPApp(root)
    root.mainloop()