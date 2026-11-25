import modulo_apollo_general as ma
import funciones_agregacion as f
import funciones_mostrar_modificar as fm
import funciones_estadisticas as fe


def obtener_accion_sub_menus(entrada):
    mapeo = {
        
        "disco": ["1", "disco", "agregar disco", "discos"],
        "banda": ["2", "banda", "agregar banda", "bandas"],
        "genero": ["3", "genero", "agregar genero", "generos"],
        "cancion": ["4", "cancion", "agregar canciones", "canciones"],
        "salir": ["5", "salir", "volver", "exit", "afuera", "cancelar"]
    }
    
    for accion, palabras_clave in mapeo.items():
        if entrada in palabras_clave:
            return accion
        
    return None

def menu_agregacion(conn):
    try:
        while True:
            print ("\n---MENU DE AGREGACION---")
            print ("1. Agregar Disco")
            print ("2. Agregar Banda")
            print ("3. Agregar Genero a canciones")
            print ("4. Agregar Canciones")
            print ("5. Salir")
            
            opcion = ma.comprobar_nombre_lower("\nSelecciona una opcion por favor (Numero o nombre): ")
            opcion_formateada = obtener_accion_sub_menus(opcion)
            
            if opcion_formateada == "banda":
                f.agregar_banda(conn)
            
            elif opcion_formateada == "disco":
                f.agregar_disco(conn)
            
            elif opcion_formateada == "cancion":
                f.agregar_cancion(conn)
            
            elif opcion_formateada == "genero":
                f.agregar_genero(conn)
            
            elif opcion_formateada == "salir":
                break
            
            else:
                print("❌ Opción no válida. Por favor, elige una opción del menú.")
                continue
            
            if ma.si_no("\nTe gustaria agregar algun otro campo? (si/no): ") == "no":
                return
                
    except ma.CancelacionUsuario:
        print ("\n🚫 Operación cancelada. Volviendo al menú principal...")
        return   

def menu_buscar(conn):
    try:
        while True:
            print ("\n---MENU DE BUSQUEDA---")
            print ("1. Disco")
            print ("2. Banda")
            print ("3. Genero")
            print ("4. Cancion")
            print ("5. Salir")
            
            respuesta = ma.comprobar_nombre_lower("Seleccione la opcion que desea buscar (Nombre o Numero): ")
            respuesta_formateada = obtener_accion_sub_menus(respuesta)
            
            if respuesta_formateada == "disco":
                mostrar_sugerencias(conn, "Nombre_Disco", "Discos")
                while True:
                    fm.buscador(conn, "ID_Disco", "Discos", "Nombre_Disco")
                    if ma.si_no("\nTe gustaria buscar otro disco? (si/no): ") == "no":
                        break
            
            elif respuesta_formateada == "banda":
                mostrar_sugerencias(conn, "Nombre_Banda", "Bandas")
                while True:
                    fm.buscador(conn, "ID_Banda", "Bandas", "Nombre_Banda")
                    if ma.si_no("\nTe gustaria buscar otra banda? (si/no): ") == "no":
                        break
            
            elif respuesta_formateada == "genero":
                mostrar_sugerencias(conn, "Nombre_Genero", "Generos")
                while True:
                    fm.buscador(conn, "ID_Genero", "Generos", "Nombre_Genero")
                    if ma.si_no("\nTe gustaria buscar otro genero? (si/no): ") == "no":
                        break
            
            elif respuesta_formateada == "cancion":
                mostrar_sugerencias(conn, "Nombre_Cancion", "Canciones")
                while True:
                    fm.buscador(conn, "ID_Cancion", "Canciones", "Nombre_Cancion")
                    if ma.si_no("\nTe gustaria buscar otra cancion? (si/no): ") == "no":
                        break
            
            elif respuesta_formateada == "salir":
                return
            
            else:
                print ("Lo siento, esa opcion no esta disponible, intentalo de nuevo")
                continue
            
            if ma.si_no("\nTe gustaria realizar otra busqueda? (si/no): ") == "no":
                return
            
    except ma.CancelacionUsuario:
        print("\n🚫 Operación cancelada. Volviendo al menú principal...")
        return

def mostrar_sugerencias(conn, nombre_sql, tabla):
    cursor = conn.cursor()
    cursor.execute(f"SELECT {nombre_sql} FROM {tabla} ORDER BY RANDOM() LIMIT 10")
    muestra = [fila[0] for fila in cursor.fetchall()]
    
    if muestra:
        print(f"💡 Pista - Algunos registros disponibles: {', '.join(muestra)}")

