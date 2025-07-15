import sqlite3


def crear_base():
    conexion = sqlite3.connect("productos.db")
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventario (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   nombre TEXT NOT NULL,
                   descripcion TEXT,
                   stock INTEGER NOT NULL,
                   precio REAL NOT NULL,
                   categoria TEXT
                   )
    """)

    conexion.commit()
    conexion.close()

#registracion de productos nuevos
def agregar_productos():
    conexion = sqlite3.connect("productos.db")
    cursor = conexion.cursor()

    #Ingreso de nombre
    while True:
        try:
            nombre = input("Ingrese el nombre del producto:").strip().lower()
            if nombre == "":
                raise ValueError ("El campo esta vacio.")
            else:
                 print("Nombre cargado")
            break
        except ValueError as error:
             print("Error:", error)
        continue

        #cargar a la base DB
    #Ingreso de descripcion
    while True:
        try:
            descripcion = input("Ingrese la descripcion del producto:").strip().lower()
            if descripcion == "":
                raise ValueError ("El campo esta vacio.")
            else:
                print("Descripcion cargada")
            break
        except ValueError as error:
            print("Error:", error)
            continue
    #Ingreso de categoria
    while True:
        try:
            categoria = input("Ingrese la categoria del producto:")
            if categoria == "":
                raise ValueError ("El campo esta vacio.")
            else:
                print("Categoria cargada")
            break
        except ValueError as error:
            print("Error:", error)
            continue

    #Ingreso de precio
    while True:
        try:
            precio = float(input("Ingrese el precio del producto: ")) 
            if precio <= 0:
                raise ValueError()
            else:
                print("Precio cargado")
                break


        except ValueError:
            print ("El valor ingresado no es valido.")
            continue

    #Ingreso de stock
    while True:
        try:
            cantidad = int(input("Ingrese la cantidad del producto: "))
            if cantidad < 0:
                raise ValueError()
            else:
                print("Cantidad Cargada")
                break


        except ValueError:
            print ("El valor ingresado no es valido.")
            continue

    

    try:
        conexion.execute("BEGIN")

        cursor.execute("INSERT into inventario (nombre, descripcion, stock, precio, categoria) VALUES (?, ?, ?, ?, ?) ", (nombre, descripcion, cantidad, precio, categoria))
        print ("Producto cargado correctamente.")

        conexion.commit()

    except sqlite3.IntegrityError as error:
        conexion.rollback()
        print(f"Error al cargar el producto: {error} ")
    except Exception as error:
        conexion.rollback()
        print(f"Ocurrio un error: {error}")
    finally:
        conexion.close()

def mostrar_productos():
        
    conexion = sqlite3.connect("productos.db")
    cursor = conexion.cursor()

    cursor.execute ("SELECT * FROM inventario")
    productos = cursor.fetchall()
    print ("Lista de productos:")
    for productos in productos:
        print(f"ID:{productos[0]} - Nombre:{productos[1]} - Descripcion: {productos[2]} - Stock: {productos[3]} - precio: {productos[4]} - categoria: {productos[5]}")


def actualizar_productos(prod_id, nuevo_nombre):
    conexion = sqlite3.connect("productos.db")
    cursor = conexion.cursor()

    cursor.execute ("UPDATE inventario SET nombre = ? WHERE id = ?", (nuevo_nombre, prod_id)) 
    
    conexion.commit()
    

    # Opcional: verificar si se modificó al menos una fila
    if cursor.rowcount == 0:
        print(f"No se encontró producto con ID = {prod_id}.") 
    else:
        print(f"Nombre actualizado a '{nuevo_nombre}' para el producto ID {prod_id}.")
    conexion.close()

def eliminar_productos():
    try:

        conexion = sqlite3.connect("productos.db")
        cursor = conexion.cursor()

        cursor.execute("BEGIN TRANSACTION")

        id = input("Ingrese el ID del producto:")

        cursor.execute("DELETE FROM inventario WHERE id = ?" , (id,) )
        conexion.commit()
    except sqlite3.Error as e:
        print (f"Error: {e}")
        conexion.rollback()
    finally:
        conexion.close()

def busqueda_productos():
    try:
        print("1. Ver los productos")
        print("2. Buscar productos")

        opcion = input("Seleccione una opcion: ")

        conexion = sqlite3.connect("productos.db")
        cursor = conexion.cursor()


        if opcion == "1":
            cursor.execute("SELECT * FROM inventario")
        elif opcion == "2":
            id_buscar= input("Ingrese el Id del producto a buscar:")
            cursor.execute("SELECT * FROM inventario WHERE id = ?", (id_buscar))
        else:
            print("Opcion invalida")
            conexion.close()
            return
        productos = cursor.fetchall()

        if productos:
            for productos in productos:

                print(f"ID:{productos[0]} - Nombre:{productos[1]} - Descripcion: {productos[2]} - Stock: {productos[3]} - precio: {productos[4]} - categoria: {productos[5]}")

        else:
            print("No se encontro Id")
    except Exception as error:
        print("Ocurrio un error {error}")

def reporte_stock(limite):
    conexion = sqlite3.connect("productos.db")
    cursor = conexion.cursor()
    cursor.execute(
    "SELECT id, nombre, descripcion, stock, precio, categoria "
    "FROM inventario "
    "WHERE stock <= ?",
    (limite,)
)
    filas = cursor.fetchall()
    conexion.close()
    return filas
def mostrar_reporte_simple(filas, limite):
    if not filas:
        print(f"No hay productos con stock ≤ {limite}.")
        return
    print(f"\nProductos con stock ≤ {limite}:")
    print(f"{'ID':<3} {'Nombre':<20} {'Cant.':<6} {'Precio':<7} {'Categoría'}")
    print('-' * 60)
    for id_, nombre, descripcion, cantidad, precio, categoria in filas:
        print(f"{id_:<3} {nombre:<20} {cantidad:<6} {precio:<7.2f} {categoria}")
    print()

   
    

def menu():
    crear_base()
    while True:
        print ("1. Menu")
        print ("2. Mostrar Productos")
        print ("3. Modificar/Actualizar Producto")
        print ("4. Eliminar productos")
        print ("5. Buscar productos")
        print ("6. Reporte de quiebre de stock")
        print("7. Actualizar productos")
        print ("8. Salir")

        opcion = input("Ingrese una opcion: ")

        if opcion == "1":
            agregar_productos()
            continue
        elif opcion == "2":
            mostrar_productos()
        elif opcion == "3":
            prod_id = int(input("ID del producto a actualizar: "))
            nuevo_nombre = input("Nuevo nombre: ")
            actualizar_productos(prod_id, nuevo_nombre)
            print("Producto actualizado.\n")

        elif opcion == "4":
            eliminar_productos()
        elif opcion == "5":
            busqueda_productos()
        elif opcion == '6':
            try:
                lim = int(input("Ingrese límite de stock: "))
            except ValueError:
                print("Por favor ingresa un número válido.\n")
                continue
            filas = reporte_stock(lim)
            mostrar_reporte_simple(filas, lim)
    

        elif opcion == "8":
            print ("Salir del programa")
            break
        else:
            print("La opcion ingresada no es valida.")


if __name__ == "__main__":
    menu()
            

