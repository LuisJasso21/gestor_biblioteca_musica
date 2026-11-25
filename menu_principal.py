import os
import sqlite3
import modulo_apollo_general as ma
import sub_menus as sm

def menu_principal(conn):
        print ("---TE DAMOS LA BIENVENIDA A NUESTRA BASE DE DATOS---")
    
        while True:
            try: 
                print ("\n-----MENU PRINCIPAL-----")
                print ("1. Menu de agregacion")
                print ("2. Buscador")
                print ("3. Explorar catalogo")
                print ("4. Modificar registro")
                print ("5. Eliminar registro")
                print ("6. Menu de Estadisticas")
                print ("7. Salir")
        
                respuesta = ma.comprobar_nombre_lower("Selecciona una opcion (escribe la accion o el numero): ")
                respuesta_formateada = obtener_accion_menu(respuesta)
        
                if respuesta_formateada == "agregacion":
                    sm.menu_agregacion(conn)
                       
                elif respuesta_formateada == "buscar":
                    sm.menu_buscar(conn)
                
                elif respuesta_formateada == "catalogo":
                    sm.menu_relaciones(conn)
                
                elif respuesta_formateada == "modificar":
                    sm.menu_modificacion(conn)
                
                elif respuesta_formateada == "eliminar":
                    sm.menu_eliminar(conn)
                    
                elif respuesta_formateada == "estadisticas":
                    sm.menu_estadisticas(conn)
        
                elif respuesta_formateada == "salir":
                    print ("¡Hasta luego!")
                    break
        
                else:
                    print("\n❌ Opción no válida. Por favor, elige una opción del menú.")
                    continue
        
                continuar = ma.si_no("\n¿Quieres realizar otra consulta del menu principal? (si/no): ")
                if continuar == "no":
                    print ("¡Hasta luego!")
                    break
            
            except ma.CancelacionUsuario:
                    print("\n🚫 Operación cancelada. ¡Hasta luego!")
                    break

def obtener_accion_menu(entrada):
    
    mapeo = {
        "agregacion": ["1", "agregacion", "agregar", "menu de agregacion"],
        "buscar": ["2", "buscar", "buscador"],
        "catalogo": ["3", "relaciones", "mostrar relaciones", "catalogo", "explorar catalogo"],
        "modificar": ["4", "modificar", "modificador", "registro", "registros", "modificacion"],
        "eliminar": ["5", "eliminar", "borrar"],
        "estadisticas": ["6", "menu de estadisticas", "estadisticas", "estadistica"],
        "salir": ["7", "salir", "volver", "exit", "cancelar", "afuera"]
    }
    
    for accion, palabras_clave in mapeo.items():
        if any(palabra == entrada for palabra in palabras_clave):
            return accion
        
    return None

def inicializar_bd(conn):
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Generos (
            ID_Genero INTEGER PRIMARY KEY AUTOINCREMENT,
            Nombre_Genero TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Bandas (
            ID_Banda INTEGER PRIMARY KEY AUTOINCREMENT,
            Nombre_Banda TEXT,
            Pais_Origen TEXT,
            Anio_Formacion INTEGER
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Discos (
            ID_Disco INTEGER PRIMARY KEY AUTOINCREMENT,
            Nombre_Disco TEXT,
            ID_Banda INTEGER,
            Fecha_Lanzamiento TEXT,
            Ventas_Fisicas INTEGER,
            Reproducciones_Streaming INTEGER,
            ID_Genero INTEGER,
            FOREIGN KEY (ID_Banda) REFERENCES Bandas(ID_Banda) ON DELETE SET NULL,
            FOREIGN KEY (ID_Genero) REFERENCES Generos(ID_Genero) ON DELETE NO ACTION
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Canciones (
            ID_Cancion INTEGER PRIMARY KEY AUTOINCREMENT,
            Nombre_Cancion TEXT,
            ID_Disco INTEGER,
            Duracion INTEGER,
            UNIQUE (Nombre_Cancion, ID_Disco),
            FOREIGN KEY (ID_Disco) REFERENCES Discos(ID_Disco) ON DELETE SET NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Cancion_Genero (
            ID_Genero INTEGER NOT NULL,
            ID_Cancion INTEGER NOT NULL,
            PRIMARY KEY (ID_Genero, ID_Cancion),
            FOREIGN KEY (ID_Genero) REFERENCES Generos(ID_Genero) ON DELETE CASCADE,
            FOREIGN KEY (ID_Cancion) REFERENCES Canciones(ID_Cancion) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()

if __name__ == "__main__":
    try:
        carpeta_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_bd = os.path.join(carpeta_actual, "discos.db")

        with sqlite3.connect(ruta_bd) as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            inicializar_bd(conn)
            
            conn.create_function("NORMALIZAR", 1, ma.normalizar)
        
            # Arrancamos el menú entregándole la llave de la base de datos
            menu_principal(conn)
    except sqlite3.OperationalError as e:
        print(f"Hubo un error operativo en la base de datos: {e}")
        print("Saliendo... ")
        
    finally:
        # El bloque finally se ejecuta SIEMPRE, haya habido error o no.
        # Esto garantiza que la base de datos quede cerrada al salir del programa.
        if 'conn' in locals():
            conn.close()

