import modulo_apollo_general as ma
import sqlite3
    
def insertar_banda(conn, nombre_banda, pais, anio):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Bandas (Nombre_Banda, Pais_Origen, Anio_Formacion) 
        VALUES (?, ?, ?)
    """, (nombre_banda, pais, anio,))
    
    # TRUCO DE ORO: SQLite te devuelve el ID que acaba de generar
    return cursor.lastrowid

def agregar_banda(conn):
    while True:
        try:
            nombre = ma.comprobar_nombre_title("Ingresa el nombre de la nueva banda: ")
            id = ma.seleccionar_id(conn, "ID_Banda", "Bandas", "Nombre_Banda", nombre)
            if id is None:
                pais = ma.comprobar_nombre_title("Ingresa el pais de origen de esta banda: ")
                anio = ma.comprobar_num("Ingresa el año de formacion de esta banda: ")
                insertar_banda(conn, nombre, pais, anio)
                ma.guardar_cambios(conn)
                print (f"La banda {nombre} fue agregada con exito")
            else:
                print("La banda seleccionada ya estaba registrada. No se realizaron cambios.")
        
            if ma.si_no("Te gustaria agregar una nueva banda? (si/no): ") == "no":
                return
        
        except sqlite3.IntegrityError:
            ma.deshacer_cambios(conn)
            print("⚠️ No se pudo registrar la banda.")
            print("Verifica que no exista otra con el mismo nombre, país y año.")
            break
        
        except ma.CancelacionUsuario:
            ma.deshacer_cambios(conn)
            print("\n🚫 Operación cancelada. Volviendo al menú...")
            break

def agregar_disco(conn):
    while True:
        try:
            datos = crear_disco(conn)
            
            if datos is None:
                ma.deshacer_cambios(conn)
                print("🚫 Registro de disco abortado.")
                return
    
            validacion = disco_sqlite(conn, datos)
    
            if validacion is False:
                ma.deshacer_cambios(conn)
                return
            else:
                ma.guardar_cambios(conn)
                print("¡Base de datos alimentada con éxito!")
                    
            continuar = ma.si_no("\n¿Deseas agregar otro disco? (si/no): ")
            if continuar == "no":
                break
            
        except sqlite3.IntegrityError:
            ma.deshacer_cambios(conn)
            print("⚠️ No se pudo completar el registro.")
            print("Se encontró un conflicto con alguna restricción de la base de datos.")
            break
        
        except ma.CancelacionUsuario:
            ma.deshacer_cambios(conn)
            print("\n🚫 Operación cancelada. Volviendo al menú...")
            break  
 
def gestionar_banda(conn):
    while True:
        nombre_banda = ma.comprobar_nombre_title("Ingresa el nombre de la banda: ")
        id_banda = ma.seleccionar_id (conn, "ID_Banda", "Bandas", "Nombre_Banda", nombre_banda)
        if id_banda is None:
            if ma.si_no(f"¿Deseas registrar '{nombre_banda}' como una nueva banda? (si/no): ") == "si":
                pais = ma.comprobar_nombre_title("Ingresa el pais de origen de esta banda: ")
                anio = ma.comprobar_num("Ingresa el anio de formacion de esta banda: ")
                id_banda = insertar_banda(conn, nombre_banda, pais, anio)
                print(f"La banda '{nombre_banda}' fue creada con exito")
            else:
                if ma.si_no("Te gustaria intentar buscar otro nombre de banda? (si/no):" ) == "si":
                    continue
                else:
                    return None
        else:
            print(f"Se seleccionó una banda existente con el ID: {id_banda}")
            
        return id_banda

def crear_disco(conn):
        print ("\nNuevo registro")
        
        nombre_disco = ma.comprobar_nombre_title("Ingresa el nombre del nuevo disco: ")
        id_banda = gestionar_banda(conn)
        if id_banda is None:
            return
        
        id_genero = gestion_genero(conn)
        if id_genero is None:
            return
        
        fecha = ma.comprobar_fecha("Ingresa la fecha de lanzamiento del album (DD-MM-YYYY): ")
        ventas = ma.pedir_cifra('''Ingresa la cantidad de ventas que tuvo este album 
(si no tiene puedes dejar el espacio vacio o poner 0): ''')
        streaming = ma.pedir_cifra("Ingresa la cantidad de reproducciones en streaming que tuvo este album: ")
            
        datos = (nombre_disco, id_banda, fecha, ventas, streaming, id_genero)
            
        return datos

def disco_sqlite(conn, datos):
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO Discos(Nombre_disco, ID_Banda, Fecha_Lanzamiento, Ventas_Fisicas, Reproducciones_Streaming, ID_Genero)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', datos)
        print("✅ Disco guardado exitosamente.")
        return True
        
    except sqlite3.IntegrityError:
        print("⚠️ ¡Ey! Ese disco ya está registrado para esa banda. No se hicieron duplicados.")
        return False # Retornamos False para avisar que hubo un choque

def agregar_cancion(conn):
    try:
        while True:
            id_disco = comprobar_disco(conn)
        
            if id_disco is None:
                print("Cancelado")
                return
        
            num = ma.comprobar_num("Ingresa la cantidad de canciones que deseas agregar: ")
            actual = 1
            
            while actual <= num:
                print(f"\n--- Canción {actual} de {num} ---")
                datos = crear_cancion(id_disco)
                
                if cancion_sqlite(conn, datos, id_disco) is not None:
                    ma.guardar_cambios(conn)
                    print("✅ Canción agregada con éxito")
                    actual += 1
                else:
                    ma.deshacer_cambios(conn)
                    if ma.si_no("¿Deseas intentar registrar esta canción de nuevo? (si/no): ") == "no":
                        actual += 1
            
            if ma.si_no("\n¿Te gustaría agregar canciones a algún otro disco? (si/no): ") == "no":
                return
            
    except ma.CancelacionUsuario:
        ma.deshacer_cambios(conn)
        print("\n🚫 Operación cancelada. Volviendo al menú...")
        return
        
def crear_cancion(id_disco):
    nombre_cancion = ma.comprobar_nombre_title("\nIngresa el nombre de la nueva cancion: ")
    duracion = ma.pedir_duracion("Ingresa la duracion de la cancion (formato MM:SS): ")
    datos = (nombre_cancion, id_disco, duracion)
    return datos

def comprobar_disco(conn):
    while True:
        disco = ma.comprobar_nombre_title ("Ingresa el nombre del disco al que pertenece(n) la(s) cancion(nes) que deseas agregar: ")
    
        id_disco = ma.seleccionar_id (conn, "ID_Disco", "Discos", "Nombre_Disco", disco)
    
        if id_disco is not None:
            return id_disco
        else:
            print("No se ha seleccionado ningún disco")
            if ma.si_no("Te gustaria buscar otro disco para agregar canciones? (si/no): ") == "no":
                return None
    
def cancion_sqlite(conn, datos, id_disco):
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO Canciones(Nombre_Cancion, ID_Disco, Duracion)
            VALUES (?, ?, ?)
            ''', datos)
        
    except sqlite3.IntegrityError:
        print("⚠️ Esa canción ya existe en este disco. No se permiten duplicados.")
        return None
    
    id_cancion_nueva = cursor.lastrowid
    cursor.execute('SELECT ID_Genero FROM Discos WHERE ID_Disco = ?', (id_disco,))
    resultado = cursor.fetchone()
    id_genero_del_disco = resultado[0] 
    
    cursor.execute('''
        INSERT INTO Cancion_Genero (ID_Cancion, ID_Genero)
        VALUES (?, ?)
    ''', (id_cancion_nueva, id_genero_del_disco))
    
    return True

def agregar_genero(conn):
    while True:
        try:
            nombre = ma.comprobar_nombre_title("Ingresa el nombre de la cancion a la que deseas agregar otro genero: ")
            id_cancion = ma.seleccionar_id(conn, "ID_Cancion", "Canciones", "Nombre_Cancion", nombre)
    
            if id_cancion is None:
                print ("No se ha seleccionado ninguna cancion")
                if ma.si_no("Te gustaria intentarlo de nuevo? (si/no): ") == "no":
                    return
                else:
                    continue
        
            try: 
                id_genero = gestion_genero(conn)
                if id_genero is None:
                    return
                
                insertar_cancion_genero(conn, id_cancion, id_genero)
                ma.guardar_cambios(conn)
                print ("Genero agregado con exito")
        
            except sqlite3.IntegrityError:
                ma.deshacer_cambios(conn)
                print("⚠️ No se pudo agregar el género. Puede que ya esté asociado a esta canción.")
    
            if ma.si_no("\n¿Deseas agregar un género extra a otra canción? (si/no): ") == "no":
                break
        
        except ma.CancelacionUsuario:
            ma.deshacer_cambios(conn)
            print("\n🚫 Operación cancelada. Volviendo al menú...")
            break
    
def insertar_genero(conn, nombre):
    cursor = conn.cursor()
    
    cursor.execute('''
            INSERT INTO Generos(Nombre_Genero)
            VALUES (?)
            ''', (nombre,))
    
    return cursor.lastrowid

def gestion_genero(conn):
    while True:
        nombre = ma.comprobar_nombre_title("Ingresa el nombre del genero: ")
        id = ma.seleccionar_id(conn, "ID_Genero", "Generos", "Nombre_Genero", nombre)
        
        if id is None:
            if ma.si_no(f"Deseas ingresar ({nombre}) como un nuevo genero? (si/no): ") == "si":
                id = insertar_genero(conn, nombre)
                print ("El nuevo ID ha sido creado")
            else:
                if ma.si_no("Te gustaria intentar buscar otro genero por nombre? (si/no): ") == "si":
                    continue
                else:
                    return None
        else:
            print (f"Se ha seleccionado el genero con el ID: {id}")
        
        return id

def insertar_cancion_genero(conn, id_cancion, id_genero):
    cursor = conn.cursor()
    
    cursor.execute('''
            INSERT INTO Cancion_Genero (ID_Cancion, ID_Genero)
            VALUES (?, ?)
        ''', (id_cancion, id_genero))