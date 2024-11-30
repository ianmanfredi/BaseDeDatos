import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


class SistemaVentas:
    def __init__(self):
        self.conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="feli0386",
            database="Ventas"
        )
        self.cursor = self.conexion.cursor()

    def listar_productos(self):
        try:
            self.cursor.execute("SELECT * FROM Productos")
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo listar productos: {err}")
            return []

    def agregar_producto(self, nombre, descripcion, precio, stock, categoria):
        try:
            query = "INSERT INTO Productos (nombre, descripcion, precio, stock, categoria) VALUES (%s, %s, %s, %s, %s)"
            valores = (nombre, descripcion, float(precio), int(stock), categoria)
            self.cursor.execute(query, valores)
            self.conexion.commit()
            messagebox.showinfo("Éxito", "Producto agregado correctamente.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo agregar producto: {err}")

    def actualizar_producto(self, id_producto, nombre, descripcion, precio, stock, categoria):
        try:
            query = "UPDATE Productos SET nombre=%s, descripcion=%s, precio=%s, stock=%s, categoria=%s WHERE id_producto=%s"
            valores = (nombre, descripcion, float(precio), int(stock), categoria, id_producto)
            self.cursor.execute(query, valores)
            self.conexion.commit()
            messagebox.showinfo("Éxito", "Producto actualizado correctamente.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo actualizar el producto: {err}")

    def eliminar_producto(self, id_producto):
        try:
            query = "DELETE FROM Productos WHERE id_producto=%s"
            valores = (id_producto,)
            self.cursor.execute(query, valores)
            self.conexion.commit()
            messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo eliminar el producto: {err}")
            
    def listar_clientes(self):
        try:
            self.cursor.execute("SELECT * FROM Clientes")
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo listar clientes: {err}")
        return []
    
    def listar_ordenes(self):
        try:
            self.cursor.execute("""
                SELECT o.id_orden, o.fecha, c.nombre 
                FROM Ordenes o 
                INNER JOIN Clientes c ON o.id_cliente = c.id_cliente
            """)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo listar órdenes: {err}")
        return []
    
    def buscar_productos(self, filtro):
        try:
            query = """
                SELECT id_producto, nombre, precio 
                FROM Productos 
                WHERE nombre LIKE %s OR categoria LIKE %s
            """
            self.cursor.execute(query, (f"%{filtro}%", f"%{filtro}%"))
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo realizar la búsqueda: {err}")
        return []
    
    def reporte_mas_vendido(self):
        try:
            self.cursor.execute("""
                SELECT p.nombre, SUM(op.cantidad) AS total_vendido 
                FROM Orden_Producto op
                INNER JOIN Productos p ON op.id_producto = p.id_producto
                GROUP BY p.nombre
                ORDER BY total_vendido DESC
                LIMIT 5
            """)
            resultados = self.cursor.fetchall()
            return "\n".join([f"{r[0]} - Vendido: {r[1]}" for r in resultados])
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo generar el reporte: {err}")
            return "No disponible"

    def cerrar_conexion(self):
        self.cursor.close()
        self.conexion.close()


