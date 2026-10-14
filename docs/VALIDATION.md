# Verificación de esta revisión

Revisión técnica del 14 de octubre de 2026, hora de Panamá.

El proyecto conserva HTML, CSS y JavaScript sin framework, su estructura editorial, fuentes locales, SVG, fichas, comparación, búsqueda, filtros, guardadas, efectos y galería de catorce fotografías.

## Portadas y audio

- Las nueve carpetas del ZIP de canciones se inspeccionaron por separado. Cada portada y fragmento se asocia por su carpeta original, incluida `LOCATION`, incorporada como «Location» de Playboi Carti.
- `assets/music/manifest.json` registra archivos originales, rutas finales, formatos reales, duraciones y SHA-256. Los dieciocho archivos coinciden byte por byte con el ZIP aportado.
- Se inspeccionaron visualmente las nueve portadas y FFmpeg decodificó los nueve audios correctamente. Los ocho `.mpeg` son MP3; `turn it up.mp4` contiene solo AAC/M4A. Se corrigieron extensiones sin recodificar.
- Los audios no incorporan etiquetas de título/artista: la identificación se sustenta en los nombres de sus carpetas. Magnolia y Location usan la misma composición de portada, con JPEG distintos conservados según su carpeta.

## Comprobaciones

- 27 pruebas funcionales con Playwright y Chromium, sin omisiones: reproducción y pausa reales de los nueve fragmentos, correspondencias y huellas, un solo audio activo, cambio de pista, avance, volumen, silencio, teclado, fin y repetición, error y reintento, carga pendiente sin giro y persistencia al buscar, filtrar o guardar.
- Se comprueban las funciones existentes: fichas y pestañas, fuentes y créditos, filtros, búsqueda y resultados vacíos, favoritos persistentes, almacenamiento bloqueado/corrupto, sincronización entre pestañas y foco, navegación móvil, galería y ampliación de fotografías, enlaces, semántica, efectos y contenido sin JavaScript.
- El contenido sin JavaScript incluye las nueve portadas y nueve controles nativos de audio. Con JavaScript, un único elemento de audio persiste al cambiar la lista.
- Vista adaptable sin desbordamiento a 320, 375, 390, 768, 1024 y 1440 píxeles, con un fragmento en reproducción. Revisión visual de la sección en escritorio y móvil.
- Los discos y el ecualizador se animan solo durante reproducción real; con movimiento reducido la música sigue funcionando y las animaciones quedan desactivadas.
- Se comprobaron cambios rápidos, doble/triple pulsación, parada durante carga y cancelaciones sin reproducción simultánea ni errores JavaScript.
- Sintaxis JavaScript/Python/Bash, sincronización del HTML inicial, referencias locales, espacios del diff e integridad del ZIP comprobados.

## Vista previa y distribución

`python3 tools/serve.py --port 8000` ofrece HTTP Range para el avance por los fragmentos. Se verificaron respuestas 206 para rangos iniciales, intermedios y finales y el desplazamiento real a 0:08. El servidor básico de Python no admite rangos y Chromium limita el avance con él, aunque el audio esté descargado; por eso el servidor incluido también se usa en las pruebas.

`bash tools/finish.sh` valida las fotografías, sincroniza el HTML inicial, ejecuta las pruebas y empaqueta el proyecto completo. Las rutas son relativas y todos los recursos necesarios están incluidos; el ZIP excluye `.git`, entornos virtuales y cachés.
