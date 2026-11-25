import modulo_apollo_general as ma
import sqlite3

def valor_disco(conn, columna):
    if columna == "fecha_lanzamiento":
        return ma.comprobar_fecha("Ingresa la nueva fecha: ")

    elif columna in ["ventas_fisicas", "reproducciones_streaming"]:
        return ma.pedir_cifra("Ingresa el nuevo valor: ")

    elif columna == "nombre_disco":
        return ma.comprobar_nombre_title("Ingresa el nuevo nombre: ")
    
    elif columna == "id_banda":
        nombre = ma.comprobar_nombre_title("Ingresa el nombre de la nueva banda relacionada: ")
        return ma.seleccionar_id(conn, "ID_Banda", "Bandas", "Nombre_Banda", nombre)
    
    elif columna == "id_genero":
        nombre = ma.comprobar_nombre_title("Ingresa el nombre del nuevo genero relacionado: ")
        return ma.seleccionar_id(conn, "ID_Genero", "Generos", "Nombre_Genero", nombre)

def valor_cancion(conn, columna):
    if columna == "nombre_cancion":
        return ma.comprobar_nombre_title("Ingresa el nuevo nombre: ")
    
    elif columna == "duracion":
        return ma.pedir_duracion("Ingresa el valor de la nueva duracion: ")
    
    elif columna == "id_disco":
        nombre = ma.comprobar_nombre_title("Ingresa el nombre del nuevo disco relacionado: ")
        return ma.seleccionar_id(conn, "ID_Disco", "Discos", "Nombre_Disco", nombre)

def valor_banda(conn, columna, id_actual):
    if columna == "nombre_banda":
        nuevo_nombre = ma.comprobar_nombre_title("Ingresa el nuevo nombre: ")
        coincidencias = ma.obtener_id(conn, "ID_Banda", "Bandas", "Nombre_Banda", nuevo_nombre)
        coincidencias = [coincidencia for coincidencia in (coincidencias or []) if coincidencia[0] != id_actual]
        
        if coincidencias:
            print(f"\n Ya existe al menos una banda registrada con un nombre similar a '{nuevo_nombre}':")
            for coincidencia in coincidencias:
                datos, columnas = ma.buscar_datos(conn, coincidencia[0], "Banda")
                for dato, col in zip(datos, columnas):
                    print(f"  {col}: {dato}")
                print("-" * 25)
                
            if ma.si_no("¿Se trata de la misma banda que ya está registrada? (si/no): ") == "si":
                print("Perfecto, cambio cancelado")
                return None
        
        return nuevo_nombre
    
    elif columna == "pais_origen":
        return ma.comprobar_nombre_title("Ingresa el nombre del nuevo pais: ")
    
    elif columna == "anio_formacion":
        return ma.comprobar_num("Ingresa el nuevo año: ")

def valor_genero(columna):
    if columna == "nombre_genero":
        return ma.comprobar_nombre_title("Ingresa el nuevo nombre: ")
    
def modificar_sqlite(conn, tabla, columna, nuevo_valor, id, valor_id):
    cursor = conn.cursor()
    
    query = f"UPDATE {tabla} SET {columna} = ? WHERE {id} = ?"
    
    cursor.execute(query, (nuevo_valor, valor_id,))
    
    return cursor.rowcount

def actualizar_genero_por_disco(conn, id_cancion, nuevo_id_disco):
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ID_Genero
        FROM Discos
        WHERE ID_Disco = ?
    """, (nuevo_id_disco,))

    genero_disco = cursor.fetchone()

    if genero_disco is None or genero_disco[0] is None:
        raise sqlite3.IntegrityError("El nuevo disco no tiene un genero valido.")

    cursor.execute("""
        DELETE FROM Cancion_Genero
        WHERE ID_Cancion = ?
    """, (id_cancion,))

    cursor.execute("""
        INSERT INTO Cancion_Genero (ID_Cancion, ID_Genero)
        VALUES (?, ?)
    """, (id_cancion, genero_disco[0]))

def actualizar_genero(conn, id_a_buscar, tabla, nombre_sql, id):
    print ("Este género tiene discos asociados. Para eliminarlo deberás seleccionar otro género que los sustituya")
    while True:
        nombre_nuevo = ma.comprobar_nombre_title("Ingresa el nombre del nuevo genero que sera asociado: ")
        nuevo_id = ma.seleccionar_id(conn, id_a_buscar, tabla, nombre_sql, nombre_nuevo)
        if nuevo_id == id:
            print("No puedes seleccionar el genero que deseas eliminar.")
            continue
        
        if nuevo_id is not None:
            actualizar_genero_sql(conn, nuevo_id, id)
            print("Perfecto, genero nuevo asociado")
            return "si"
        else:
            print("Lo siento, no se seleccionó un género válido.")
            if ma.si_no("Te gustaria intentarlo de nuevo? (si/no): ") == "no":
                return "no"

def tiene_discos_asociados(conn, id_genero):
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 1
        FROM Discos
        WHERE ID_Genero = ?
        LIMIT 1
    """, (id_genero,))

    return cursor.fetchone() is not None

def actualizar_genero_sql(conn, id_nuevo, id_antiguo):
    cursor = conn.cursor()
    
    cursor.execute('''
            UPDATE DISCOS
            SET ID_Genero = ?
            WHERE ID_Genero = ?
            ''',(id_nuevo, id_antiguo,))
    
    return cursor.rowcount

def eliminar_sql(conn, tabla, id_a_eliminar, id):
    cursor = conn.cursor()
    
    query = f"DELETE FROM {tabla} WHERE {id_a_eliminar} = ?"
    
    cursor.execute(query, (id,))
    
    return cursor.rowcount