class App:
    def __init__(self, root):
        self.sistema = SistemaVentas()
        self.root = root
        self.root.title("Sistema de Gestión de Ventas")
        self.root.geometry("800x600")

        self.frame_productos = tk.Frame(root)
        self.frame_clientes = tk.Frame(root)
        self.frame_ordenes = tk.Frame(root)
        self.frame_busquedas = tk.Frame(root)
        self.frame_reporte = tk.Frame(root)

        boton_productos = tk.Button(root, text="Gestión de Productos", command=self.mostrar_frame_productos)
        boton_productos.pack(pady=5)

        boton_clientes = tk.Button(root, text="Gestión de Clientes", command=self.mostrar_frame_clientes)
        boton_clientes.pack(pady=5)

        boton_ordenes = tk.Button(root, text="Procesamiento de Órdenes", command=self.mostrar_frame_ordenes)
        boton_ordenes.pack(pady=5)

        boton_busquedas = tk.Button(root, text="Búsquedas Avanzadas", command=self.mostrar_frame_busquedas)
        boton_busquedas.pack(pady=5)

        boton_reporte = tk.Button(root, text="Reportes", command=self.mostrar_frame_reporte)
        boton_reporte.pack(pady=5)

        self.crear_menu_productos()
        self.crear_menu_clientes()
        self.crear_menu_ordenes()
        self.crear_menu_busquedas()
        self.crear_menu_reporte()

        self.mostrar_frame_productos()

    def crear_menu_productos(self):
        etiqueta = tk.Label(self.frame_productos, text="Gestión de Productos", font=("Arial", 16))
        etiqueta.pack(pady=10)

        self.lista_productos = tk.Listbox(self.frame_productos, width=80, height=10)
        self.lista_productos.pack(pady=10)

        botones_frame = tk.Frame(self.frame_productos)
        botones_frame.pack()

        boton_listar = tk.Button(botones_frame, text="Listar Productos", command=self.listar_productos)
        boton_listar.pack(side="left", padx=5)

        boton_agregar = tk.Button(botones_frame, text="Agregar Producto", command=self.ventana_agregar_producto)
        boton_agregar.pack(side="left", padx=5)

        boton_actualizar = tk.Button(botones_frame, text="Actualizar Producto", command=self.ventana_actualizar_producto)
        boton_actualizar.pack(side="left", padx=5)

        boton_eliminar = tk.Button(botones_frame, text="Eliminar Producto", command=self.ventana_eliminar_producto)
        boton_eliminar.pack(side="left", padx=5)

    def listar_productos(self):
        productos = self.sistema.listar_productos()
        self.lista_productos.delete(0, tk.END)
        for producto in productos:
            self.lista_productos.insert(tk.END, f"ID: {producto[0]} | {producto[1]} | ${producto[3]} | Stock: {producto[4]}")

    def ventana_agregar_producto(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Agregar Producto")
        ventana.geometry("400x300")

        tk.Label(ventana, text="Nombre:").grid(row=0, column=0, padx=10, pady=10)
        entry_nombre = tk.Entry(ventana)
        entry_nombre.grid(row=0, column=1)

        tk.Label(ventana, text="Descripción:").grid(row=1, column=0, padx=10, pady=10)
        entry_descripcion = tk.Entry(ventana)
        entry_descripcion.grid(row=1, column=1)

        tk.Label(ventana, text="Precio:").grid(row=2, column=0, padx=10, pady=10)
        entry_precio = tk.Entry(ventana)
        entry_precio.grid(row=2, column=1)

        tk.Label(ventana, text="Stock:").grid(row=3, column=0, padx=10, pady=10)
        entry_stock = tk.Entry(ventana)
        entry_stock.grid(row=3, column=1)

        tk.Label(ventana, text="Categoría:").grid(row=4, column=0, padx=10, pady=10)
        entry_categoria = tk.Entry(ventana)
        entry_categoria.grid(row=4, column=1)

        def guardar_producto():
            if not entry_nombre.get():
                messagebox.showerror("Error", "El nombre del producto es obligatorio.")
                return
            try:
                precio = float(entry_precio.get())
                if precio <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "El precio debe ser un número positivo.")
                return
            try:
                stock = int(entry_stock.get())
                if stock < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "El stock debe ser un número entero no negativo.")
                return
            self.sistema.agregar_producto(
                entry_nombre.get(),
                entry_descripcion.get(),
                precio,
                stock,
                entry_categoria.get()
            )
            self.listar_productos()
            ventana.destroy()

        tk.Button(ventana, text="Guardar", command=guardar_producto).grid(row=5, column=0, columnspan=2, pady=20)

    def ventana_actualizar_producto(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Actualizar Producto")
        ventana.geometry("400x350")

        tk.Label(ventana, text="ID del Producto:").grid(row=0, column=0, padx=10, pady=10)
        entry_id = tk.Entry(ventana)
        entry_id.grid(row=0, column=1)

        tk.Label(ventana, text="Nombre:").grid(row=1, column=0, padx=10, pady=10)
        entry_nombre = tk.Entry(ventana)
        entry_nombre.grid(row=1, column=1)

        tk.Label(ventana, text="Descripción:").grid(row=2, column=0, padx=10, pady=10)
        entry_descripcion = tk.Entry(ventana)
        entry_descripcion.grid(row=2, column=1)

        tk.Label(ventana, text="Precio:").grid(row=3, column=0, padx=10, pady=10)
        entry_precio = tk.Entry(ventana)
        entry_precio.grid(row=3, column=1)

        tk.Label(ventana, text="Stock:").grid(row=4, column=0, padx=10, pady=10)
        entry_stock = tk.Entry(ventana)
        entry_stock.grid(row=4, column=1)

        tk.Label(ventana, text="Categoría:").grid(row=5, column=0, padx=10, pady=10)
        entry_categoria = tk.Entry(ventana)
        entry_categoria.grid(row=5, column=1)

        def actualizar_producto():
            if not entry_id.get():
                messagebox.showerror("Error", "El ID del producto es obligatorio.")
                return
            if not entry_nombre.get():
                messagebox.showerror("Error", "El nombre del producto es obligatorio.")
                return
            try:
                precio = float(entry_precio.get())
                if precio <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "El precio debe ser un número positivo.")
                return
            try:
                stock = int(entry_stock.get())
                if stock < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "El stock debe ser un número entero no negativo.")
                return
            self.sistema.actualizar_producto(
                int(entry_id.get()),
                entry_nombre.get(),
                entry_descripcion.get(),
                precio,
                stock,
                entry_categoria.get()
            )
            self.listar_productos()
            ventana.destroy()

        tk.Button(ventana, text="Actualizar", command=actualizar_producto).grid(row=6, column=0, columnspan=2, pady=20)

    def ventana_eliminar_producto(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Eliminar Producto")
        ventana.geometry("300x150")

        tk.Label(ventana, text="ID del Producto:").pack(pady=10)
        entry_id = tk.Entry(ventana)
        entry_id.pack()

        def eliminar_producto():
            if not entry_id.get():
                messagebox.showerror("Error", "Debes ingresar el ID del producto a eliminar.")
                return
            if messagebox.askyesno("Confirmar Eliminación", "¿Estás seguro que deseas eliminar este producto?"):
                try:
                    id_producto = int(entry_id.get())
                except ValueError:
                    messagebox.showerror("Error", "El ID del producto debe ser un número entero.")
                    return
                self.sistema.eliminar_producto(id_producto)
                self.listar_productos()
                ventana.destroy()

        tk.Button(ventana, text="Eliminar", command=eliminar_producto).pack(pady=20)

    def crear_menu_clientes(self):
        etiqueta = tk.Label(self.frame_clientes, text="Gestión de Clientes", font=("Arial", 16))
        etiqueta.pack(pady=10)

        self.lista_clientes = tk.Listbox(self.frame_clientes, width=80, height=10)
        self.lista_clientes.pack(pady=10)

        botones_frame = tk.Frame(self.frame_clientes)
        botones_frame.pack()

        boton_listar = tk.Button(botones_frame, text="Listar Clientes", command=self.listar_clientes)
        boton_listar.pack(side="left", padx=5)

    def listar_clientes(self):
        clientes = self.sistema.listar_clientes()
        self.lista_clientes.delete(0, tk.END)
        for cliente in clientes:
            self.lista_clientes.insert(tk.END, f"ID: {cliente[0]} | {cliente[1]} | {cliente[2]}")

    def crear_menu_ordenes(self):
        etiqueta = tk.Label(self.frame_ordenes, text="Procesamiento de Órdenes", font=("Arial", 16))
        etiqueta.pack(pady=10)

        self.lista_ordenes = tk.Listbox(self.frame_ordenes, width=80, height=10)
        self.lista_ordenes.pack(pady=10)

        botones_frame = tk.Frame(self.frame_ordenes)
        botones_frame.pack()

        boton_listar = tk.Button(botones_frame, text="Listar Órdenes", command=self.listar_ordenes)
        boton_listar.pack(side="left", padx=5)

    def listar_ordenes(self):
        ordenes = self.sistema.listar_ordenes()
        self.lista_ordenes.delete(0, tk.END)
        for orden in ordenes:
            self.lista_ordenes.insert(tk.END, f"ID: {orden[0]} | Fecha: {orden[1]} | Cliente ID: {orden[2]}")

    def crear_menu_busquedas(self):
        etiqueta = tk.Label(self.frame_busquedas, text="Búsquedas Avanzadas", font=("Arial", 16))
        etiqueta.pack(pady=10)

        tk.Label(self.frame_busquedas, text="Filtro:").pack(pady=5)
        filtro_entry = tk.Entry(self.frame_busquedas)
        filtro_entry.pack(pady=5)

        def buscar():
            filtro = filtro_entry.get()
            productos = self.sistema.buscar_productos(filtro)
            resultados = "\n".join([f"{p[0]} - {p[1]}" for p in productos])
            messagebox.showinfo("Resultados", resultados if resultados else "No se encontraron productos.")

        tk.Button(self.frame_busquedas, text="Buscar Productos", command=buscar).pack(pady=10)

    def crear_menu_reporte(self):
        etiqueta = tk.Label(self.frame_reporte, text="Reporte de Productos Más Vendidos", font=("Arial", 16))
        etiqueta.pack(pady=10)

        def generar_reporte():
            reporte = self.sistema.reporte_mas_vendido()
            messagebox.showinfo("Reporte", reporte)

        tk.Button(self.frame_reporte, text="Generar Reporte", command=generar_reporte).pack(pady=10)

    def mostrar_frame_productos(self):
        self.frame_clientes.pack_forget()
        self.frame_ordenes.pack_forget()
        self.frame_busquedas.pack_forget()
        self.frame_reporte.pack_forget()
        self.frame_productos.pack(fill="both", expand=True)

    def mostrar_frame_clientes(self):
        self.frame_productos.pack_forget()
        self.frame_ordenes.pack_forget()
        self.frame_busquedas.pack_forget()
        self.frame_reporte.pack_forget()
        self.frame_clientes.pack(fill="both", expand=True)

    def mostrar_frame_ordenes(self):
        self.frame_productos.pack_forget()
        self.frame_clientes.pack_forget()
        self.frame_busquedas.pack_forget()
        self.frame_reporte.pack_forget()
        self.frame_ordenes.pack(fill="both", expand=True)

    def mostrar_frame_busquedas(self):
        self.frame_productos.pack_forget()
        self.frame_clientes.pack_forget()
        self.frame_ordenes.pack_forget()
        self.frame_reporte.pack_forget()
        self.frame_busquedas.pack(fill="both", expand=True)

    def mostrar_frame_reporte(self):
        self.frame_productos.pack_forget()
        self.frame_clientes.pack_forget()
        self.frame_ordenes.pack_forget()
        self.frame_busquedas.pack_forget()
        self.frame_reporte.pack(fill="both", expand=True)

    def cerrar_aplicacion(self):
        self.sistema.cerrar_conexion()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.protocol("WM_DELETE_WINDOW", app.cerrar_aplicacion)
    root.mainloop()
