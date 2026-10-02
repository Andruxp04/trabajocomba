import sqlite3
from config import DB_NAME


# ==========================================
# CONEXIÓN A LA BASE DE DATOS
# ==========================================
def conectar():
    return sqlite3.connect(DB_NAME)


# ==========================================
# CREAR TABLAS
# ==========================================
def crear_tablas():
    conn = conectar()
    cursor = conn.cursor()

    # PRODUCTOS
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS productos (
            codigo TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """
    )

    # CLIENTES
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            tipo_documento TEXT,
            documento TEXT,
            telefono TEXT,
            direccion TEXT,
            sexo TEXT,
            email TEXT
        )
    """
    )

    # PROVEEDORES
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS proveedores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            nit TEXT,
            telefono TEXT,
            direccion TEXT
        )
    """
    )

    # VENTAS
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_venta TEXT NOT NULL,
            fecha TEXT NOT NULL,
            vendedor TEXT NOT NULL,
            subtotal REAL NOT NULL,
            descuento REAL NOT NULL,
            iva REAL NOT NULL,
            total REAL NOT NULL,
            metodo_pago TEXT NOT NULL
        )
    """
    )

    # DETALLE DE VENTA
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS detalle_venta (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            venta_id INTEGER NOT NULL,
            codigo_producto TEXT NOT NULL,
            producto TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL,
            subtotal REAL NOT NULL,
            FOREIGN KEY (venta_id) REFERENCES ventas(id)
        )
    """
    )

    conn.commit()
    conn.close()


# ==========================================
# PRODUCTOS DE PRUEBA
# ==========================================
# ==========================================
# PRODUCTOS DE PRUEBA AMPLIADOS
# ==========================================
def insertar_productos_prueba():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM productos")
    cantidad = cursor.fetchone()[0]

    if cantidad == 0:
        productos = [
            # Bebidas y Snacks
            ("1001", "Coca Cola 400ml", 3500, 150),
            ("1002", "Galletas Oreo 36g", 2000, 80),
            ("1003", "Papas Margarita Natural 45g", 2500, 60),
            ("1004", "Jugo Hit Mora 500ml", 3000, 90),
            ("1005", "Agua Brisa Sin Gas 600ml", 2000, 100),
            ("1006", "Cerveza Poker Lata 330ml", 3800, 200),
            ("1007", "Chocolatina Jet 12g", 700, 300),
            
            # Lácteos y Despensa
            ("2001", "Leche Alpina Entera 1L", 5000, 70),
            ("2002", "Arroz Diana 500g", 2800, 120),
            ("2003", "Aceite Gourmet 900ml", 14500, 45),
            ("2004", "Pan Tajado Bimbo Blanco", 6500, 30),
            ("2005", "Café Sello Rojo 250g", 8900, 50),
            ("2006", "Azúcar Incauca 1kg", 4200, 85),
            ("2007", "Huevo AA Rojo (Cubeta x30)", 18000, 25),
            ("2008", "Mantequilla Colanta 250g", 7800, 40),
            ("2009", "Atún Van Camp's en Agua", 7200, 65),

            # Aseo y Cuidado Personal
            ("3001", "Jabón Rey 300g", 2200, 110),
            ("3002", "Detergente Fab 1kg", 11500, 40),
            ("3003", "Crema Dental Colgate 100ml", 6800, 55),
            ("3004", "Papel Higiénico Familia (4 rollos)", 8500, 50),
            ("3005", "LAVAPLATOS AXION Crema 450g", 5400, 35)
        ]
        
        cursor.executemany(
            "INSERT INTO productos (codigo, nombre, precio, stock) VALUES (?, ?, ?, ?)",
            productos,
        )
        conn.commit()

    conn.close()


# ==========================================
# OBTENER PRODUCTOS

def obtener_productos():
    conn = conectar()
    cursor = conn.cursor()
    
    # Se cambia "ORDER BY nombre" por "ORDER BY CAST(codigo AS INTEGER) ASC"
    cursor.execute("""
        SELECT codigo, nombre, precio, stock
        FROM productos
        ORDER BY CAST(codigo AS INTEGER) ASC
    """)
    
    datos = cursor.fetchall()
    conn.close()
    return datos

# ==========================================
# BUSCAR PRODUCTO
# ==========================================
def buscar_producto(codigo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT codigo, nombre, precio, stock
        FROM productos
        WHERE codigo = ?
    """,
        (codigo,),
    )
    producto = cursor.fetchone()
    conn.close()
    return producto


