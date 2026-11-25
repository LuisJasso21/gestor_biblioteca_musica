# Gestor de Biblioteca Musical (CLI)

Sistema de línea de comandos desarrollado en **Python** y **SQLite** para administrar un catálogo musical relacional, consultar métricas y garantizar la integridad de los datos.

## Características principales

* **Gestión CRUD completa:** Registro, búsqueda flexible (insensible a mayúsculas y acentos), modificación y eliminación de bandas, discos, canciones y géneros.
* **Integridad referencial:** Esquema relacional normalizado con llaves foráneas (`ON DELETE SET NULL`, `ON DELETE CASCADE`) y prevención de duplicados (`UNIQUE`).
* **Transacciones seguras:** Control explícito mediante `COMMIT` y `ROLLBACK`, además de cancelación segura desde cualquier punto de captura.
* **Exploración y estadísticas:** Consultas relacionales entre entidades, rankings de ventas y reproducciones en streaming, promedios por banda y cálculo de duración total por álbum.
* **Autoinicialización:** Creación automática de la base de datos y sus tablas al iniciar el programa si no existe un archivo previo.

## Estructura del proyecto

* `menu_principal.py`: Punto de entrada, conexión a SQLite e inicialización de tablas.
* `sub_menus.py`: Navegación y mapeo de comandos por módulo.
* `funciones_agregacion.py`: Lógica de inserción y validación de nuevos registros.
* `funciones_mostrar_modificar.py`: Búsquedas, relaciones, ediciones y eliminaciones.
* `funciones_estadisticas.py`: Consultas agregadas, rankings y métricas.
* `modulo_apollo_general.py`: Validaciones de entrada, normalización de texto y manejo de transacciones.
* `modulo_apollo_bme.py`: Lógica auxiliar para actualizaciones y borrados en cascada.

## Cómo ejecutarlo

1. Asegúrate de tener **Python 3** instalado.
2. Clona o descarga este repositorio y abre una terminal en la carpeta del proyecto.
3. Ejecuta el archivo principal:

```bash
python menu_principal.py
```

## Evolución y próximos pasos

Esta versión nació de una idea que quería desarrollar como pasatiempo cuando comencé a aprender **Python**. Con cada nueva lección, comando y función que he ido incorporando, el proyecto ha evolucionado hasta convertirse en un gestor relacional completo.

Esta no es su versión definitiva, sino una base en constante crecimiento:

* **Próxima actualización:** Integrar bibliotecas como **`pandas`** para optimizar el manejo de datos y potenciar los reportes del apartado estadístico.