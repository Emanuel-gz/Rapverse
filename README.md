# Rapverse - web interactiva Hecha por Emanuel-gz

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

Las fichas reúnen hitos biográficos y de discografía hasta 2026 con enlaces a Apple Music, Pitchfork, Billboard y un archivo histórico de listas. Las influencias se presentan según el alcance de cada fuente: mentoría, colaboraciones, antecedentes señalados por crítica o referencias culturales. Ninguna semejanza vocal se convierte en influencia personal atribuida. La tabla y las pestañas identifican por separado datos e interpretaciones; consulta [las fuentes y el criterio editorial](docs/SOURCES.md).

La selección ofrece cuatro canciones por artista. Los puestos del Hot 100 corresponden a semanas concretas; las otras canciones aparecen en «Top Songs» de Apple Music al momento de la consulta. No es un ranking actual de reproducciones.

Las imágenes son ilustraciones originales; no hay audio ni vídeo alojado o incrustado. Anton y Space Grotesk incluyen sus licencias SIL Open Font License 1.1. La página no carga fuentes remotas, analítica ni APIs. Los enlaces de Spotify abren búsquedas en otra pestaña y se identifican como tales.

## Revisar y subir desde Codex

El trabajo continúa en la rama `feat/rapverse-page`. Estos comandos se ejecutan en la terminal del entorno de Codex, dentro de `/workspace/Rapverse`. **No fusionan el Pull Request con `main`**.

1. Revisa el estado y las diferencias de esta ampliación:

   ```bash
   cd /workspace/Rapverse
   git branch --show-current
   git status --short
   git diff --check
   git diff --stat
   git diff
   ```

2. Ejecuta las comprobaciones:

   ```bash
   node --check script.js
   python3 tests/smoke.py -v
   ```

3. Si las diferencias son correctas, prepara solo los archivos modificados y revisa el contenido del commit:

   ```bash
   git add README.md index.html styles.css script.js docs/SOURCES.md tests/smoke.py
   git diff --cached --check
   git diff --cached --stat
   git diff --cached
   ```

4. Sube el nuevo commit a la **misma rama**:

   ```bash
   git commit -m "feat: complete sourced artist profiles and influences"
   git push origin feat/rapverse-page
   ```

5. Abre el Pull Request existente en GitHub y consulta **Files changed**. El nuevo commit aparecerá allí automáticamente. Revisa las fuentes y los límites de las influencias antes de decidir si fusionas el PR; este paso no es automático.
](http://127.0.0.1:8000/)