def menu_relaciones(conn):
    print("\nExplora el contenido de tu biblioteca según lo que quieras consultar:")
    try:
        while True:
            print("\n--- EXPLORAR CATÁLOGO ---")
            print("1. Ver canciones de un disco")
            print("2. Ver discos de una banda")
            print("3. Ver discos de un género")
            print("4. Volver al menú")
            
            respuesta = ma.comprobar_nombre_lower("Selecciona una opción (número o palabra clave): ")
            accion = obtener_accion_relaciones(respuesta)
            
            if accion == "disco":
                fm.mostrar_relacionados(conn, "Disco")
            
            elif accion == "banda":
                fm.mostrar_relacionados(conn, "Banda")
            
            elif accion == "genero":
                fm.mostrar_relacionados(conn, "Genero")
            
            elif accion == "salir":
                return
            
            else:
                print("⚠️ Opción no válida, inténtalo de nuevo.")
                continue
            
            if ma.si_no("\n¿Te gustaría consultar otro listado? (si/no): ") == "no":
                return
            
    except ma.CancelacionUsuario:
        print("\n🚫 Operación cancelada. Volviendo al menú principal...")
        return

def obtener_accion_relaciones(entrada):
    mapeo = {
        "disco": ["1", "disco", "discos", "canciones", "cancion"],
        "banda": ["2", "banda", "bandas", "discografia"],
        "genero": ["3", "genero", "generos"],
        "salir": ["4", "salir", "volver", "exit", "afuera", "cancelar"]
    }
    
    for accion, palabras_clave in mapeo.items():
        if entrada in palabras_clave:
            return accion
        
    return None

def menu_modificacion(conn):
    try:
        while True:
            print ("\n---MENU DE MODIFICACION---")
            print ("1. Disco")
            print ("2. Banda")
            print ("3. Genero")
            print ("4. Cancion")
            print ("5. Salir")
            
            respuesta = ma.comprobar_nombre_lower("Seleccione la opcion que desea para modificar (Nombre o Numero): ")
            respuesta_formateada = obtener_accion_sub_menus(respuesta)
            
            if respuesta_formateada == "disco":
                while True:
                    fm.modificador(conn, "ID_Disco", "Discos", "Nombre_Disco")
                    if ma.si_no("\nTe gustaria modificar otro disco? (si/no): ") == "no":
                        break
            
            elif respuesta_formateada == "banda":
                while True:
                    fm.modificador(conn, "ID_Banda", "Bandas", "Nombre_Banda")
                    if ma.si_no("\nTe gustaria modificar otra banda? (si/no): ") == "no":
                        break
            
            elif respuesta_formateada == "genero":
                while True:
                    fm.modificador(conn, "ID_Genero", "Generos", "Nombre_Genero")
                    if ma.si_no("\nTe gustaria modificar otro genero? (si/no): ") == "no":
                        break
            
            elif respuesta_formateada == "cancion":
                while True:
                    fm.modificador(conn, "ID_Cancion", "Canciones", "Nombre_Cancion")
                    if ma.si_no("\nTe gustaria modificar otra cancion? (si/no): ") == "no":
                        break
            
            elif respuesta_formateada == "salir":
                return
            
            else:
                print ("Lo siento, esa opcion no esta disponible, intentalo de nuevo")
                continue
            
            if ma.si_no("\nTe gustaria realizar otra modificacion? (si/no): ") == "no":
                return
            
    except ma.CancelacionUsuario:
        print("\n🚫 Operación cancelada. Volviendo al menú principal...")
        return

