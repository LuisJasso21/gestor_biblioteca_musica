import modulo_apollo_general as ma

def extremo_disco_cifras (conn, extremo, categoria):
    cursor = conn.cursor()
    if extremo == "maximo":
        ext = "MAX"
        texto = "mas"
    
    else:
        ext = "MIN"
        texto = "menos"
    
    if categoria == "ventas":
        columna = "Ventas_Fisicas"
        unidad = "ventas fisicas"
    
    else:
        columna = "Reproducciones_Streaming"
        unidad = "reproducciones en streaming"
                
    query = f'''
            SELECT
                Discos.Nombre_Disco,
                Bandas.Nombre_Banda,
                Discos.{columna}
            FROM Discos
            LEFT JOIN Bandas
            ON Discos.ID_Banda = Bandas.ID_Banda
            
            WHERE Discos.{columna} = (SELECT {ext}({columna})
            FROM Discos)
            '''
    
    cursor.execute(query)
    resultado = cursor.fetchall()
    
    if not resultado:
        print(f"No hay datos registrados para consultar.")
        return
    
    print(f"\nDiscos con {texto} {unidad}:")

    for disco, banda, cantidad in resultado:
        print(f"{disco} - {banda}: {ma.imprimir_cifras(cantidad)} de {unidad}")

def sumar_cifras_banda(conn, categoria):
    if categoria == "ventas":
        columna = "Ventas_Fisicas"
        unidad = "ventas fisicas"
    
    else:
        columna = "Reproducciones_Streaming"
        unidad = "reproducciones en streaming"
    
    nombre = ma.comprobar_nombre_title("Ingresa el nombre de la banda: ")
    id = ma.seleccionar_id(conn, "ID_Banda", "Bandas", "Nombre_Banda", nombre)
    if id is not None:
        cursor = conn.cursor()
        
        query = f'''
            SELECT Bandas.Nombre_Banda, 
            SUM(Discos.{columna})
            FROM Discos
            JOIN Bandas 
            ON Discos.ID_Banda = Bandas.ID_Banda
            WHERE Bandas.ID_Banda = ?;
            '''
        
        cursor.execute(query, (id,))
        resultado = cursor.fetchone()
        
        if resultado[1] is None:
            print("Esta banda no tiene cifras registradas para consultar.")
            return
        
        print (f"El total de {unidad} de la banda {resultado[0]} es de {ma.imprimir_cifras(resultado[1])}")
        
def ranking(conn, categoria):
    if categoria == "ventas":
        columna = "Ventas_Fisicas"
        unidad = "ventas fisicas"
    
    else:
        columna = "Reproducciones_Streaming"
        unidad = "reproducciones en streaming"
    
    cursor = conn.cursor()
    
    cursor.execute(f'''
            SELECT Bandas.Nombre_Banda, 
            SUM(Discos.{columna})
            FROM Discos
            JOIN Bandas
            ON Discos.ID_Banda = Bandas.ID_Banda
            GROUP BY Bandas.ID_Banda
            ORDER BY SUM(Discos.{columna}) DESC
            LIMIT 5
            ''')
    
    resultado = cursor.fetchall()
    
    print("")
    for i, (banda, total) in enumerate (resultado, 1):
        print (f"#{i} {banda} - {unidad}: {ma.imprimir_cifras(total)}")

def duracion_disco(conn):
    nombre = ma.comprobar_nombre_title("Ingresa el nombre del disco: ")
    id = ma.seleccionar_id(conn, "ID_Disco", "Discos", "Nombre_Disco", nombre)
    if id is not None:
        cursor = conn.cursor()
        
        query = f'''
        SELECT Discos.Nombre_Disco, SUM(Canciones.Duracion), COUNT(Canciones.ID_Cancion)
        FROM Canciones
        JOIN Discos
        ON Discos.ID_Disco = Canciones.ID_Disco
        WHERE Discos.ID_Disco = ?'''
        
        cursor.execute(query, (id,))
        resultado = cursor.fetchone()
        
        if resultado[1] is None:
            print ("Lo siento, ese disco no tiene canciones agregadas.")
            return
        
        minutos, segundos = divmod(resultado[1], 60)
        
        print (f"La duracion total del disco {resultado[0]} ({resultado[2]} canciones) es: {minutos} minutos con {segundos:02d} segundos")

def promedio_cifras(conn, categoria):
    if categoria == "ventas":
        columna = "Ventas_Fisicas"
        unidad = "ventas fisicas"
        texto = "ventas"
    
    else:
        columna = "Reproducciones_Streaming"
        unidad = "reproducciones en streaming"
        texto = "streaming"
    
    cursor = conn.cursor()
    
    query = f'''
        SELECT Bandas.Nombre_Banda, 
        CAST(ROUND(AVG(Discos.{columna})) AS INTEGER) AS Promedio,
        COUNT (Discos.ID_disco)
        FROM Discos
        JOIN Bandas
        ON Bandas.ID_Banda = Discos.ID_Banda
        GROUP BY Bandas.ID_Banda
        ORDER BY Promedio DESC
        LIMIT 3
        '''
    
    cursor.execute(query)
    
    resultado = cursor.fetchall()

    if not resultado:
        print("No hay datos suficientes para calcular el promedio.")
        return
    
    print (f"\nLas bandas con mejor promedio en {unidad} son:")
    for i, (nombre, promedio, total_discos) in enumerate(resultado, 1):
        print (f"#{i} {nombre} ({total_discos} discos) con un promedio en {texto} de {ma.imprimir_cifras(promedio)}")