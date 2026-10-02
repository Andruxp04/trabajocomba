import tkinter as tk
from tkinter import messagebox, ttk
from config import *
from modules.database import conectar
from modules.inventario import LUFFY_BLUE, LUFFY_GOLD, LUFFY_RED, LUFFY_VINOTINTO


class ProveedoresFrame(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_FONDO)
        self.proveedor_id = None
        self.crear_interfaz()
        self.cargar_proveedores()

    # INTERFAZ
    def crear_interfaz(self):
        titulo = tk.Label(
            self,
            text="GESTIÓN DE PROVEEDORES",
            font=("Segoe UI", 18, "bold"),
            bg=COLOR_FONDO,
        )
        titulo.pack(pady=10)

        form = tk.LabelFrame(
            self, text="DATOS DEL PROVEEDOR", bg=COLOR_BLANCO, padx=10, pady=10
        )
        form.pack(fill="x", padx=10, pady=10)

        # NOMBRE
        tk.Label(form, text="Razón Social", bg=COLOR_BLANCO).grid(
            row=0, column=0, sticky="w"
        )
        self.ent_nombre = tk.Entry(form, width=40)
        self.ent_nombre.grid(row=1, column=0, padx=5, pady=5)

        # NIT
        tk.Label(form, text="NIT", bg=COLOR_BLANCO).grid(
            row=0, column=1, sticky="w"
        )
        self.ent_nit = tk.Entry(form, width=20)
        self.ent_nit.grid(row=1, column=1, padx=5, pady=5)

        # TELEFONO
        tk.Label(form, text="Teléfono", bg=COLOR_BLANCO).grid(
            row=0, column=2, sticky="w"
        )
        self.ent_telefono = tk.Entry(form, width=20)
        self.ent_telefono.grid(row=1, column=2, padx=5, pady=5)

        # DIRECCION
        tk.Label(form, text="Dirección", bg=COLOR_BLANCO).grid(
            row=2, column=0, sticky="w"
        )
        self.ent_direccion = tk.Entry(form, width=50)
        self.ent_direccion.grid(
            row=3, column=0, columnspan=2, padx=5, pady=5, sticky="we"
        )

        # ======================
        # BOTONES
        # ======================
        barra = tk.Frame(self, bg=COLOR_FONDO)
        barra.pack(fill="x", padx=10, pady=5)

        # ======================
        # BOTONES (PALETA LUFFY)
        # ======================
        barra = tk.Frame(self, bg=COLOR_FONDO)
        barra.pack(fill="x", padx=10, pady=5)

        tk.Button(
            barra,
            text="Guardar",
            bg=LUFFY_BLUE,
            fg="white",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            padx=10,
            command=self.guardar_proveedor,
        ).pack(side="left", padx=5)

        tk.Button(
            barra,
            text="Actualizar",
            bg=LUFFY_GOLD,
            fg="white",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            padx=10,
            command=self.actualizar_proveedor,
        ).pack(side="left", padx=5)

        tk.Button(
            barra,
            text="Eliminar",
            bg=LUFFY_RED,
            fg="white",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            padx=10,
            command=self.eliminar_proveedor,
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

        # ======================
        # BUSCADOR
        # ======================
        frame_busqueda = tk.Frame(self, bg=COLOR_FONDO)
        frame_busqueda.pack(fill="x", padx=10, pady=10)

        tk.Label(frame_busqueda, text="Buscar:", bg=COLOR_FONDO).pack(
            side="left"
        )
        self.ent_buscar = tk.Entry(frame_busqueda, width=40)
        self.ent_buscar.pack(side="left", padx=5)

        tk.Button(
            frame_busqueda, text="Buscar", command=self.buscar_proveedor
        ).pack(side="left")

        # ======================
        # TREEVIEW
        # ======================
        frame_tree = tk.Frame(self)
        frame_tree.pack(expand=True, fill="both", padx=10, pady=10)

        columnas = ("id", "nombre", "nit", "telefono", "direccion")

        self.tree = ttk.Treeview(
            frame_tree, columns=columnas, show="headings"
        )
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="RAZÓN SOCIAL")
        self.tree.heading("nit", text="NIT")
        self.tree.heading("telefono", text="TELÉFONO")
        self.tree.heading("direccion", text="DIRECCIÓN")

        self.tree.column("id", width=60)
        self.tree.column("nombre", width=250)
        self.tree.column("nit", width=150)
        self.tree.column("telefono", width=150)
        self.tree.column("direccion", width=250)

        self.tree.pack(expand=True, fill="both")
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_proveedor)

    # =====================
    # CRUD
    # =====================
    def guardar_proveedor(self):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO proveedores (nombre, nit, telefono, direccion)
            VALUES (?, ?, ?, ?)
        """,
            (
                self.ent_nombre.get(),
                self.ent_nit.get(),
                self.ent_telefono.get(),
                self.ent_direccion.get(),
            ),
        )
        conn.commit()
        conn.close()
        messagebox.showinfo("Éxito", "Proveedor registrado correctamente")
        self.cargar_proveedores()
        self.limpiar_formulario()

    def actualizar_proveedor(self):
        if not self.proveedor_id:
            return
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE proveedores
            SET nombre=?, nit=?, telefono=?, direccion=?
            WHERE id=?
        """,
            (
                self.ent_nombre.get(),
                self.ent_nit.get(),
                self.ent_telefono.get(),
                self.ent_direccion.get(),
                self.proveedor_id,
            ),
        )
        conn.commit()
        conn.close()
        self.cargar_proveedores()
        messagebox.showinfo("Actualizado", "Proveedor actualizado correctamente")
        self.limpiar_formulario()

    def eliminar_proveedor(self):
        if not self.proveedor_id:
            return
        confirmar = messagebox.askyesno(
            "Confirmar", "¿Desea eliminar el proveedor?"
        )
        if not confirmar:
            return
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            """
            DELETE FROM proveedores
            WHERE id=?
        """,
            (self.proveedor_id,),
        )
        conn.commit()
        conn.close()
        self.cargar_proveedores()
        self.limpiar_formulario()

    def cargar_proveedores(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM proveedores
            ORDER BY nombre
        """
        )
        datos = cursor.fetchall()
        conn.close()
        for fila in datos:
            self.tree.insert("", tk.END, values=fila)

    def buscar_proveedor(self):
        texto = self.ent_buscar.get().strip()
        for item in self.tree.get_children():
            self.tree.delete(item)
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM proveedores
            WHERE nombre LIKE ? OR nit LIKE ?
        """,
            (f"%{texto}%", f"%{texto}%"),
        )
        resultados = cursor.fetchall()
        conn.close()
        for fila in resultados:
            self.tree.insert("", tk.END, values=fila)

    def seleccionar_proveedor(self, event):
        seleccion = self.tree.selection()
        if not seleccion:
            return
        datos = self.tree.item(seleccion)["values"]
        self.proveedor_id = datos[0]
        self.limpiar_formulario(False)
        self.ent_nombre.insert(0, datos[1])
        self.ent_nit.insert(0, datos[2])
        self.ent_telefono.insert(0, datos[3])
        self.ent_direccion.insert(0, datos[4])

    def limpiar_formulario(self, reset_id=True):
        self.ent_nombre.delete(0, tk.END)
        self.ent_nit.delete(0, tk.END)
        self.ent_telefono.delete(0, tk.END)
        self.ent_direccion.delete(0, tk.END)

        if reset_id:
            self.proveedor_id = None