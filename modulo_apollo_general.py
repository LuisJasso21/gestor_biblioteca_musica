from datetime import datetime
import unicodedata

class CancelacionUsuario(Exception):
    pass

# 2. Tu nueva función base para pedir datos
def input_cancelable(mensaje):
    respuesta = input(mensaje).strip()
    
    # Si el usuario quiere huir, disparamos la alarma
    if respuesta.lower() in ["cancelar", "salir", "abortar"]:
        raise CancelacionUsuario()
        
    return respuesta

def seleccionar_opcion(lista):
    if len(lista) == 1:
        return lista[0]

    while True:
        print (f"\nSelecciona una opcion (1-{len(lista)})")
        num = comprobar_num("Tambien puedes poner '0' si no se encuentra la opcion que deseas: ")
        if 1 <= num <= len(lista):
            return lista[num-1]
        elif num == 0:
            return None
        print("❌ Número fuera de rango, inténtalo de nuevo.")

def si_no(pregunta):
    while True:
        respuesta = input_cancelable(pregunta).lower().strip()
        respuesta_normalizada = normalizar(respuesta)

        if respuesta_normalizada in ("si", "no"):
            return respuesta_normalizada

        print("Por favor responde únicamente 'si' o 'no'")

def comprobar_num(mensaje):
    while True:
        numero = input_cancelable(mensaje).strip()
        if numero.isdecimal():
            return int(numero)
        else: 
            print("Por favor, utiliza solo numeros enteros positivos")

def comprobar_nombre_lower(mensaje):
    while True: 
        texto = input_cancelable(mensaje).lower().strip()
        if texto:
            return texto
        else:
            print ("El espacio no puede estar vacio, por favor, intentalo de nuevo")

def comprobar_nombre_title(mensaje):
    while True: 
        texto = input_cancelable(mensaje).title().strip()
        if texto:
            return texto
        else:
            print ("El espacio no puede estar vacio, por favor, intentalo de nuevo")

def imprimir_cifras(ventas):
    if ventas >= 1000000000:
        resultado = ventas / 1000000000
        return f"{resultado:.2f} mil millones"
    elif ventas >= 1000000:
        resultado = ventas / 1000000
        return f"{resultado:.2f} millones"
    elif ventas >= 1000:
        resultado = ventas / 1000
        return f"{resultado:.2f} mil"
    return ventas

def obtener_multiplicador_y_limpiar(entrada):
    mapeo = {
        1_000_000_000: ["mil millones", "miles de millones"],
        1_000_000: ["millones", "millón", "millon"],
        1_000: ["miles", "mil"]
    }
    
    for multiplicador, palabras_clave in mapeo.items():
        for palabra in palabras_clave:
            if palabra in entrada:
                # Si encuentra la palabra, la borra del texto original
                texto_limpio = entrada.replace(palabra, "").strip()
                return texto_limpio, multiplicador
                
    # Si no encontró ninguna palabra, devuelve el texto intacto y multiplicador de 1
    return entrada, 1

def pedir_cifra(mensaje):
    while True:
        entrada = input_cancelable(mensaje).strip().lower()
        
        if entrada == "":
            return 0
            
        # Extraemos el texto sin la palabra (ej. "20.5") y el número a multiplicar
        texto_limpio, multiplicador = obtener_multiplicador_y_limpiar(entrada)

        try:
            numero_final = float(texto_limpio) * multiplicador
            return int(numero_final) 
            
        except ValueError:
            print("❌ Formato no reconocido. Intenta con '20 millones', '1.5 mil' o '2000000'.")

def pedir_duracion(mensaje):
    while True:
        entrada = input_cancelable(mensaje).strip()
        
        if entrada == "":
            return 0
            
        try:
            # Separamos el texto usando los dos puntos ':'
            partes = entrada.split(':')
            
            if len(partes) == 2:
                minutos = int(partes[0])
                segundos = int(partes[1])
                
                # Verificamos que los segundos no sean una locura como "3:99"
                if segundos > 59:
                    print("❌ Los segundos no pueden ser mayores a 59.")
                    continue
                    
                total_segundos = (minutos * 60) + segundos
                return total_segundos
            else:
                print("❌ Usa el formato MM:SS. Por ejemplo: 3:45 o 04:20")
                
        except ValueError:
            print("❌ Formato inválido. Asegúrate de usar números y dos puntos (:).")


def guardar_cambios(conn):
    conn.commit()

def deshacer_cambios(conn):
    conn.rollback()

def normalizar(texto):
    texto = unicodedata.normalize("NFD", texto)

    texto = "".join(
        caracter for caracter in texto
        if not unicodedata.combining(caracter)
    )

    return texto.casefold()

def formatear_datos(datos, tipo):
    if tipo == "Disco":
        fecha = datetime.strptime(datos[-3], "%Y-%m-%d").strftime("%d-%m-%Y")
        ventas = f"{datos[-2]:,}"
        reproducciones = f"{datos[-1]:,}"

        datos = (*datos[:-3], fecha, ventas, reproducciones)
        
    elif tipo == "Cancion":
        duracion = datos[-1]
        minutos, segundos = divmod(duracion, 60)
        duracion_formateada = f"{minutos}:{segundos:02d}"
        datos = (*datos[:-1], duracion_formateada)
    
    return datos

