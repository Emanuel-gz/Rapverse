# Verificación de esta revisión

Revisión técnica del 13 de octubre de 2026, hora de Panamá.

El ZIP subido y el repositorio integrado coincidían en los archivos del proyecto. Se conservaron HTML, CSS y JavaScript sin framework, las fuentes locales, los SVG y el contenido documentado.

- La aplicación actual pasó sus 15 pruebas funcionales: recursos, pestañas con teclado, créditos, navegación móvil, búsqueda combinada, resultados vacíos, favoritos persistentes, almacenamiento denegado/corrupto, sincronización entre pestañas con foco conservado, semántica y contenido sin JavaScript.
- Se comprobó la ausencia de desbordamientos a 320, 375, 390, 650, 768, 1024 y 1440 píxeles.
- Las dos pruebas de galería se ejecutaron en una copia temporal con 14 JPEG de prueba. Pasaron los filtros, diálogo, flechas, Escape, restauración del foco y desplazamiento, carga de imágenes locales y enlaces sin JavaScript. También pasó el diseño adaptable con la galería activa.
- El importador pasó simulación, validación de JPEG y dimensiones, segunda ejecución sin duplicaciones, fallos de descarga sin cambios y restauración tras un fallo de instalación.
- Se comprobaron sintaxis JavaScript/Python/Bash, espacios del diff, referencias locales y contenido/integridad del ZIP.

## Límite pendiente: fotografías originales

El proxy del entorno devolvió HTTP 403 al descargar las URLs de las fotos. Los dominios necesarios no estaban en la lista permitida. Por tanto, los originales no se incluyeron en la entrega ni se comprobó su encuadre real. Los JPEG de prueba permanecen fuera del proyecto y no se distribuyen.

El código de integración completo está en `tools/import-photos.py`, junto con las 14 URLs en `tools/photos.json`. Después de habilitar sus dominios en la configuración del entorno, `bash tools/finish.sh` descarga los originales, activa la presentación fotográfica, ejecuta las 17 pruebas y genera el ZIP con todas las fotos. Si las descargas fallan, conserva la página actual funcionando.
