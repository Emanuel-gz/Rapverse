# Rapverse

🎧 RapVerse is an interactive web platform dedicated exclusively to Playboi Carti and Cochise. Explore their stories, musical evolution, most popular songs, personalities, influences, similarities, and differences through a modern and immersive Hip-Hop, Rap, and Trap experience.

## Desarrollo

Página estática en español, con HTML, CSS y JavaScript sin framework, dependencias de aplicación ni proceso de compilación. Se implementó en la raíz porque el repositorio original solo tenía este README.

Desde la terminal de Codex:

```bash
cd /workspace/Rapverse
python3 -m http.server 8000 --bind 127.0.0.1
```

El servidor sirve la página y todos sus recursos locales. Detenlo con `Ctrl+C`. En este entorno la validación se realiza mediante Chromium y peticiones locales; no se presupone que la interfaz de Codex exponga una vista previa pública. Para verla en tu equipo, clona el repositorio y ejecuta el mismo comando desde su carpeta; abre la dirección local que indica el servidor en tu navegador.

### Archivos

- `index.html`: estructura, navegación, secciones, accesibilidad y metadatos.
- `styles.css`: diseño adaptable, tipografía local, impresión y movimiento reducido.
- `script.js`: contenido documental y editorial, pestañas accesibles, filtros y menú móvil.
- `assets/`: ilustraciones SVG originales, fuentes locales y licencias.
- `docs/SOURCES.md`: registros consultados, criterio editorial y alcance de la investigación.
- `tests/smoke.py`: pruebas funcionales de navegador.

### Comprobaciones

```bash
node --check script.js
python3 tests/smoke.py -v
git diff --check
```

Las pruebas de navegador usan Playwright y Chromium ya disponibles en el entorno de Codex. Inician su propio servidor en un puerto local libre y lo detienen al terminar. Comprueban carga de recursos sin solicitudes externas, pestañas con teclado, filtros, créditos de colaboradores, menú móvil, enlaces internos, semántica y ausencia de desbordamiento en siete tamaños de pantalla. La aplicación funciona sin Playwright; solo las pruebas lo necesitan.

En otra máquina instala las herramientas de prueba en un entorno de Python y usa un Chromium local, o instala el navegador de Playwright:

```bash
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install playwright==1.62.0
python3 -m playwright install chromium
python3 tests/smoke.py -v
```

Si usas otro ejecutable de Chromium, indica su ruta mediante `RAPVERSE_BROWSER_PATH`. No es necesario instalar Node para servir la página; se utiliza para comprobar la sintaxis de JavaScript.

## Contenido y licencias

Los datos publicados se verificaron contra registros históricos de un archivo independiente de Billboard Hot 100 y enlazan versiones fijas. Las interpretaciones están identificadas y no describen la personalidad privada. La selección no es un ranking actual ni una discografía completa. La biografía completa, la evolución de álbumes y las influencias declaradas quedan pendientes de acceso a las fuentes musicales bloqueadas por la red; no se rellenaron con afirmaciones sin verificar. Consulta [las fuentes y limitaciones](docs/SOURCES.md).

Las imágenes son ilustraciones originales; no hay audio ni vídeo alojado o incrustado. Anton y Space Grotesk incluyen sus licencias SIL Open Font License 1.1. La página no carga fuentes remotas, analítica ni APIs. Los enlaces de Spotify abren búsquedas en otra pestaña y se identifican como tales.

## Revisar y subir desde Codex

Estos comandos utilizan las herramientas Git disponibles en el entorno y no dependen de botones específicos de la interfaz. Los cambios se dejan sin commit ni push para revisión.

1. Inspecciona los archivos nuevos y las diferencias. `git diff` solo muestra cambios en archivos ya seguidos; abre también `index.html`, `styles.css`, `script.js`, `assets/`, `docs/` y `tests/` en el explorador de archivos.

   ```bash
   cd /workspace/Rapverse
   git status --short
   git diff -- README.md
   ```

2. Ejecuta las comprobaciones anteriores. Crea una rama para subir la funcionalidad sin enviar directamente a `main`:

   ```bash
   git switch -c feat/rapverse-page
   ```

3. Prepara únicamente los archivos de esta funcionalidad y revisa lo que incluirá el commit:

   ```bash
   git add .gitignore README.md index.html styles.css script.js assets docs tests
   git diff --cached --check
   git diff --cached --stat
   git diff --cached
   ```

4. Confirma y sube la rama:

   ```bash
   git commit -m "feat: add Rapverse artist discovery page"
   git push -u origin feat/rapverse-page
   ```

5. Abre `Emanuel-gz/Rapverse` en GitHub y crea un Pull Request desde `feat/rapverse-page` hacia `main`. Revisa archivos, pruebas y las limitaciones documentales antes de fusionarlo. Se verificó acceso de lectura al repositorio; el push requiere que tu cuenta tenga permiso de escritura. Si falla, sigue el mecanismo de conexión/autorización de GitHub de Codex; no pegues tokens en archivos ni en el chat.

Publicar el entorno de Codex y subir commits a GitHub son operaciones diferentes. Los cambios de red guardados en los ajustes del entorno requieren revisión, guardado y publicación para completar la investigación pendiente.
