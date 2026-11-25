import modulo_apollo_general as ma
import sqlite3
import modulo_apollo_bme as mm

def buscador(conn, id_a_buscar, tabla, nombre_sql):
    try:
        tipo = nombre_sql.split('_')[1]
        if tipo in ["Banda", "Cancion"]:
            texto = "de la"
        else:
            texto = "del"
        nombre = ma.comprobar_nombre_title(f"Ingresa el nombre {texto} {tipo} que deseas buscar: ")
        id = ma.obtener_id(conn, id_a_buscar, tabla, nombre_sql, nombre)
        if id is not None:
            if len(id) > 1:
                print("Se encontraron varias opciones")
                for i, tupla in enumerate (id, 1):
                    id_disco = tupla[0]
                    datos, columnas = ma.buscar_datos(conn, id_disco, tipo)
                    print(f"\nResultado {i}:")
                                    
                    for dato, columna in zip(datos, columnas):
                        print(f"  {columna}: {dato}")
            else:
                desempaquetado = id[0]
                id_disco = desempaquetado[0]
                datos, columnas = ma.buscar_datos(conn, id_disco, tipo)
                print ("Se encontro el siguiente resultado")
                for dato, columna in zip(datos, columnas):
                    print(f"  {columna}: {dato}")
        else:
            print ("Lo siento, no se encontraron coincidencias con ese nombre")
            return
    except ma.CancelacionUsuario:
        print ("\n🚫 Operación cancelada. Volviendo al menú...")
        return

def mostrar_relacionados(conn, tipo_origen):
    try:
        cursor = conn.cursor()
        
        if tipo_origen == "Banda":
            nombre = ma.comprobar_nombre_title("Ingresa el nombre de la banda: ")
            id_origen = ma.seleccionar_id(conn, "ID_Banda", "Bandas", "Nombre_Banda", nombre)
            query = "SELECT Nombre_Disco FROM Discos WHERE ID_Banda = ?"
            encabezado = "Discos registrados de esta banda:"
            
        elif tipo_origen == "Disco":
            nombre = ma.comprobar_nombre_title("Ingresa el nombre del disco: ")
            id_origen = ma.seleccionar_id(conn, "ID_Disco", "Discos", "Nombre_Disco", nombre)
            query = "SELECT Nombre_Cancion FROM Canciones WHERE ID_Disco = ?"
            encabezado = "Canciones registradas en este disco:"
            
        elif tipo_origen == "Genero":
            nombre = ma.comprobar_nombre_title("Ingresa el nombre del género: ")
            id_origen = ma.seleccionar_id(conn, "ID_Genero", "Generos", "Nombre_Genero", nombre)
            query = "SELECT Nombre_Disco FROM Discos WHERE ID_Genero = ?"
            encabezado = "Discos asociados a este género:"

        if id_origen is not None:
            cursor.execute(query, (id_origen,))
            resultados = cursor.fetchall()
            
            if not resultados:
                print("No hay registros asociados todavía.")
                return
                
            print(f"\n{encabezado}")
            for i, fila in enumerate(resultados, 1):
                print(f"  {i}. {fila[0]}")
                
    except ma.CancelacionUsuario:
        print ("\n🚫 Operación cancelada. Volviendo al menú...")
        return

def modificador(conn, id_a_buscar, tabla, nombre_sql):
    try:
        while True:
            tipo = nombre_sql.split('_')[1]
            if tipo in ["Banda", "Cancion"]:
                texto = "de la"
            else:
                texto = "del"
            nombre = ma.comprobar_nombre_title(f"Ingresa el nombre {texto} {tipo} que deseas modificar: ")
            id = ma.seleccionar_id(conn, id_a_buscar, tabla, nombre_sql, nombre)
            if id is not None:
                cursor = conn.execute(f"PRAGMA table_info({tabla})")
                
                columnas = cursor.fetchall()
                
                columnas_permitidas = {
                    columna[1].lower()
                    for columna in columnas
                    if columna[5] == 0}
                
                while True:
                    print("\nCampos disponibles para modificar:")
                    for columna in columnas:
                        if columna[5] == 0:
                            print(columna[1])
                    
                    columna = ma.comprobar_nombre_lower("Ingresa el campo que deseas modificar: ")
                    if columna not in columnas_permitidas:
                        print("Ese campo no existe o no se puede modificar.")
                        continue
                    
                    if tipo == "Disco":
                        nuevo_valor = mm.valor_disco(conn, columna)

                    elif tipo == "Cancion":
                        nuevo_valor = mm.valor_cancion(conn, columna)

                    elif tipo == "Banda":
                        nuevo_valor = mm.valor_banda(conn, columna, id)

                    elif tipo == "Genero":
                        nuevo_valor = mm.valor_genero(columna)
                    
                    if nuevo_valor is None:
                        print ("No se encontro un registro valido, no se hicieron modificaciones")
                        if ma.si_no("Te gustaria intentarlo de nuevo? (si/no): ") == "no":
                            return
                        else:
                            continue
                    
                    resultado = mm.modificar_sqlite(conn, tabla, columna, nuevo_valor, id_a_buscar, id)
                    
                    if resultado == 0:
                        ma.deshacer_cambios(conn)
                        print ("No se encontro el registro, no se realizaron cambios")
                    else:
                        if tipo == "Cancion" and columna == "id_disco":
                            mm.actualizar_genero_por_disco(conn, id, nuevo_valor)
                        ma.guardar_cambios(conn)
                        print ("Base de datos actualizada con exito!")
                        if ma.si_no(f"Te gustaria realizar algun cambio mas de {tipo}s? (si/no): ") == "si":
                            continue
                        else:
                            return
                        
            else:
                print ("Lo siento no se encontraron coincidencias con ese nombre")
                if ma.si_no("Te gustaria intentarlo de nuevo? (si/no): ") == "si":
                    continue
                else:
                    return
                    
    except sqlite3.IntegrityError as e:
        ma.deshacer_cambios(conn)
        print(f"No se pudo realizar la modificación: {e}")
    
    except sqlite3.OperationalError:
        ma.deshacer_cambios(conn)  
        print ("Lo siento, hubo un error")
        
    except ma.CancelacionUsuario:
        ma.deshacer_cambios(conn)
        print ("\n🚫 Operación cancelada. Volviendo al menú...")
        return

