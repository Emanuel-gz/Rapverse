# Rapverse

Una web editorial en español dedicada a Playboi Carti y Cochise: sus recorridos, su evolución musical y una selección de canciones para explorar ambos universos.

El proyecto conserva HTML, CSS y JavaScript sin framework, dependencias de aplicación ni compilación. Las fuentes y los recursos gráficos se sirven desde el proyecto.

## Abrir el proyecto

Desde la carpeta `Rapverse`:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Abre http://127.0.0.1:8000 en tu navegador. También puedes abrir `index.html` directamente; se recomienda el servidor local para un comportamiento uniforme de las fuentes y el almacenamiento del navegador. Detén el servidor con `Ctrl+C`.

## Estructura

- `index.html`: navegación, secciones y contenido inicial accesible sin JavaScript.
- `styles.css`: diseño editorial adaptable, controles, tipografía local, impresión y movimiento reducido.
- `script.js`: fichas documentadas, pestañas con teclado, búsqueda de canciones, filtros, guardadas y menú móvil.
- `gallery.js`: filtros y ampliación de fotografías con teclado y restauración del foco.
- `assets/`: gráficos, fuentes locales y sus licencias.
- `docs/SOURCES.md`: fuentes, criterio de selección y alcance editorial.
- `tools/sync-fallback.mjs`: sincroniza el contenido inicial del HTML con los datos de JavaScript.
- `assets/photos/`: las catorce fotografías originales y su registro de procedencia.
- `tools/import-photos.py` y `tools/photos.json`: validan e integran la selección fotográfica.
- `tools/finish.sh`: ejecuta la integración, las comprobaciones y el empaquetado.
- `tools/package.py`: comprueba los recursos locales y genera un ZIP completo.
- `tests/smoke.py`: comprobaciones funcionales con Playwright y Chromium.

## Interacciones

Las fichas ofrecen Historia, Evolución, Estilo y actitud e Influencias. Puedes cambiar de pestaña con las flechas, Inicio y Fin. El catálogo permite combinar una búsqueda por título, crédito o año con un filtro; la búsqueda ignora mayúsculas y acentos. El corazón guarda canciones en este navegador. Si el almacenamiento está bloqueado, la colección sigue funcionando durante la visita.

Las búsquedas de Spotify se abren en una pestaña nueva. La página no reproduce ni aloja audio. Sin JavaScript, las biografías, la selección completa, la comparación y las fuentes siguen disponibles, con navegación móvil visible.

## Ejecutar la integración completa en Codex

Dentro del proyecto, ejecuta:

```bash
bash tools/finish.sh
```

Las catorce fotos ya están incluidas en `assets/photos/`. Este script valida los archivos locales y sincroniza su presentación en la portada, las fichas y la galería. Después comprueba JavaScript, ejecuta las pruebas y genera `../Rapverse-mejorado.zip`. Se detiene si un paso falla.

La página y este flujo usan las fotografías incluidas en el proyecto. Las URL de procedencia se conservan como referencia; no es necesario descargarlas de nuevo ni configurar permisos de red para mostrar las imágenes.

Puedes revisar el plan sin descargar ni modificar nada:

```bash
python3 tools/import-photos.py --from-directory assets/photos --dry-run
```

Si ya tienes los originales guardados, nómbralos según `tools/photos.json` y usa:

```bash
python3 tools/import-photos.py --from-directory /ruta/a/las/fotos
```

Las fotografías se instalan en `assets/photos/`, junto con su registro de procedencia y huellas SHA-256. La galería ofrece filtros, ampliación, flechas y cierre con Escape; sin JavaScript sus enlaces abren el archivo local original. Los SVG originales se conservan.

## Mantener y comprobar

Cuando cambies los datos de `artistContent`, `songs`, `comparisons` o las fuentes en `script.js`, sincroniza el HTML inicial:

```bash
node tools/sync-fallback.mjs
```

El sincronizador modifica únicamente los bloques identificados como `fallback` y el contador inicial. Es una herramienta opcional de mantenimiento; la web no requiere ejecutarlo para abrirse.

```bash
node --check script.js
node --check gallery.js
python3 tests/smoke.py -v
git diff --check
```

Las pruebas inician y detienen su propio servidor local. Comprueban recursos, pestañas, enlaces, menú, búsqueda, guardadas, almacenamiento bloqueado y corrupto, contenido sin JavaScript y ausencia de desbordamiento en siete anchos de pantalla.

Para instalar las herramientas de prueba en otra máquina:

```bash
python3 -m venv .venv
# Linux/macOS:
. .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python3 -m pip install playwright==1.62.0
python3 -m playwright install chromium
python3 tests/smoke.py -v
```

Si tienes Chromium instalado, puedes indicar su ruta con `RAPVERSE_BROWSER_PATH`. Playwright y Node son herramientas de desarrollo; no son dependencias de la página.

## Contenido y recursos

Las biografías y los catálogos enlazan Apple Music, Pitchfork y Billboard. Los puestos del Hot 100 corresponden a semanas concretas de un archivo independiente; las otras canciones estaban en «Top Songs» de Apple Music al consultar la selección. No es un ranking actual de reproducciones. Los datos y las interpretaciones están identificados por separado; consulta [las fuentes](docs/SOURCES.md).

Anton y Space Grotesk incluyen sus licencias SIL Open Font License 1.1. Los SVG originales se conservan. La página no carga fuentes remotas, analítica ni APIs al abrirse. Es un proyecto independiente, sin afiliación con los artistas.

## Cambios en GitHub y distribución

La revisión se prepara en `feat/rapverse-visual-refresh`. Un Pull Request permite revisar los cambios antes de incorporarlos a `main`.

El ZIP de distribución conserva la carpeta `Rapverse` con código, documentación, pruebas, herramientas y todos los recursos locales. No necesita `node_modules`, un archivo de configuración secreto ni un proceso de instalación para mostrar la web. El directorio `.git` y las cachés de prueba no forman parte de la distribución.
