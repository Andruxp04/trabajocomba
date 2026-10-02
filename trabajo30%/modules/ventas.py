import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from config import *
from modules.dashboard import LUFFY_BLUE, LUFFY_GOLD
from modules.database import (
    buscar_producto,
    registrar_venta,
    registrar_detalle,
    descontar_stock,
)


class VentasFrame(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_FONDO)
        self.cart = []
        self.producto_actual = None
        self.total_actual = 0
        self.generar_numero_venta()
        self.crear_interfaz()

    # NÚMERO DE VENTA
    # ========================
    def generar_numero_venta(self):
        self.numero_venta = "VTA-" + datetime.now().strftime("%Y%m%d%H%M%S")

    # =============================================
    # INTERFAZ
    def crear_interfaz(self):
        # =================
        # TÍTULO
        titulo = tk.Label(
            self,
            text="PUNTO DE VENTA (POS)",
            bg=COLOR_FONDO,
            font=("Segoe UI", 16, "bold"),
        )
        titulo.pack(pady=(5, 3))

        # ======================
        # INFORMACIÓN
        # ======================
        info = tk.Frame(self, bg=COLOR_FONDO)
        info.pack(fill="x", padx=10)

        self.lbl_factura = tk.Label(
            info,
            text=f"Factura: {self.numero_venta}",
            bg=COLOR_FONDO,
            font=("Segoe UI", 9, "bold"),
        )
        self.lbl_factura.pack(side="left")

        self.lbl_fecha = tk.Label(
            info,
            text=datetime.now().strftime("%d/%m/%Y %H:%M"),
            bg=COLOR_FONDO,
            font=("Segoe UI", 9),
        )
        self.lbl_fecha.pack(side="right")

        # ======================
        # BUSCADOR
        # ======================
        frm_busqueda = tk.LabelFrame(
            self, text=" AGREGAR PRODUCTO", bg=COLOR_BLANCO, padx=6, pady=5
        )
        frm_busqueda.pack(fill="x", padx=10, pady=5)

        # Código
        tk.Label(frm_busqueda, text="Código:", bg=COLOR_BLANCO).grid(
            row=0, column=0, padx=3
        )
        self.ent_codigo = tk.Entry(frm_busqueda, width=16)
        self.ent_codigo.grid(row=0, column=1, padx=3)
        self.ent_codigo.bind(
            "<Return>", lambda e: self.buscar_producto_ui()
        )

        # Buscar
        tk.Button(
            frm_busqueda,
            text="Buscar",
            bg=LUFFY_GOLD,
            fg="white",
            command=self.buscar_producto_ui,
        ).grid(row=0, column=2, padx=3)

        # Producto
        self.lbl_producto = tk.Label(
            frm_busqueda,
            text="Producto:",
            bg=COLOR_BLANCO,
            font=("Segoe UI", 9, "bold"),
        )
        self.lbl_producto.grid(row=0, column=3, padx=10, sticky="w")

        # Precio
        self.lbl_precio = tk.Label(
            frm_busqueda,
            text="$ 0",
            bg=COLOR_BLANCO,
            font=("Segoe UI", 9, "bold"),
        )
        self.lbl_precio.grid(row=0, column=4, padx=5)

        # Cantidad
        tk.Label(frm_busqueda, text="Cantidad:", bg=COLOR_BLANCO).grid(
            row=0, column=5, padx=3
        )
        self.spin_cantidad = tk.Spinbox(
            frm_busqueda, from_=1, to=100, width=4
        )
        self.spin_cantidad.grid(row=0, column=6, padx=3)

        # Agregar
        tk.Button(
            frm_busqueda,
            text="+ Agregar",
            bg=LUFFY_BLUE,
            fg="white",
            command=self.agregar_carrito,
        ).grid(row=0, column=7, padx=5)

        # ==================================================
        # CONTENEDOR PRINCIPAL
        # ==================================================
        contenido = tk.Frame(self, bg=COLOR_FONDO)
        contenido.pack(fill="both", expand=True, padx=10, pady=3)

        # ==================================
        # CARRITO IZQUIERDA
        # ==================================
        frame_carrito = tk.LabelFrame(
            contenido, text=" CARRITO DE COMPRA ", bg=COLOR_BLANCO
        )
        frame_carrito.pack(side="left", fill="both", expand=True, padx=(0, 5))

        # Treeview
        columnas = ("codigo", "producto", "cantidad", "precio", "subtotal")
        self.tree = ttk.Treeview(
            frame_carrito, columns=columnas, show="headings", height=8
        )
        self.tree.heading("codigo", text="CÓDIGO")
        self.tree.heading("producto", text="PRODUCTO")
        self.tree.heading("cantidad", text="CANT.")
        self.tree.heading("precio", text="PRECIO")
        self.tree.heading("subtotal", text="SUBTOTAL")

        self.tree.column("codigo", width=80, anchor="center")
        self.tree.column("producto", width=180)
        self.tree.column("cantidad", width=60, anchor="center")
        self.tree.column("precio", width=90, anchor="e")
        self.tree.column("subtotal", width=100, anchor="e")

        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        # BOTONES CARRITO
        botones_carrito = tk.Frame(frame_carrito, bg=COLOR_BLANCO)
        botones_carrito.pack(fill="x", padx=5, pady=5)

        tk.Button(
            botones_carrito,
            text="Eliminar",
            bg="#DC2626",
            fg="white",
            command=self.eliminar_item,
        ).pack(side="left", padx=3)

        tk.Button(
            botones_carrito,
            text="Limpiar",
            bg=LUFFY_GOLD,
            fg="white",
            command=self.limpiar_carrito,
        ).pack(side="left", padx=3)

        # ==================================
        # PANEL DERECHO
        # ==================================
        panel_derecho = tk.Frame(contenido, bg=COLOR_FONDO, width=280)
        panel_derecho.pack(side="right", fill="y", padx=(5, 0))
        panel_derecho.pack_propagate(False)

        # ======================
        # RESUMEN
        # ======================
        resumen = tk.LabelFrame(
            panel_derecho, text=" RESUMEN ", bg=COLOR_BLANCO, padx=8, pady=5
        )
        resumen.pack(fill="x", pady=(0, 5))

        self.lbl_subtotal = tk.Label(
            resumen, text="Subtotal: $0", bg=COLOR_BLANCO, anchor="e"
        )
        self.lbl_subtotal.pack(fill="x", pady=2)

        # Descuento
        descuento_frame = tk.Frame(resumen, bg=COLOR_BLANCO)
        descuento_frame.pack(fill="x", pady=2)

        tk.Label(descuento_frame, text="Descuento:", bg=COLOR_BLANCO).pack(
            side="left"
        )
        self.ent_descuento = tk.Entry(descuento_frame, width=10)
        self.ent_descuento.insert(0, "0")
        self.ent_descuento.pack(side="right")
        self.ent_descuento.bind(
            "<KeyRelease>", lambda e: self.actualizar_totales()
        )

        self.lbl_iva = tk.Label(
            resumen, text="IVA: $0", bg=COLOR_BLANCO, anchor="e"
        )
        self.lbl_iva.pack(fill="x", pady=2)

        self.lbl_total = tk.Label(
            resumen,
            text="$ 0",
            bg=LUFFY_GOLD,
            fg="white",
            font=("Segoe UI", 16, "bold"),
        )
        self.lbl_total.pack(fill="x", pady=5)

        # ==================================================
        # PAGO
        # ==================================================
        pago = tk.LabelFrame(
            panel_derecho, text=" MÉTODO DE PAGO ", bg=COLOR_BLANCO, padx=8, pady=5
        )
        pago.pack(fill="x", pady=5)

        tk.Label(pago, text="Método:", bg=COLOR_BLANCO).pack(anchor="w")
        self.cmb_pago = ttk.Combobox(
            pago, values=["Efectivo", "Tarjeta", "Transferencia"], state="readonly"
        )
        self.cmb_pago.current(0)
        self.cmb_pago.pack(fill="x", pady=3)

        tk.Label(pago, text="Valor recibido:", bg=COLOR_BLANCO).pack(anchor="w")
        self.ent_pagado = tk.Entry(pago)
        self.ent_pagado.pack(fill="x", pady=3)
        self.ent_pagado.bind(
            "<KeyRelease>", lambda e: self.calcular_cambio()
        )

        self.lbl_cambio = tk.Label(
            pago,
            text="Cambio: $0",
            bg=COLOR_BLANCO,
            fg="green",
            font=("Segoe UI", 11, "bold"),
        )
        self.lbl_cambio.pack(pady=5)

        # ======================
        # FACTURAR
        # ======================
        tk.Button(
            panel_derecho,
            text="FACTURAR VENTA",
            bg="#16A34A",
            fg="white",
            font=("Segoe UI", 12, "bold"),
            height=2,
            command=self.facturar,
        ).pack(fill="x", pady=8)

    # BUSCAR PRODUCTO
    def buscar_producto_ui(self):
        codigo = self.ent_codigo.get().strip()
        if not codigo:
            messagebox.showwarning(
                "Producto", "Ingrese el código del producto."
            )
            return
        producto = buscar_producto(codigo)
        if not producto:
            messagebox.showerror("Producto", "Producto no encontrado.")
            self.producto_actual = None
            self.lbl_producto.config(text="Producto:")
            self.lbl_precio.config(text="$ 0")
            return
        self.producto_actual = producto
        nombre = producto[1]
        precio = float(producto[2])
        stock = int(producto[3])
        self.lbl_producto.config(text=f"{nombre} | Stock: {stock}")
        self.lbl_precio.config(text=f"$ {precio:,.0f}")

    # =======================
    # AGREGAR CARRITO
    def agregar_carrito(self):
        if not self.producto_actual:
            messagebox.showwarning("Producto", "Primero busque un producto.")
            return
        try:
            cantidad = int(self.spin_cantidad.get())
        except ValueError:
            messagebox.showerror("Cantidad", "Ingrese una cantidad válida.")
            return
        if cantidad <= 0:
            messagebox.showwarning(
                "Cantidad", "La cantidad debe ser mayor que cero."
            )
            return
        codigo = self.producto_actual[0]
        nombre = self.producto_actual[1]
        precio = float(self.producto_actual[2])
        stock = int(self.producto_actual[3])

        # Buscar producto existente
        for item in self.cart:
            if item["codigo"] == codigo:
                nueva_cantidad = item["cantidad"] + cantidad
                if nueva_cantidad > stock:
                    disponible = stock - item["cantidad"]
                    messagebox.showerror(
                        "Stock insuficiente",
                        f"Solo puede agregar {disponible} unidades.",
                    )
                    return
                item["cantidad"] = nueva_cantidad
                item["subtotal"] = nueva_cantidad * precio
                self.refrescar_carrito()
                return

        # Producto nuevo
        if cantidad > stock:
            messagebox.showerror(
                "Stock insuficiente", f"Stock disponible: {stock}"
            )
            return
        self.cart.append(
            {
                "codigo": codigo,
                "nombre": nombre,
                "cantidad": cantidad,
                "precio": precio,
                "subtotal": cantidad * precio,
            }
        )
        self.refrescar_carrito()

    # =====================
    # REFRESCAR CARRITO
    # ====================
    def refrescar_carrito(self):
        self.tree.delete(*self.tree.get_children())
        for item in self.cart:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    item["codigo"],
                    item["nombre"],
                    item["cantidad"],
                    f"${item['precio']:,.0f}",
                    f"${item['subtotal']:,.0f}",
                ),
            )
        self.actualizar_totales()

    # ELIMINAR
    def eliminar_item(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Carrito", "Seleccione un producto.")
            return
        index = self.tree.index(seleccion[0])
        del self.cart[index]
        self.refrescar_carrito()

    # ======================
    # LIMPIAR
    # ======================
    def limpiar_carrito(self):
        if self.cart:
            confirmar = messagebox.askyesno(
                "Limpiar", "¿Desea limpiar la venta actual?"
            )
            if not confirmar:
                return
        self.cart.clear()
        self.producto_actual = None
        self.tree.delete(*self.tree.get_children())
        self.ent_codigo.delete(0, tk.END)
        self.ent_pagado.delete(0, tk.END)
        self.ent_descuento.delete(0, tk.END)
        self.ent_descuento.insert(0, "0")
        self.spin_cantidad.delete(0, tk.END)
        self.spin_cantidad.insert(0, "1")
        self.lbl_producto.config(text="Producto:")
        self.lbl_precio.config(text="$ 0")
        self.lbl_cambio.config(text="Cambio: $0", fg="green")
        self.generar_numero_venta()
        self.lbl_factura.config(text=f"Factura: {self.numero_venta}")
        self.actualizar_totales()

    # ACTUALIZAR TOTALES
    # ========================
    def actualizar_totales(self):
        subtotal = sum(item["subtotal"] for item in self.cart)
        try:
            descuento = float(self.ent_descuento.get() or 0)
        except ValueError:
            descuento = 0
        if descuento < 0:
            descuento = 0
        if descuento > subtotal:
            descuento = subtotal
        base = subtotal - descuento
        iva = base * IVA
        total = base + iva
        self.total_actual = total
        self.lbl_subtotal.config(text=f"Subtotal: ${subtotal:,.0f}")
        self.lbl_iva.config(text=f"IVA: ${iva:,.0f}")
        self.lbl_total.config(text=f"$ {total:,.0f}")
        self.calcular_cambio()

    # CAMBIO
    def calcular_cambio(self):
        try:
            pagado = float(self.ent_pagado.get() or 0)
        except ValueError:
            pagado = 0
        cambio = pagado - self.total_actual
        if pagado == 0:
            self.lbl_cambio.config(text="Cambio: $0", fg="green")
        elif cambio < 0:
            self.lbl_cambio.config(
                text=f"Faltan: ${abs(cambio):,.0f}", fg="red"
            )
        else:
            self.lbl_cambio.config(text=f"Cambio: ${cambio:,.0f}", fg="green")

    # =======================
    # FACTURAR
    def facturar(self):
        if not self.cart:
            messagebox.showwarning("Venta", "No hay productos en el carrito.")
            return
        subtotal = sum(item["subtotal"] for item in self.cart)
        try:
            descuento = float(self.ent_descuento.get() or 0)
        except ValueError:
            messagebox.showerror(
                "Descuento", "El descuento debe ser numérico."
            )
            return
        if descuento < 0:
            messagebox.showerror(
                "Descuento", "El descuento no puede ser negativo."
            )
            return
        if descuento > subtotal:
            messagebox.showerror(
                "Descuento", "El descuento supera el subtotal."
            )
            return
        base = subtotal - descuento
        iva = base * IVA
        total = base + iva
        try:
            pagado = float(self.ent_pagado.get() or 0)
        except ValueError:
            messagebox.showerror("Pago", "Ingrese un valor recibido válido.")
            return
        if pagado < total:
            messagebox.showerror(
                "Pago insuficiente",
                f"Total: ${total:,.0f}\n"
                f"Pagado: ${pagado:,.0f}\n"
                f"Faltan: ${total - pagado:,.0f}",
            )
            return
        cambio = pagado - total
        metodo_pago = self.cmb_pago.get()
        confirmar = messagebox.askyesno(
            "Confirmar venta",
            f"Factura: {self.numero_venta}\n\n"
            f"Subtotal: ${subtotal:,.0f}\n"
            f"Descuento: ${descuento:,.0f}\n"
            f"IVA: ${iva:,.0f}\n"
            f"TOTAL: ${total:,.0f}\n\n"
            f"Pago: {metodo_pago}\n"
            f"Recibido: ${pagado:,.0f}\n"
            f"Cambio: ${cambio:,.0f}\n\n"
            "¿Confirmar venta?",
        )
        if not confirmar:
            return
        try:
            venta_id = registrar_venta(
                self.numero_venta,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "ADMIN",
                subtotal,
                descuento,
                iva,
                total,
                metodo_pago,
            )
            for item in self.cart:
                registrar_detalle(
                    venta_id,
                    item["codigo"],
                    item["nombre"],
                    item["cantidad"],
                    item["precio"],
                    item["subtotal"],
                )
                descontar_stock(item["codigo"], item["cantidad"])
            messagebox.showinfo(
                "Venta registrada",
                f"VENTA REGISTRADA\n\n"
                f"Factura: {self.numero_venta}\n"
                f"Total: ${total:,.0f}\n"
                f"Cambio: ${cambio:,.0f}",
            )
            # Nueva venta
            self.cart.clear()
            self.tree.delete(*self.tree.get_children())
            self.ent_codigo.delete(0, tk.END)
            self.ent_pagado.delete(0, tk.END)
            self.ent_descuento.delete(0, tk.END)
            self.ent_descuento.insert(0, "0")
            self.producto_actual = None
            self.lbl_producto.config(text="Producto:")
            self.lbl_precio.config(text="$ 0")
            self.lbl_cambio.config(text="Cambio: $0", fg="green")
            self.generar_numero_venta()
            self.lbl_factura.config(text=f"Factura: {self.numero_venta}")
            self.actualizar_totales()
        except Exception as e:
            messagebox.showerror(
                "Error", f"No se pudo registrar la venta:\n\n{e}"
            )