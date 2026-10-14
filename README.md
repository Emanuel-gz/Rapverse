# Rapverse

Una web editorial en español dedicada a Playboi Carti y Cochise: sus recorridos, su evolución musical y una selección de canciones para explorar ambos universos.

El proyecto conserva HTML, CSS y JavaScript sin framework, dependencias de aplicación ni compilación. Las fuentes, las imágenes y los nueve fragmentos de audio se sirven desde el proyecto.

## Abrir el proyecto

Desde la carpeta `Rapverse`:

```bash
python3 tools/serve.py --port 8000
```

Abre http://127.0.0.1:8000 en tu navegador. También puedes abrir `index.html` directamente; se recomienda el servidor incluido para las fuentes, el almacenamiento y el avance del audio. `tools/serve.py` admite solicitudes HTTP Range; el servidor básico `python -m http.server` no las admite y algunos navegadores limitan el avance con él. Detén el servidor con `Ctrl+C`.

## Estructura

- `index.html`: navegación, secciones y contenido inicial accesible sin JavaScript.
- `styles.css`: identidad negro y rojo, diseño adaptable, controles, tipografía local, impresión y movimiento reducido.
- `script.js`: fichas documentadas, pestañas con teclado, búsqueda de canciones, filtros, guardadas, reproductor compartido y menú móvil.
- `gallery.js`: filtros y ampliación de fotografías con teclado y restauración del foco.
- `fx.js`: capa opcional de interacciones (progreso de scroll, luz que sigue al puntero, marquesina reactiva, titulares que se encienden, decodificación del titular y ráfaga al guardar). Respeta `prefers-reduced-motion`.
- `assets/`: gráficos, fuentes locales y sus licencias.
- `assets/music/`: nueve portadas y nueve fragmentos locales, incluida «Location» de Playboi Carti; `manifest.json` registra correspondencias, formatos, duraciones y huellas SHA-256.
- `docs/SOURCES.md`: fuentes, criterio de selección y alcance editorial.
- `tools/sync-fallback.mjs`: sincroniza el contenido inicial del HTML con los datos de JavaScript.
- `assets/photos/`: las catorce fotografías (las de baja resolución, mejoradas) y su registro de procedencia; los archivos tal como se aportaron están en `assets/photos/originals/`.
- `tools/enhance-photos.py`: regenera las versiones mejoradas desde `originals/` (requiere `opencv-python` y `numpy`; la web no los necesita).
- `tools/import-photos.py` y `tools/photos.json`: validan e integran la selección fotográfica.
- `tools/finish.sh`: ejecuta la integración, las comprobaciones y el empaquetado.
- `tools/serve.py`: servidor local con soporte HTTP Range para avanzar por los fragmentos.
- `tools/package.py`: comprueba los recursos locales y genera un ZIP completo.
- `tests/smoke.py`: comprobaciones funcionales con Playwright y Chromium.

## Interacciones

Las fichas ofrecen Historia, Evolución, Estilo y actitud e Influencias. Puedes cambiar de pestaña con las flechas, Inicio y Fin. El catálogo permite combinar una búsqueda por título, crédito o año con un filtro; la búsqueda ignora mayúsculas y acentos. El corazón guarda canciones en este navegador. Si el almacenamiento está bloqueado, la colección sigue funcionando durante la visita.

«El sonido» incluye nueve canciones con sus portadas y fragmentos locales. Los discos muestran la portada de cada tema y giran durante la reproducción. El reproductor permite reproducir, pausar, detener y volver al inicio, desplazarse por el fragmento, ajustar el volumen y silenciar. Con JavaScript utiliza un único elemento de audio persistente: cambiar la búsqueda, el filtro o las guardadas conserva la reproducción y evita que suenen dos canciones a la vez. La reproducción comienza al pulsar un control.

Las búsquedas de Spotify siguen disponibles y se abren en una pestaña nueva. Sin JavaScript, cada canción ofrece controles de audio nativos del navegador; las biografías, la selección completa, la comparación y las fuentes siguen disponibles, con navegación móvil visible.

El corazón, además, lanza una breve ráfaga de partículas; la marquesina acelera con el scroll y se invierte al subir. La preferencia de movimiento reducido desactiva los giros y los efectos animados sin impedir escuchar los fragmentos.

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

Las pruebas inician y detienen su propio servidor local. Comprueban recursos, pestañas, enlaces, menú, búsqueda, guardadas, almacenamiento bloqueado y corrupto, contenido sin JavaScript y ausencia de desbordamiento en seis anchos de pantalla (320–1440 px). También verifican las nueve asociaciones de portada y audio, reproducción real, controles, avance, errores, fin, exclusión de pistas y animación sincronizada.

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

Las biografías y los catálogos enlazan Apple Music, Pitchfork y Billboard. Los puestos del Hot 100 corresponden a semanas concretas de un archivo independiente; «Sky», «Hatchback», «POCKET ROCKET» y «TURN IT UP» estaban en «Top Songs» de Apple Music al consultar la selección. «Location» se añadió desde el ZIP aportado y enlaza el catálogo de Carti. No es un ranking actual de reproducciones. Los datos y las interpretaciones están identificados por separado; consulta [las fuentes](docs/SOURCES.md).

Las parejas de portada y audio proceden de sus respectivas carpetas del ZIP `canciones y covers playboi carti, cochise.zip`. Se conservaron los bytes originales: los ocho archivos `.mpeg`, que contienen MP3, usan ahora `.mp3`; `turn it up.mp4`, que contiene solo audio AAC en un contenedor M4A, usa `.m4a`. No se recodificó ni se alargó ningún fragmento. [El manifiesto de audio](assets/music/manifest.json) permite revisar cada correspondencia y sus huellas.

Anton y Space Grotesk incluyen sus licencias SIL Open Font License 1.1. Los SVG originales se conservan. La página no carga fuentes remotas, analítica ni APIs al abrirse. Es un proyecto independiente, sin afiliación con los artistas.

## Cambios en GitHub y distribución

La revisión corresponde a la rama `feat/rapverse-visual-refresh` y al [Pull Request #2](https://github.com/Emanuel-gz/Rapverse/pull/2). El PR reúne la selección fotográfica y los nueve fragmentos con sus portadas y controles. Revisa los cambios antes de incorporarlos a `main`.

Para subirlos manualmente al repositorio existente, copia el **contenido** de la carpeta `Rapverse/` a la raíz actual del repositorio: `index.html`, `styles.css`, `script.js`, las demás entradas existentes y las carpetas `assets/`, `docs/`, `tools/` y `tests/`. Conserva especialmente `assets/music/` completo, incluido `manifest.json`; no añadas una segunda carpeta `Rapverse/` dentro de la raíz. Las rutas de imágenes, audio, fuentes y scripts son relativas, compatibles con GitHub Pages tanto en la raíz de un dominio como bajo `/Rapverse/`.

El ZIP de distribución conserva la carpeta `Rapverse` con código, documentación, pruebas, herramientas y todos los recursos locales. No necesita `node_modules`, un archivo de configuración secreto ni un proceso de instalación para mostrar la web. El directorio `.git` y las cachés de prueba no forman parte de la distribución.