def eliminador(conn, id_a_buscar, tabla, nombre_sql):
    try:
        while True:
            tipo = nombre_sql.split('_')[1]
            if tipo in ["Banda", "Cancion"]:
                texto = "de la"
            else:
                texto = "del"
            nombre = ma.comprobar_nombre_title(f"Ingresa el nombre {texto} {tipo} que deseas eliminar: ")
            id = ma.seleccionar_id(conn, id_a_buscar, tabla, nombre_sql, nombre)
            if id is not None:
                
                cursor = conn.cursor()

                query = f"SELECT {nombre_sql} FROM {tabla} WHERE {id_a_buscar} = ?"

                cursor.execute(query, (id,))

                nombre_real = cursor.fetchone()[0]
                
                if tipo == "Disco":
                    print ("Al realizar esta accion, canciones pueden quedar sin un disco asociado")
                    pregunta = ma.si_no(f"Estas seguro de querer eliminar el disco {nombre_real} (si/no): ")
                
                elif tipo == "Banda":
                    print ("Al realizar esta accion, discos pueden quedar sin una banda asociada")
                    pregunta = ma.si_no(f"Estas seguro de querer eliminar la banda {nombre_real} (si/no): ")
                
                elif tipo == "Cancion":
                    pregunta = ma.si_no(f"Estas seguro de querer eliminar la cancion {nombre_real} (si/no): ")
                
                elif tipo == "Genero":
                    print("Al eliminar este genero, sus asociaciones con canciones desapareceran.")
                    if mm.tiene_discos_asociados(conn, id):
                        confirmacion = mm.actualizar_genero(conn, id_a_buscar, tabla, nombre_sql, id)
                        if confirmacion == "no":
                            print ("Operacion cancelada")
                            ma.deshacer_cambios(conn)
                            return
                        
                    pregunta = ma.si_no(f"Estas seguro de querer eliminar el genero {nombre_real} (si/no): ")
                
                if pregunta == "si":
                    pregunta2 = ma.si_no("Por favor, confirma una vez mas la eliminacion (si/no): ")
                    if pregunta2 == "si":
                        resultado = mm.eliminar_sql(conn, tabla, id_a_buscar, id)
                        if resultado == 0:
                            print ("Operacion cancelada, no se realizaron cambios")
                            ma.deshacer_cambios(conn)
                        else:
                            ma.guardar_cambios(conn)
                            print ("Eliminacion realizada con exito, base de datos actualizada")
                    else:
                        ma.deshacer_cambios(conn)
                        print ("Operacion cancelada")
                else:
                    ma.deshacer_cambios(conn)
                    print ("Operacion cancelada:")
                
                if ma.si_no(f"Te gustaria realizar una eliminacion mas de {tipo}s? (si/no): ") == "si":
                    continue
                else:
                    break

                                
            else:
                print ("Lo siento no se encontraron coincidencias con ese nombre")
                if ma.si_no("Te gustaria intentarlo de nuevo? (si/no): ") == "si":
                    continue
                else:
                    return            
    
    except sqlite3.OperationalError:
        ma.deshacer_cambios(conn)  
        print ("Lo siento, hubo un error")
    
    except sqlite3.IntegrityError as e:
        ma.deshacer_cambios(conn)
        print(f"No se pudo realizar la modificación: {e}")
    
    except ma.CancelacionUsuario:
        ma.deshacer_cambios(conn)
        print ("\n🚫 Operación cancelada. Volviendo al menú...")
        return