def buscar_datos(conn, id, tipo):
    cursor = conn.cursor()
    
    if tipo == "Disco":
        cursor.execute('''
            SELECT 
                Discos.Nombre_Disco AS Nombre,
                Bandas.Nombre_Banda AS Banda,
                Bandas.Pais_Origen AS "Pais de Origen",
                Bandas.Anio_Formacion AS "Año de Formacion",
                Discos.Fecha_Lanzamiento AS Lanzamiento,
                Discos.Ventas_Fisicas AS Ventas,
                Discos.Reproducciones_Streaming AS Reproducciones
            
            FROM Discos
            LEFT JOIN Bandas ON Bandas.ID_Banda = Discos.ID_Banda
            WHERE ID_Disco = ?
            ''',(id,))
    
    elif tipo == "Banda":
        cursor.execute('''
            SELECT 
                Bandas.Nombre_Banda AS Banda,
                Bandas.Pais_Origen AS "Pais de origen",
                Bandas.Anio_Formacion AS "Año de formacion",
                Bandas.ID_Banda AS ID
            FROM Bandas
            WHERE ID_Banda = ?
            ''',(id,))
    
    elif tipo == "Genero":
        cursor.execute('''
            SELECT 
                Generos.Nombre_Genero AS Genero,
                Generos.ID_Genero AS ID
            FROM Generos
            WHERE ID_Genero = ?
            ''',(id,))
    
    elif tipo == "Cancion":
        cursor.execute('''
            SELECT
                Canciones.Nombre_Cancion AS Cancion,
                Discos.Nombre_Disco AS Disco,
                Bandas.Nombre_Banda AS Banda,
                Bandas.Pais_Origen AS "Pais de Origen",
                Bandas.Anio_Formacion AS "Año de Formacion",
                Canciones.ID_Cancion AS ID,
                Canciones.Duracion AS Duracion
            
            FROM Canciones
            LEFT JOIN Discos ON Discos.ID_Disco = Canciones.ID_Disco
            LEFT JOIN Bandas ON Discos.ID_Banda = Bandas.ID_Banda
            WHERE ID_Cancion = ?
            ''',(id,))
    
    datos = cursor.fetchone()
    columnas = [columna[0] for columna in cursor.description]
    
    if datos is None:
        return None

    datos = formatear_datos(datos, tipo)
    
    resultado = (datos, columnas)

    return resultado

def seleccionar_id(conn, id_a_buscar, tabla, nombre_buscar, nombre):
    ids = obtener_id(conn, id_a_buscar, tabla, nombre_buscar, nombre)
    tipo = nombre_buscar.split('_')[1]
    if ids is not None:
        if len(ids) > 1:
            print("Se encontraron varias opciones")
            for i, tupla in enumerate (ids, 1):
                id_disco = tupla[0]
                datos, columnas = buscar_datos(conn, id_disco, tipo)
                
                print(f"\nOpción {i}:")
                
                for dato, columna in zip(datos, columnas):
                    print(f"  {columna}: {dato}")
                
            opcion = seleccionar_opcion(ids)
            if opcion is None:
                return None
            return opcion[0]
        else:
            desempaquetado = ids[0]
            id = desempaquetado[0]
            print ("Se encontro el siguiente resultado:")
            datos, columnas = buscar_datos(conn, id, tipo)
            for dato, columna in zip(datos, columnas):
                print (f"{columna}: {dato}")
            if si_no("Es este el resultado que deseabas? (si/no): ") == "si":
                return id
            else:
                return None
    else:
        return None

def obtener_id(conn, id_a_buscar, tabla, nombre_buscar, nombre):
    cursor = conn.cursor()
    
    query = f"SELECT {id_a_buscar} FROM {tabla} WHERE NORMALIZAR ({nombre_buscar}) LIKE ?"
    
    cursor.execute(query, (f"%{normalizar(nombre)}%",))
    resultado = cursor.fetchall()
    
    if resultado:
        return resultado
    else:
        return None

def validar_fecha_sqlite(fecha_texto):
    try:
        # Intenta leerla. Si el usuario pone "30-02-2023", esto fallará automáticamente.
        #strptime(): interpreta una cadena de texto y la convierte en un objeto de fecha.
        fecha_obj = datetime.strptime(fecha_texto, "%d-%m-%Y")
        
        if fecha_obj > datetime.now():
            return None
            
        # Si pasó la prueba, la formateamos como le gusta a SQLite
        #strftime(): convierte ese objeto de fecha nuevamente en texto, con el formato que elijas.
        fecha_sqlite = fecha_obj.strftime("%Y-%m-%d")
        return fecha_sqlite
        
    except ValueError:
        return None
    
def comprobar_fecha(mensaje):
    while True:
        texto = input_cancelable(mensaje).strip()
        fecha = validar_fecha_sqlite(texto)
        if fecha is not None:
            return fecha
        else:
            print("Error: Fecha inválida. Asegúrate de usar el formato DD-MM-YYYY, que sea una fecha real y que no este en el futuro")
            continue