def menu_eliminar(conn):
    try:
        while True:
            print ("\n---MENU DE ELIMINACION---")
            print ("1. Eliminar disco")
            print ("2. Eliminar banda")
            print ("3. Eliminar genero")
            print ("4. Eliminar cancion")
            print ("5. Salir")
            
            respuesta = ma.comprobar_nombre_lower("Seleccione la opcion que desea para eliminar (Nombre o Numero): ")
            respuesta_formateada = obtener_accion_sub_menus(respuesta)
            
            if respuesta_formateada == "disco":
                while True:
                    fm.eliminador(conn, "ID_Disco", "Discos", "Nombre_Disco")
                    if ma.si_no("\nTe gustaria eliminar otro disco? (si/no): ") == "no":
                        break
            
            elif respuesta_formateada == "banda":
                while True:
                    fm.eliminador(conn, "ID_Banda", "Bandas", "Nombre_Banda")
                    if ma.si_no("\nTe gustaria eliminar otra banda? (si/no): ") == "no":
                        break
            
            elif respuesta_formateada == "genero":
                while True:
                    fm.eliminador(conn, "ID_Genero", "Generos", "Nombre_Genero")
                    if ma.si_no("\nTe gustaria eliminar otro genero? (si/no): ") == "no":
                        break
            
            elif respuesta_formateada == "cancion":
                while True:
                    fm.eliminador(conn, "ID_Cancion", "Canciones", "Nombre_Cancion")
                    if ma.si_no("\nTe gustaria eliminar otra cancion? (si/no): ") == "no":
                        break
            
            elif respuesta_formateada == "salir":
                return
            
            else:
                print ("Lo siento, esa opcion no esta disponible, intentalo de nuevo")
                continue
            
            if ma.si_no("\nTe gustaria realizar otra eliminacion? (si/no): ") == "no":
                return
            
    except ma.CancelacionUsuario:
        print("\n🚫 Operación cancelada. Volviendo al menú principal...")
        return

def menu_estadisticas(conn):
    try:
        while True:
            print ("\n----MENU DE ESTADISTICAS---")
            print ("1. Maximos y minimos de ventas y streaming")
            print ("2. Sumar cifras totales de una banda")
            print ("3. Ranking de bandas")
            print ("4. Saber duracion total de un disco: ")
            print ("5. Ver las bandas con mejores promedios")
            print ("6. Salir")
            
            respuesta = ma.comprobar_nombre_lower("Seleccione la opcion que desea (nombre o numero): ")
            respuesta_formateada = obtener_accion_estadisticas(respuesta)
            
            if respuesta_formateada == "extremos":
                fe.extremo_disco_cifras(conn, "maximo", "ventas")
                fe.extremo_disco_cifras(conn, "minimo", "ventas")
                fe.extremo_disco_cifras(conn, "maximo", "streaming")
                fe.extremo_disco_cifras(conn, "minimo", "streaming")
            
            elif respuesta_formateada == "suma":
                submenu_sumar(conn)
            
            elif respuesta_formateada == "ranking":
                fe.ranking(conn, "ventas")
                fe.ranking(conn, "reproducciones")
            
            elif respuesta_formateada == "duracion":
                fe.duracion_disco(conn)
            
            elif respuesta_formateada == "promedio":
                fe.promedio_cifras(conn, "ventas")
                fe.promedio_cifras(conn, "streaming")
            
            elif respuesta_formateada == "salir":
                return
            
            else:
                print ("Lo siento, esa opcion no esta disponible, intentalo de nuevo")
                continue
            
            if ma.si_no("\nTe gustaria realizar otra consulta del menu de estadisticas? (si/no): ") == "no":
                return
            
    except ma.CancelacionUsuario:
        print("\n🚫 Operación cancelada. Volviendo al menú principal...")
        return

def obtener_accion_estadisticas(entrada):
    mapeo = {
        "extremos": ["1", "mostrar extremos", "extremos"],
        "suma": ["2", "ventas", "sumar", "reproducciones", "streaming"],
        "ranking": ["3", "ranking", "ranking de bandas"],
        "duracion": ["4", "duracion", "saber duracion", "duracion total"],
        "promedio": ["5", "promedio", "promedios", "mejores promedios"],
        "salir": ["6", "salir", "exit", "afuera", "cancelar"]
    }
    
    for accion, palabras_clave in mapeo.items():
        if any(palabra == entrada for palabra in palabras_clave):
            return accion
        
    return None

def submenu_sumar(conn):
    while True:
        print ("\n1. Ventas fisicas")
        print ("2. Reproducciones en Streaming")
        opcion = ma.comprobar_num("Selecciona la opcion que te gustaria sumar (1 o 2): ")
        
        if opcion == 1:
            fe.sumar_cifras_banda(conn, "ventas")
        elif opcion == 2:
            fe.sumar_cifras_banda(conn, "reproducciones")
        else:
            print ("Lo siento opcion no valida, intentalo de nuevo")
            continue
        
        if ma.si_no("Te gustaria sumar las cifras de alguna otra banda? (si/no): ") == "no":
            return