# Fuentes, criterio editorial y recursos

Consulta realizada el **12 de octubre de 2026** (America/Panama). La página está en español y separa datos documentados e interpretación editorial. No se usaron citas de artistas.

## Datos que se pudieron verificar

Se consultaron los archivos JSON del archivo independiente [Historic Billboard Hot 100 Data](https://github.com/mhollingshead/billboard-hot-100), de mhollingshead. Su README explica que obtiene listas de Billboard. Es una **fuente secundaria**, no una publicación oficial de Billboard. Se verificó cada registro citado contra sus campos `song`, `artist`, `this_week` y `date`.

Los enlaces de la página fijan el commit `abefdd18eaf587c102bda9b0f2bc11aa9ae250d5` para evitar que una actualización del archivo cambie silenciosamente las referencias. No se redistribuye el conjunto completo de listas ni textos periodísticos: solo se comunican unos pocos datos factuales con atribución.

| Afirmación                                                                                          | Registro consultado                                                                                                                 |
| --------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| «Magnolia» y «Wokeuplikethis\*» aparecen el 20 de mayo de 2017; la segunda acredita a Lil Uzi Vert. | [2017-05-20](https://github.com/mhollingshead/billboard-hot-100/blob/abefdd18eaf587c102bda9b0f2bc11aa9ae250d5/date/2017-05-20.json) |
| «Magnolia», Playboi Carti, posición semanal 29.                                                     | [2017-07-08](https://github.com/mhollingshead/billboard-hot-100/blob/abefdd18eaf587c102bda9b0f2bc11aa9ae250d5/date/2017-07-08.json) |
| «Shoota», Playboi Carti Featuring Lil Uzi Vert, posición 46.                                        | [2018-05-26](https://github.com/mhollingshead/billboard-hot-100/blob/abefdd18eaf587c102bda9b0f2bc11aa9ae250d5/date/2018-05-26.json) |
| «Tell Em», Cochise & $NOT, posición 64.                                                             | [2021-06-12](https://github.com/mhollingshead/billboard-hot-100/blob/abefdd18eaf587c102bda9b0f2bc11aa9ae250d5/date/2021-06-12.json) |
| «Tell Em» también figura el 3 de julio de 2021.                                                     | [2021-07-03](https://github.com/mhollingshead/billboard-hot-100/blob/abefdd18eaf587c102bda9b0f2bc11aa9ae250d5/date/2021-07-03.json) |
| «FE!N», Travis Scott Featuring Playboi Carti, posición 5.                                           | [2023-08-12](https://github.com/mhollingshead/billboard-hot-100/blob/abefdd18eaf587c102bda9b0f2bc11aa9ae250d5/date/2023-08-12.json) |
| «Evil J0rdan», Playboi Carti, posición 2.                                                           | [2025-03-29](https://github.com/mhollingshead/billboard-hot-100/blob/abefdd18eaf587c102bda9b0f2bc11aa9ae250d5/date/2025-03-29.json) |

Se examinó además `all.json` de ese archivo para confirmar que «Tell Em» aparece en cuatro listas: 12 y 19 de junio, 3 y 17 de julio de 2021. **No son semanas consecutivas.** Se excluyó una entrada de 1971 de otro artista llamado Cochise; compartir nombre no establece identidad.

Los años de la selección se refieren a su presencia en listas, no necesariamente a su fecha exacta de lanzamiento. Las posiciones mostradas corresponden a semanas concretas; no se presentan como reproducciones actuales, ranking mundial ni medidas de calidad. La selección no contiene igual número de canciones de cada artista porque solo incluye registros contrastados con esta fuente.

## Investigación pendiente y alcance publicado

El proxy del entorno respondió `403 Forbidden` antes de llegar a las páginas de Wikipedia, RCA Records, Playboi Carti y Billboard. La configuración activa mantiene el preset de gestores de paquetes; los dominios adicionales están guardados en un borrador y requieren revisión, guardado y publicación en los ajustes del entorno.

Se solicitaron únicamente estos destinos para la investigación y los enlaces de escucha:

- `en.wikipedia.org`
- `www.rcarecords.com`
- `www.playboicarti.com`
- `www.billboard.com`
- `pitchfork.com`
- `music.apple.com`
- `open.spotify.com`

Las páginas bloqueadas **no cuentan como fuentes consultadas ni verificadas**. Por ello no se publican fechas de nacimiento, nombres legales, ciudades de origen, biografías completas, cronologías de álbumes ni influencias declaradas. Queda pendiente ampliar esas secciones después de verificar discografías oficiales e entrevistas directas. No se atribuye a Cochise una influencia de Carti por un parecido vocal.

La evolución publicada utiliza hitos comerciales contrastados; no pretende describir toda la evolución sonora. Las pestañas de estilo y la comparación están marcadas como lectura editorial: ofrecen preguntas de escucha, no diagnósticos psicológicos ni opiniones atribuidas a los músicos. «Intenso» y «juguetón» se refieren a posibles impresiones musicales.

## Recursos y condiciones de uso

| Recurso                                                          | Procedencia y permiso                                                                                                                                                                                       |
| ---------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `assets/universe.svg`, `carti.svg`, `cochise.svg`, `favicon.svg` | Ilustraciones originales creadas para este proyecto. No reproducen fotos, retratos ni portadas oficiales.                                                                                                   |
| Anton                                                            | [Google Fonts, Anton](https://github.com/google/fonts/tree/main/ofl/anton). SIL Open Font License 1.1, incluida en `assets/fonts/Anton-OFL.txt`. No se modificó el archivo de fuente.                       |
| Space Grotesk                                                    | [Google Fonts, Space Grotesk](https://github.com/google/fonts/tree/main/ofl/spacegrotesk). SIL Open Font License 1.1, incluida en `assets/fonts/SpaceGrotesk-OFL.txt`. No se modificó el archivo de fuente. |
| Audio y vídeo                                                    | No se alojan, incrustan ni reproducen grabaciones. Los botones abren búsquedas externas en Spotify, identificadas como nueva pestaña.                                                                       |

Los archivos visuales y tipográficos se sirven localmente; no hay CDN, analítica, cookies, llamadas a APIs ni solicitudes a plataformas musicales al cargar la página. Los nombres de artistas y canciones se usan con propósito informativo, sin afirmar afiliación. Las licencias de fuentes no se extienden al resto del repositorio.
