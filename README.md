# LISTLOG - Listado Rápido de Directorios para IA

📺 **Mira el videotutorial de funcionamiento aquí:** [https://www.youtube.com/watch?v=qhAvNsMBzGA](https://www.youtube.com/watch?v=qhAvNsMBzGA)

## Descripción

Herramienta de línea de comandos que genera reportes estructurados de directorios en formato tabla, optimizados para ser copiados al portapapeles y pegados directamente como contexto para IA.

## Características

* **Modo Simple**: Lista solo el contenido del directorio raíz (1 nivel)
* **Modo Recursivo**: Escanea todo el árbol de directorios con estadísticas totales
* **Sin dependencias externas**: Solo usa bibliotecas estándar de Python
* **Auto-copia al portapapeles**: El reporte se copia automáticamente (Ctrl+V listo)
* **Guardado automático**: Los logs se guardan en `%USERPROFILE%\.ialogpack\logs\`

## Instalación

```cmd
instalar.bat

```

## Uso

### Línea de comandos

```cmd
# Modo simple (solo el directorio actual)
listlog.py "C:\ruta\carpeta"

# Modo recursivo
listlog.py "C:\ruta\carpeta" --recursive

```

### Menú contextual (Windows)

Una vez instalado:

1. Click derecho en cualquier carpeta o en el fondo del directorio
2. Ir a `IALogPack`
3. Seleccionar:
* `1_listlog` → Modo simple
* `2_listlog_recursive` → Modo recursivo



## Ejemplo de salida

```
==================================================================================
   LISTADOR DE DIRECTORIO - LISTLOG v1.0.0 (SIMPLE)
==================================================================================
 Directorio: C:\Proyectos\mi_app

NOMBRE                                             TIPO    TAMANO     MODIFICADO     
------------------------------------------------------------------------------------
src                                                DIR      <DIR>     2026-06-14 10:30
tests                                              DIR      <DIR>     2026-06-14 09:15
README.md                                          .md      2.15 KB   2026-06-13 18:00
requirements.txt                                   .txt     1.02 KB   2026-06-12 15:20
main.py                                            .py      8.45 KB   2026-06-14 11:00
config.json                                        .json    0.85 KB   2026-06-10 09:00
------------------------------------------------------------------------------------
 RESUMEN: 4 Arch. (0 PDFs) | 2 Carp. | Total: 12.47 KB (12,771 B) | Tiempo: 0.023 seg
==================================================================================

```

## Formato de salida

| Columna | Descripción |
| --- | --- |
| NOMBRE | Nombre del archivo o carpeta |
| TIPO | Extensión del archivo o `DIR` para carpetas |
| TAMANO | Tamaño formateado (B/KB/MB/GB) o `<DIR>` |
| MODIFICADO | Fecha y hora de última modificación |

## Limitaciones

* ❌ No analiza contenido de archivos
* ❌ No muestra hashes ni metadatos internos
* ❌ No detecta tipos MIME reales (solo extensión)
* ❌ Modo recursivo: listado plano sin jerarquía visual

## Dependencias

**Ninguna** - Solo bibliotecas estándar de Python.

## Archivos generados

Los reportes se guardan automáticamente en:

```
%USERPROFILE%\.ialogpack\logs\listlog_nombre_carpeta_YYYY-MM-DD_HH-MM-SS.log

```

## Desinstalación

```cmd
desinstalador.bat

```

## Licencia

MIT

## Versión

1.0.0

---

*Esta herramienta forma parte del paquete IALogPack.*
