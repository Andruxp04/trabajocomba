import tkinter as tk
from tkinter import ttk, messagebox
from config import *
from modules.database import (
    conectar,
    obtener_productos,
    agregar_producto,
    actualizar_producto,
    eliminar_producto,
    buscar_producto,
)

# Paleta oficial de Luffy
LUFFY_RED = "#D62828"        # Rojo chaleco
LUFFY_BLUE = "#003049"       # Azul pantalón / jeans
LUFFY_YELLOW = "#FDF0D5"     # Sombrero de paja
LUFFY_GOLD = "#F77F00"       # Cinta del sombrero / Dorado Haki
LUFFY_DARK = "#1E1E1E"       # Detalle oscuro / Cabello
LUFFY_VINOTINTO = "#971F1F"  # Vinotinto


class InventarioFrame(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_FONDO)
        self.crear_interfaz()
        self.cargar_productos()

    # =============================================
    # INTERFAZ GRÁFICA
    # =============================================
    def crear_interfaz(self):
        # Título estilo Luffy
        titulo = tk.Label(
            self,
            text="GESTIÓN DE INVENTARIO",
            bg=COLOR_FONDO,
            fg=LUFFY_VINOTINTO,
            font=("Segoe UI", 18, "bold"),
        )
        titulo.pack(pady=10)

        # Formulario
        form = tk.LabelFrame(
            self,
            text="DATOS DEL PRODUCTO",
            bg=COLOR_BLANCO,
            fg=LUFFY_BLUE,
            font=("Segoe UI", 10, "bold"),
            padx=10,
            pady=10,
        )
        form.pack(fill="x", padx=10, pady=10)

        # Campos
        tk.Label(form, text="Código", bg=COLOR_BLANCO, fg=LUFFY_DARK).grid(
            row=0, column=0, sticky="w"
        )
        self.ent_codigo = tk.Entry(form, width=20)
        self.ent_codigo.grid(row=1, column=0, padx=5, pady=5)

        tk.Label(form, text="Nombre", bg=COLOR_BLANCO, fg=LUFFY_DARK).grid(
            row=0, column=1, sticky="w"
        )
        self.ent_nombre = tk.Entry(form, width=40)
        self.ent_nombre.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form, text="Precio", bg=COLOR_BLANCO, fg=LUFFY_DARK).grid(
            row=0, column=2, sticky="w"
        )
        self.ent_precio = tk.Entry(form, width=15)
        self.ent_precio.grid(row=1, column=2, padx=5, pady=5)

        tk.Label(form, text="Stock", bg=COLOR_BLANCO, fg=LUFFY_DARK).grid(
            row=0, column=3, sticky="w"
        )
        self.ent_stock = tk.Entry(form, width=10)
        self.ent_stock.grid(row=1, column=3, padx=5, pady=5)

        # Botones de Acción
        barra = tk.Frame(self, bg=COLOR_FONDO)
        barra.pack(fill="x", padx=10)

        tk.Button(
            barra,
            text="Guardar",
            bg=LUFFY_BLUE,
            fg="white",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            padx=10,
            command=self.agregar_producto,
        ).pack(side="left", padx=5)

        tk.Button(
            barra,
            text="Actualizar",
            bg=LUFFY_GOLD,
            fg="white",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            padx=10,
            command=self.actualizar_producto,
        ).pack(side="left", padx=5)

        tk.Button(
            barra,
            text="Eliminar",
            bg=LUFFY_RED,
            fg="white",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            padx=10,
            command=self.eliminar_producto,
        ).pack(side="left", padx=5)

        tk.Button(
            barra,
            text="Limpiar",
            bg=LUFFY_VINOTINTO,
            fg="white",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            padx=10,
            command=self.limpiar_formulario,
        ).pack(side="left", padx=5)

        # Buscador
        busqueda = tk.Frame(self, bg=COLOR_FONDO)
        busqueda.pack(fill="x", padx=10, pady=10)

        tk.Label(
            busqueda,
            text="Buscar:",
            bg=COLOR_FONDO,
            fg=LUFFY_DARK,
            font=("Segoe UI", 10, "bold"),
        ).pack(side="left")

        self.ent_buscar = tk.Entry(busqueda)
        self.ent_buscar.pack(side="left", padx=5)

        tk.Button(
            busqueda,
            text="Buscar",
            bg=LUFFY_BLUE,
            fg="white",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            command=self.buscar_producto,
        ).pack(side="left")

        # Treeview (Tabla)
        frame_tree = tk.Frame(self)
        frame_tree.pack(expand=True, fill="both", padx=10, pady=10)

        # Estilo para la tabla
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview.Heading",
            background=LUFFY_BLUE,
            foreground="white",
            font=("Segoe UI", 10, "bold"),
        )
        style.configure(
            "Treeview",
            fieldbackground="white",
            rowheight=25,
        )
        style.map("Treeview", background=[("selected", LUFFY_GOLD)])

        columnas = ("codigo", "nombre", "precio", "stock")
        self.tree = ttk.Treeview(
            frame_tree, columns=columnas, show="headings"
        )

        self.tree.heading("codigo", text="Código")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("precio", text="Precio")
        self.tree.heading("stock", text="Stock")

        self.tree.column("codigo", width=100, anchor="center")
        self.tree.column("nombre", width=300)
        self.tree.column("precio", width=120, anchor="e")
        self.tree.column("stock", width=100, anchor="center")

        self.tree.pack(expand=True, fill="both")
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_producto)

    # =============================================
    # MÉTODOS CRUD
    # =============================================
    def agregar_producto(self):
        codigo = self.ent_codigo.get().strip()
        nombre = self.ent_nombre.get().strip()
        if not codigo or not nombre:
            messagebox.showwarning("Advertencia", "Código y Nombre son obligatorios")
            return

        try:
            precio = float(self.ent_precio.get())
            stock = int(self.ent_stock.get())
        except ValueError:
            messagebox.showerror("Error", "Precio o Stock inválido")
            return

        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO productos (codigo, nombre, precio, stock) VALUES (?, ?, ?, ?)",
                (codigo, nombre, precio, stock),
            )
            conn.commit()
            messagebox.showinfo("Éxito", "Producto agregado correctamente")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

        self.cargar_productos()
        self.limpiar_formulario()

    def actualizar_producto(self):
        codigo = self.ent_codigo.get().strip()
        if not codigo:
            messagebox.showwarning("Advertencia", "Seleccione un producto a actualizar")
            return

        try:
            precio = float(self.ent_precio.get())
            stock = int(self.ent_stock.get())
        except ValueError:
            messagebox.showerror("Error", "Valores inválidos")
            return

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE productos
            SET nombre = ?, precio = ?, stock = ?
            WHERE codigo = ?
            """,
            (self.ent_nombre.get().strip(), precio, stock, codigo),
        )
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", "Producto actualizado")
        self.cargar_productos()
        self.limpiar_formulario()

    def eliminar_producto(self):
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("Advertencia", "Seleccione un producto para eliminar")
            return

        codigo = self.tree.item(item)["values"][0]
        respuesta = messagebox.askyesno("Confirmar", "¿Eliminar producto?")
        if respuesta:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM productos WHERE codigo = ?", (codigo,))
            conn.commit()
            conn.close()

            self.cargar_productos()
            self.limpiar_formulario()

    def cargar_productos(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos ORDER BY nombre")
        datos = cursor.fetchall()
        conn.close()

        for fila in datos:
            self.tree.insert("", tk.END, values=fila)

    def buscar_producto(self):
        texto = self.ent_buscar.get().strip()
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM productos
            WHERE nombre LIKE ? OR codigo LIKE ?
            """,
            (f"%{texto}%", f"%{texto}%"),
        )
        productos = cursor.fetchall()
        conn.close()

        for item in productos:
            self.tree.insert("", tk.END, values=item)

    def seleccionar_producto(self, event):
        seleccion = self.tree.selection()
        if seleccion:
            valores = self.tree.item(seleccion)["values"]
            self.limpiar_formulario()
            self.ent_codigo.insert(0, valores[0])
            self.ent_nombre.insert(0, valores[1])
            self.ent_precio.insert(0, valores[2])
            self.ent_stock.insert(0, valores[3])

    def limpiar_formulario(self):
        self.ent_codigo.delete(0, tk.END)
        self.ent_nombre.delete(0, tk.END)
        self.ent_precio.delete(0, tk.END)
        self.ent_stock.delete(0, tk.END)