# ==========================================
# AGREGAR PRODUCTO
# ==========================================
def agregar_producto(codigo, nombre, precio, stock):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO productos (codigo, nombre, precio, stock)
            VALUES (?, ?, ?, ?)
        """,
            (codigo, nombre, precio, stock),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


# ==========================================
# ACTUALIZAR PRODUCTO
# ==========================================
def actualizar_producto(codigo, nombre, precio, stock):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE productos
        SET nombre = ?, precio = ?, stock = ?
        WHERE codigo = ?
    """,
        (nombre, precio, stock, codigo),
    )
    actualizado = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return actualizado


# ==========================================
# ELIMINAR PRODUCTO
# ==========================================
def eliminar_producto(codigo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """
        DELETE FROM productos
        WHERE codigo = ?
    """,
        (codigo,),
    )
    eliminado = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return eliminado


# ==========================================
# DESCONTAR STOCK
# ==========================================
def descontar_stock(codigo, cantidad):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE productos
        SET stock = stock - ?
        WHERE codigo = ? AND stock >= ?
    """,
        (cantidad, codigo, cantidad),
    )
    actualizado = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return actualizado


# ==========================================
# AUMENTAR STOCK
# ==========================================
def actualizar_stock(codigo, cantidad):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE productos
        SET stock = stock + ?
        WHERE codigo = ?
    """,
        (cantidad, codigo),
    )
    actualizado = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return actualizado


# ==========================================
# DASHBOARD
# ==========================================
def total_productos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM productos")
    total = cursor.fetchone()[0]
    conn.close()
    return total


def total_clientes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM clientes")
    total = cursor.fetchone()[0]
    conn.close()
    return total


def total_proveedores():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM proveedores")
    total = cursor.fetchone()[0]
    conn.close()
    return total


def total_ventas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM ventas")
    total = cursor.fetchone()[0]
    conn.close()
    return total


# ==========================================
# REGISTRAR VENTA
# ==========================================
def registrar_venta(
    numero_venta, fecha, vendedor, subtotal, descuento, iva, total, metodo_pago
):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO ventas (numero_venta, fecha, vendedor, subtotal, descuento, iva, total, metodo_pago)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                numero_venta,
                fecha,
                vendedor,
                subtotal,
                descuento,
                iva,
                total,
                metodo_pago,
            ),
        )
        venta_id = cursor.lastrowid
        conn.commit()
        return venta_id
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# ==========================================
# REGISTRAR DETALLE DE VENTA
# ==========================================
def registrar_detalle(
    venta_id, codigo_producto, producto, cantidad, precio, subtotal
):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO detalle_venta (venta_id, codigo_producto, producto, cantidad, precio, subtotal)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (venta_id, codigo_producto, producto, cantidad, precio, subtotal),
        )
        conn.commit()
        return True
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# ==========================================
# OBTENER VENTAS
# ==========================================
def obtener_ventas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, numero_venta, fecha, vendedor, subtotal, descuento, iva, total, metodo_pago
        FROM ventas
        ORDER BY fecha DESC
    """
    )
    ventas = cursor.fetchall()
    conn.close()
    return ventas


# ==========================================
# OBTENER DETALLE DE VENTA
# ==========================================
def obtener_detalle_venta(venta_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, venta_id, codigo_producto, producto, cantidad, precio, subtotal
        FROM detalle_venta
        WHERE venta_id = ?
    """,
        (venta_id,),
    )
    detalle = cursor.fetchall()
    conn.close()
    return detalle


# ==========================================
# TOTAL DINERO EN VENTAS
# ==========================================
def total_ventas_dinero():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT COALESCE(SUM(total), 0) FROM ventas")
    total = cursor.fetchone()[0]
    conn.close()
    return total


# ==========================================
# PRODUCTOS CON BAJO STOCK
# ==========================================
def productos_bajo_stock(limite=10):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT codigo, nombre, precio, stock
        FROM productos
        WHERE stock <= ?
        ORDER BY stock ASC
    """,
        (limite,),
    )
    datos = cursor.fetchall()
    conn.close()
    return datos


# ==========================================
# REGISTRAR VENTA COMPLETA
# ==========================================
def registrar_venta_completa(
    numero_venta,
    fecha,
    vendedor,
    subtotal,
    descuento,
    iva,
    total,
    metodo_pago,
    carrito,
):
    conexion = conectar()
    try:
        cursor = conexion.cursor()

        # 1. GUARDAR CABECERA DE LA VENTA
        cursor.execute(
            """
            INSERT INTO ventas (numero_venta, fecha, vendedor, subtotal, descuento, iva, total, metodo_pago)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                numero_venta,
                fecha,
                vendedor,
                subtotal,
                descuento,
                iva,
                total,
                metodo_pago,
            ),
        )
        venta_id = cursor.lastrowid

        # 2. GUARDAR DETALLES
        for item in carrito:
            codigo = item["codigo"]
            nombre = item["nombre"]
            cantidad = item["cantidad"]
            precio = item["precio"]
            subtotal_item = item["subtotal"]

            # Verificar stock nuevamente
            cursor.execute(
                "SELECT stock FROM productos WHERE codigo = ?", (codigo,)
            )
            resultado = cursor.fetchone()
            if not resultado:
                raise Exception(f"El producto {codigo} ya no existe.")

            stock_actual = int(resultado[0])
            if stock_actual < cantidad:
                raise Exception(
                    f"Stock insuficiente para {nombre}.\n"
                    f"Disponible: {stock_actual}\n"
                    f"Solicitado: {cantidad}"
                )

            # Guardar detalle
            cursor.execute(
                """
                INSERT INTO detalle_venta (venta_id, codigo_producto, producto, cantidad, precio, subtotal)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (venta_id, codigo, nombre, cantidad, precio, subtotal_item),
            )

            # Descontar inventario
            cursor.execute(
                """
                UPDATE productos
                SET stock = stock - ?
                WHERE codigo = ?
            """,
                (cantidad, codigo),
            )

        # 3. GUARDAR TODO
        conexion.commit()
        return venta_id

    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()

# =============================================
# CONSULTAS AVANZADAS PARA EL DASHBOARD
# =============================================

def productos_mas_vendidos(limite=5):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT producto, SUM(cantidad) as total_vendido
        FROM detalle_venta
        GROUP BY codigo_producto
        ORDER BY total_vendido DESC
        LIMIT ?
    """, (limite,))
    datos = cursor.fetchall()
    conn.close()
    return datos

def ultimas_ventas(limite=5):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT numero_venta, fecha, total, metodo_pago
        FROM ventas
        ORDER BY id DESC
        LIMIT ?
    """, (limite,))
    datos = cursor.fetchall()
    conn.close()
    return datos

def resumen_inventario():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*), COALESCE(SUM(stock), 0), COALESCE(SUM(precio * stock), 0) FROM productos")
    resumen = cursor.fetchone()
    conn.close()
    return {
        "total_items": resumen[0],
        "total_unidades": resumen[1],
        "valor_inventario": resumen[2]
    }

# ==========================================
# CLIENTES DE PRUEBA
# ==========================================
def insertar_clientes_prueba():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM clientes")
    cantidad = cursor.fetchone()[0]

    if cantidad == 0:
        clientes = [
            ("Carlos Mendoza", "Cédula de Ciudadanía", "1045238901", "Masculino", "3001234567", "Calle 45 #12-34", "carlos.mendoza@gmail.com"),
            ("María Fernanda Gómez", "Cédula de Ciudadanía", "1082940123", "Femenino", "3159876543", "Carrera 10 #5-20", "mafe.gomez@hotmail.com"),
            ("Comercializadora El Sol SAS", "NIT", "900123456-1", "Otro / LGBT+", "6053501122", "Zona Industrial Lt 4", "ventas@elsol.com"),
            ("Andrés Felipe Ruiz", "Tarjeta de Identidad", "1098765432", "Masculino", "3024567890", "Av. Circunvalar #88-12", "andres.ruiz@yahoo.com")
        ]
        
        cursor.executemany("""
            INSERT INTO clientes (nombre, tipo_documento, documento, sexo, telefono, direccion, email)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, clientes)
        
        conn.commit()

    conn.close()