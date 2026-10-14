#!/usr/bin/env python3
"""Importa la selección fotográfica de Rapverse con Python 3.9+, sin paquetes.

    python3 tools/import-photos.py --dry-run
    python3 tools/import-photos.py
    python3 tools/import-photos.py --from-directory /ruta/a/originales

Los originales locales deben usar los nombres de tools/photos.json. Primero
se comprueban todos los archivos; sólo entonces se instalan fotos y HTML. Una
descarga fallida conserva el sitio. --dry-run no escribe ni accede a la red.
Se respetan las restricciones de red y la configuración de proxy del entorno.
"""

import argparse
import hashlib
import html
import json
import os
from pathlib import Path
import re
import shutil
import struct
import sys
import tempfile
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parent.parent
MAX_BYTES = 25 * 1024 * 1024
TIMEOUT = 30
HOSTS = (
    "encrypted-tbn0.gstatic.com",
    "www.masqueradeatlanta.com",
    "resources.tidal.com",
    "m.media-amazon.com",
)
BLOCKS = ("hero", "carti", "cochise", "gallery", "license")
GALLERY_ORDER = (
    "carti-red-stage.jpg", "cochise-feature.jpg",
    "carti-beanie.jpg", "cochise-trench.jpg",
    "carti-blue-portrait.jpg", "cochise-blue-portrait.jpg",
    "carti-jersey.jpg", "cochise-red-jacket.jpg",
    "carti-lounge.jpg", "cochise-point.jpg",
    "carti-green-jacket.jpg", "cochise-suit.jpg",
    "carti-camo.jpg", "cochise-microphone.jpg",
)
ARTISTS = {"carti": "Playboi Carti", "cochise": "Cochise"}


class PhotoError(Exception):
    """Error previsto que debe dejar intacta la instalación existente."""


def digest(data):
    return hashlib.sha256(data).hexdigest()


def load_manifest(root):
    try:
        manifest = json.loads((root / "tools/photos.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise PhotoError(f"No se pudo leer tools/photos.json: {error}") from error
    if not isinstance(manifest, dict) or manifest.get("version") != 1:
        raise PhotoError("El manifiesto debe usar version: 1.")
    if manifest.get("destination") != "assets/photos":
        raise PhotoError("El destino del manifiesto debe ser assets/photos.")
    photos = manifest.get("photos")
    if not isinstance(photos, list) or len(photos) != 14:
        raise PhotoError("El manifiesto debe contener las 14 fotografías.")
    seen = set()
    for photo in photos:
        if not isinstance(photo, dict):
            raise PhotoError("Cada fotografía debe ser un objeto en el manifiesto.")
        for field in ("filename", "artist", "caption", "alt", "url", "source"):
            if not isinstance(photo.get(field), str) or not photo[field].strip():
                raise PhotoError(f"Falta un campo válido: {field}.")
        filename = photo["filename"]
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*\.jpg", filename):
            raise PhotoError(f"Nombre de archivo no válido: {filename!r}.")
        if filename in seen or photo["artist"] not in ARTISTS:
            raise PhotoError(f"Fotografía duplicada o artista no válido: {filename}.")
        seen.add(filename)
        for field in ("width", "height"):
            if type(photo.get(field)) is not int or not 0 < photo[field] <= 30000:
                raise PhotoError(f"Dimensión {field} no válida: {filename}.")
        parsed = urlsplit(photo["url"])
        if parsed.scheme != "https" or parsed.hostname not in HOSTS or parsed.username:
            raise PhotoError(f"URL ajena a los cuatro orígenes previstos: {filename}.")
    if seen != set(GALLERY_ORDER):
        raise PhotoError("Los nombres no coinciden con la selección de 14 fotografías.")
    return photos


def block_markers(name):
    return f"<!-- photos:{name}:start -->", f"<!-- photos:{name}:end -->"


def check_template(document):
    for name in BLOCKS:
        start, end = block_markers(name)
        if document.count(start) != 1 or document.count(end) != 1:
            raise PhotoError(f"index.html necesita una pareja única de marcadores photos:{name}.")
        if document.index(start) >= document.index(end):
            raise PhotoError(f"Los marcadores photos:{name} están desordenados.")
    if document.count("<!-- photos:navigation -->") != 1:
        raise PhotoError("index.html necesita el marcador único photos:navigation.")
    navigation = re.search(r'<nav\b[^>]*\bid="navigation"[^>]*>(.*?)</nav>', document, re.S)
    if not navigation or "<!-- photos:navigation -->" not in navigation.group(1):
        raise PhotoError("El marcador photos:navigation debe estar en la navegación principal.")
    if len(re.findall(r'href=[\"\']#galeria[\"\']', navigation.group(1))) > 1:
        raise PhotoError("La navegación ya contiene enlaces duplicados a #galeria.")
    visual_classes = re.findall(r'class="([^"]*\bartist-visual\b[^"]*)"', document)
    for artist in ARTISTS:
        if sum(f"{artist}-visual" in value.split() for value in visual_classes) != 1:
            raise PhotoError(f"Debe existir una tarjeta visual única para {artist}.")
    if len(re.findall(r'<p class="eyebrow">0[45] / DETRÁS DEL CONTENIDO</p>', document)) != 1:
        raise PhotoError("No se localizó la numeración de la sección de fuentes.")
    gallery_start, gallery_end = block_markers("gallery")
    outside_gallery = document[:document.index(gallery_start)] + document[document.index(gallery_end):]
    for identity in ("galeria", "photo-dialog", "gallery-title"):
        if re.search(rf'\bid=[\"\']{identity}[\"\']', outside_gallery):
            raise PhotoError(f"El identificador {identity} ya existe fuera del bloque de galería.")


def check_destinations(root, photos):
    """No seguir enlaces simbólicos al instalar dentro del proyecto."""
    for directory in (root / "assets", root / "assets/photos"):
        if directory.is_symlink() or (directory.exists() and not directory.is_dir()):
            raise PhotoError(f"El destino debe ser un directorio normal: {directory}")
    destinations = [root / "index.html", root / "assets/photos/SOURCES.md"]
    destinations.extend(root / "assets/photos" / photo["filename"] for photo in photos)
    for target in destinations:
        if target.is_symlink() or (target.exists() and not target.is_file()):
            raise PhotoError(f"El destino debe ser un archivo normal: {target}")
    if not (root / "index.html").is_file():
        raise PhotoError(f"No existe {root / 'index.html'}.")
    if not os.access(root, os.W_OK):
        raise PhotoError(f"No se puede escribir en el proyecto: {root}")
    for directory in (root / "assets", root / "assets/photos"):
        if directory.exists() and not os.access(directory, os.W_OK):
            raise PhotoError(f"No se puede escribir en el destino: {directory}")


def jpeg_dimensions(data, label):
    """Comprueba firma, segmentos, escaneo y cierre JPEG; lee dimensiones SOF.

    Usa la estructura del formato, sin un decodificador de imagen externo.
    Acepta JPEG secuencial y progresivo; rechaza HTML, WebP y bytes truncados.
    """
    if not data.startswith(b"\xff\xd8") or len(data) > MAX_BYTES:
        raise PhotoError(f"{label}: el recurso no es un JPEG válido de hasta 25 MiB.")
    position = 2
    dimensions = None
    has_scan = False
    has_quantization = False
    has_huffman = False
    sof = {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}
    while position < len(data):
        if data[position] != 0xFF:
            raise PhotoError(f"{label}: segmento JPEG no válido.")
        while position < len(data) and data[position] == 0xFF:
            position += 1
        if position >= len(data):
            break
        marker = data[position]
        position += 1
        if marker == 0xD9:
            if dimensions and has_scan and position == len(data):
                return dimensions
            raise PhotoError(f"{label}: cierre JPEG incompleto o bytes extraños al final.")
        if marker in {0, 0xD8, *range(0xD0, 0xD8)}:
            raise PhotoError(f"{label}: marcador JPEG fuera de lugar.")
        if marker == 0x01:
            continue
        if position + 2 > len(data):
            break
        length = struct.unpack_from(">H", data, position)[0]
        if length < 2 or position + length > len(data):
            break
        payload = data[position + 2:position + length]
        position += length
        if marker == 0xDB:
            table_position = 0
            while table_position < len(payload):
                descriptor = payload[table_position]
                precision, identity = descriptor >> 4, descriptor & 0x0F
                if precision not in (0, 1) or identity > 3:
                    raise PhotoError(f"{label}: tabla de cuantización JPEG no válida.")
                table_position += 1 + 64 * (precision + 1)
                if table_position > len(payload):
                    raise PhotoError(f"{label}: tabla de cuantización JPEG truncada.")
                has_quantization = True
        if marker == 0xC4:
            table_position = 0
            while table_position < len(payload):
                descriptor = payload[table_position]
                if descriptor >> 4 not in (0, 1) or descriptor & 0x0F > 3 or table_position + 17 > len(payload):
                    raise PhotoError(f"{label}: tabla Huffman JPEG no válida.")
                symbols = sum(payload[table_position + 1:table_position + 17])
                table_position += 17 + symbols
                if not 0 < symbols <= 256 or table_position > len(payload):
                    raise PhotoError(f"{label}: tabla Huffman JPEG truncada.")
                has_huffman = True
        if marker in sof:
            if marker not in (0xC0, 0xC1, 0xC2):
                raise PhotoError(f"{label}: variante JPEG no admitida; se requiere JPEG secuencial o progresivo Huffman.")
            if len(payload) < 6 or len(payload) != 6 + 3 * payload[5]:
                raise PhotoError(f"{label}: cabecera de dimensiones JPEG no válida.")
            height, width = struct.unpack_from(">HH", payload, 1)
            if not 0 < width <= 30000 or not 0 < height <= 30000 or width * height > 100000000:
                raise PhotoError(f"{label}: dimensiones JPEG fuera de los límites previstos.")
            if dimensions and dimensions != (width, height):
                raise PhotoError(f"{label}: dimensiones JPEG contradictorias.")
            dimensions = (width, height)
        if marker == 0xDA:
            if not dimensions or len(payload) < 6 or len(payload) != 4 + 2 * payload[0]:
                raise PhotoError(f"{label}: cabecera de escaneo JPEG no válida.")
            if not has_quantization or not has_huffman:
                raise PhotoError(f"{label}: faltan tablas JPEG para decodificar la imagen.")
            has_scan = True
            scan_data = False
            while position < len(data):
                next_marker = data.find(b"\xff", position)
                if next_marker != position:
                    scan_data = True
                if next_marker < 0:
                    position = len(data)
                    break
                position = next_marker
                next_byte = position + 1
                while next_byte < len(data) and data[next_byte] == 0xFF:
                    next_byte += 1
                if next_byte >= len(data):
                    position = len(data)
                    break
                if data[next_byte] == 0 or 0xD0 <= data[next_byte] <= 0xD7:
                    if data[next_byte] == 0:
                        scan_data = True
                    position = next_byte + 1
                else:
                    break
            if not scan_data:
                raise PhotoError(f"{label}: escaneo JPEG vacío; faltan los datos de la imagen.")
    raise PhotoError(f"{label}: JPEG truncado; falta un cierre de imagen válido.")


def read_resource(photo, originals):
    if originals is not None:
        path = originals / photo["filename"]
        if not path.is_file():
            raise PhotoError(f"Falta el original renombrado: {path}")
        with path.open("rb") as resource:
            return resource.read(MAX_BYTES + 1)
    request = Request(photo["url"], headers={
        "User-Agent": "Rapverse-photo-import/1.0",
        "Accept": "image/jpeg",
    })
    try:
        with urlopen(request, timeout=TIMEOUT) as response:
            content_type = response.headers.get_content_type()
            if content_type not in {"image/jpeg", "image/jpg", "application/octet-stream"}:
                raise PhotoError(f"{photo['filename']}: el servidor devolvió {content_type}, no JPEG.")
            return response.read(MAX_BYTES + 1)
    except HTTPError as error:
        if error.code == 403:
            domains = ", ".join(HOSTS)
            raise PhotoError(
                f"Descarga bloqueada (HTTP 403): {photo['url']}\n"
                f"Habilita el acceso de red a los cuatro dominios: {domains}.\n"
                "También puedes usar --from-directory con los 14 originales renombrados. "
                "No se han instalado fotografías ni modificado index.html."
            ) from error
        raise PhotoError(f"{photo['filename']}: HTTP {error.code} al descargar {photo['url']}.") from error
    except URLError as error:
        raise PhotoError(f"{photo['filename']}: no se pudo descargar la imagen: {error.reason}.") from error


def replace_block(document, name, content):
    start, end = block_markers(name)
    start_position = document.index(start) + len(start)
    end_position = document.index(end)
    return document[:start_position] + "\n" + content + "\n" + document[end_position:]


def image(photo, css_class="", eager=False):
    attributes = [
        f'src="assets/photos/{photo["filename"]}"',
        f'alt="{html.escape(photo["alt"], quote=True)}"',
        f'width="{photo["width"]}"',
        f'height="{photo["height"]}"',
    ]
    if css_class:
        attributes.append(f'class="{css_class}"')
    attributes.append('fetchpriority="high"' if eager else 'loading="lazy"')
    attributes.append('decoding="async"')
    return "<img " + " ".join(attributes) + " />"


def gallery_markup(by_name):
    lines = [
        '<section class="gallery-section container section" id="galeria" aria-labelledby="gallery-title">',
        '  <div class="section-heading">',
        '    <div><p class="eyebrow">04 / EN IMÁGENES</p><h2 id="gallery-title">EL ESTILO TAMBIÉN<br /><span class=\"outline\">ENTRA POR LOS OJOS.</span></h2></div>',
        '    <p class="section-description">Catorce encuadres para cambiar de perspectiva.<br />Del micrófono a la ropa, cada imagen<br />añade otra pista al recorrido.</p>',
        '  </div>',
        '  <div class="gallery-toolbar">',
        '    <div class="gallery-filters" role="group" aria-label="Filtrar fotografías por artista">',
        '      <button class="gallery-filter selected" type="button" data-gallery-filter="all" aria-pressed="true">Todas</button>',
        '      <button class="gallery-filter" type="button" data-gallery-filter="carti" aria-pressed="false">Playboi Carti</button>',
        '      <button class="gallery-filter" type="button" data-gallery-filter="cochise" aria-pressed="false">Cochise</button>',
        '    </div>',
        '    <span id="gallery-count" role="status" aria-live="polite">14 fotografías</span>',
        '  </div>',
        '  <div class="photo-grid">',
    ]
    for index, filename in enumerate(GALLERY_ORDER):
        photo = by_name[filename]
        artist = html.escape(ARTISTS[photo["artist"]])
        caption = html.escape(photo["caption"], quote=True)
        extra_class = " feature-photo" if index < 2 else ""
        lines.extend([
            f'    <figure class="photo-card{extra_class}" data-artist="{photo["artist"]}">',
            f'      <a class="photo-link" href="assets/photos/{filename}" data-artist="{photo["artist"]}" data-caption="{caption}" data-title="{artist}" aria-label="Ver fotografía: {html.escape(photo["alt"], quote=True)}">',
            "        " + image(photo),
            f'        <span class="photo-caption">{artist}<small>{caption}</small></span>',
            '        <span class="photo-open" aria-hidden="true">↗</span>',
            '      </a>',
            '    </figure>',
        ])
    lines.extend([
        '  </div>',
        '  <p class="gallery-note">El recorrido también se mira. Amplía las fotos y encuentra sus archivos de origen en <a href="assets/photos/SOURCES.md">el registro de imágenes</a>.</p>',
        '</section>',
        '<dialog id="photo-dialog" aria-labelledby="photo-dialog-title">',
        '  <div class="photo-dialog-top"><p class="eyebrow">EN IMÁGENES</p><button id="photo-close" type="button" aria-label="Cerrar fotografía">×</button></div>',
        '  <img id="photo-full" alt="" />',
        '  <div class="photo-dialog-bottom">',
        '    <div><h3 id="photo-dialog-title">Fotografía</h3><span id="photo-position" aria-live="polite"></span></div>',
        '    <div class="photo-navigation"><button id="photo-prev" type="button" aria-label="Fotografía anterior">←</button><button id="photo-next" type="button" aria-label="Fotografía siguiente">→</button></div>',
        '  </div>',
        '</dialog>',
    ])
    return "\n".join(lines)


def render_html(document, photos):
    check_template(document)
    by_name = {photo["filename"]: photo for photo in photos}
    hero = "\n".join([
        '<div class="hero-portraits">',
        "  <figure>" + image(by_name["carti-red-stage.jpg"], "hero-carti", eager=True) + "</figure>",
        "  <figure>" + image(by_name["cochise-feature.jpg"], "hero-cochise", eager=True) + "</figure>",
        '</div>',
    ])
    document = replace_block(document, "hero", hero)
    document = replace_block(document, "carti", image(by_name["carti-beanie.jpg"]))
    document = replace_block(document, "cochise", image(by_name["cochise-trench.jpg"]))
    document = replace_block(document, "gallery", gallery_markup(by_name))
    license_note = (
        '<p>Catorce imágenes acompañan este recorrido, del escenario al retrato. '
        'Encontrarás sus archivos de origen en <a href="assets/photos/SOURCES.md">el registro de imágenes</a> '
        'junto a las versiones originales. '
        'Las ilustraciones y composiciones propias de Rapverse '
        'se conservan en el proyecto.</p>'
    )
    document = replace_block(document, "license", license_note)

    def add_visual_class(match):
        classes = match.group(1).split()
        if "artist-visual" in classes and any(f"{artist}-visual" in classes for artist in ARTISTS):
            if "photo-visual" not in classes:
                classes.append("photo-visual")
            return 'class="' + " ".join(classes) + '"'
        return match.group(0)

    document = re.sub(r'class="([^"]*)"', add_visual_class, document)
    document = document.replace("ILUSTRACIÓN ORIGINAL", "SERIE FOTOGRÁFICA")
    navigation = re.search(r'<nav\b[^>]*\bid="navigation"[^>]*>(.*?)</nav>', document, re.S)
    if not re.search(r'href=[\"\']#galeria[\"\']', navigation.group(1)):
        document = document.replace(
            "<!-- photos:navigation -->",
            '<!-- photos:navigation -->\n          <a class="nav-link" href="#galeria">En imágenes</a>',
            1,
        )
    return document.replace("04 / DETRÁS DEL CONTENIDO", "05 / DETRÁS DEL CONTENIDO")


def render_sources(photos, imported_at, originals):
    local = originals is not None
    lines = [
        "# Procedencia de las fotografías de Rapverse", "",
        "Selección de 14 fotografías aportadas por el usuario; las URL de procedencia se conservan en `tools/photos.json`.",
        "No se conoce una licencia de uso confirmada para estas imágenes. No se atribuyen licencias ni autorías no verificadas.", "",
        f"Fecha de importación (UTC): {imported_at}.",
        "Método: originales locales renombrados; el script no descargó los recursos." if local else "Método: descarga HTTPS desde las URL del manifiesto.",
        "Las dimensiones y SHA-256 siguientes corresponden a los bytes JPEG instalados.",
        "Las fotografías de baja resolución se ampliaron con `tools/enhance-photos.py` (reducción de ruido, x2 y nitidez moderada, sin añadir ni quitar elementos); los archivos tal como se aportaron se conservan en `assets/photos/originals/`.", "",
    ]
    for filename in GALLERY_ORDER:
        photo = next(photo for photo in photos if photo["filename"] == filename)
        upload_lines = (
            [f"- Archivo original aportado en `imagenes.zip`: `{photo['uploaded_filename']}`"]
            if local and photo.get("uploaded_filename") else []
        )
        lines.extend([
            f"## {filename}", "",
            f"- Artista: {ARTISTS[photo['artist']]}",
            f"- Descripción: {photo['alt']}",
            f"- Pie: {photo['caption']}",
            *upload_lines,
            f"- Origen indicado: {photo['source']}",
            f"- URL proporcionada: {photo['url']}",
            f"- Dominio de origen: {urlsplit(photo['url']).hostname}",
            "- Fecha de descarga: no verificada; archivo aportado localmente." if local else f"- Fecha de descarga (UTC): {photo['retrieved_at']}",
            f"- Archivo local: `assets/photos/{filename}`",
            f"- Dimensiones JPEG: {photo['width']} × {photo['height']} px",
            f"- Tamaño: {photo['bytes']} bytes",
            f"- SHA-256: `{photo['sha256']}`", "",
        ])
    return "\n".join(lines)


def install(root, staging, photos, original_index):
    """Instala con sustituciones atómicas por archivo y deshace errores."""
    if digest((root / "index.html").read_bytes()) != digest(original_index):
        raise PhotoError("index.html cambió durante la importación; vuelve a ejecutar el script.")
    check_destinations(root, photos)
    relative_paths = [f"assets/photos/{photo['filename']}" for photo in photos]
    relative_paths.extend(["assets/photos/SOURCES.md", "index.html"])
    backup = staging / "backup"
    existed = set()
    for relative in relative_paths:
        target = root / relative
        if target.exists():
            copy = backup / relative
            copy.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(target, copy)
            existed.add(relative)
    created_directories = []
    touched = []
    try:
        for directory in (root / "assets", root / "assets/photos"):
            if not directory.exists():
                directory.mkdir()
                created_directories.append(directory)
        for relative in relative_paths:
            touched.append(relative)
            os.replace(staging / "ready" / relative, root / relative)
    except (OSError, KeyboardInterrupt) as error:
        rollback_errors = []
        for relative in reversed(touched):
            try:
                if relative in existed:
                    os.replace(backup / relative, root / relative)
                else:
                    (root / relative).unlink(missing_ok=True)
            except OSError as rollback_error:
                rollback_errors.append(str(rollback_error))
        for directory in reversed(created_directories):
            try:
                directory.rmdir()
            except OSError as rollback_error:
                rollback_errors.append(str(rollback_error))
        if rollback_errors:
            # main conserva el directorio con las copias para recuperación manual.
            (staging / "KEEP_BACKUP").touch()
            raise PhotoError(
                f"Falló la instalación y no se completó la restauración. Copias: {backup}\n"
                + "\n".join(rollback_errors)
            ) from error
        raise PhotoError(f"La instalación falló y se restauraron los archivos originales: {error}") from error


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--from-directory", type=Path, help="Carpeta con los 14 JPEG renombrados según tools/photos.json.")
    parser.add_argument("--dry-run", action="store_true", help="Valida y muestra el plan sin escribir ni descargar.")
    arguments = parser.parse_args(argv)
    staging = None
    try:
        photos = load_manifest(ROOT)
        check_destinations(ROOT, photos)
        original_index = (ROOT / "index.html").read_bytes()
        document = original_index.decode("utf-8")
        check_template(document)
        originals = arguments.from_directory
        if originals is not None:
            originals = originals.expanduser().resolve()
            if not originals.is_dir():
                raise PhotoError(f"La carpeta de originales no existe: {originals}")
            missing = [photo["filename"] for photo in photos if not (originals / photo["filename"]).is_file()]
            if missing:
                raise PhotoError("Faltan originales renombrados: " + ", ".join(missing))
        if arguments.dry_run and originals is None:
            render_html(document, photos)
            print("Validación correcta: 14 URL, marcadores HTML y destinos preparados.")
            print("Plan: descargar y validar 14 JPEG; instalar assets/photos y actualizar index.html.")
            print("Simulación: no se ha escrito ningún archivo ni accedido a la red.")
            return 0
        if not arguments.dry_run:
            staging = Path(tempfile.mkdtemp(prefix=".rapverse-photo-import-", dir=ROOT))
            (staging / "ready/assets/photos").mkdir(parents=True)
        for photo in photos:
            data = read_resource(photo, originals)
            photo["width"], photo["height"] = jpeg_dimensions(data, photo["filename"])
            photo["bytes"] = len(data)
            photo["sha256"] = digest(data)
            photo["retrieved_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
            if staging is not None:
                staged_file = staging / "ready/assets/photos" / photo["filename"]
                staged_file.write_bytes(data)
                staged_file.chmod(0o644)
            print(f"Validado {photo['filename']}: {photo['width']} × {photo['height']} px, {len(data)} bytes.")
        updated_document = render_html(document, photos)
        if arguments.dry_run:
            print("Simulación correcta: 14 JPEG y HTML validados; ningún archivo modificado.")
            return 0
        imported_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
        (staging / "ready/assets/photos/SOURCES.md").write_text(
            render_sources(photos, imported_at, originals), encoding="utf-8"
        )
        staged_index = staging / "ready/index.html"
        staged_index.write_text(updated_document, encoding="utf-8")
        staged_index.chmod((ROOT / "index.html").stat().st_mode & 0o777)
        install(ROOT, staging, photos, original_index)
        print("Importación completa: 14 fotografías, galería, retratos y registro de procedencia instalados.")
        return 0
    except (PhotoError, OSError, UnicodeError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Importación cancelada antes de completar la instalación.", file=sys.stderr)
        return 130
    finally:
        if staging is not None and not (staging / "KEEP_BACKUP").exists():
            shutil.rmtree(staging)


if __name__ == "__main__":
    raise SystemExit(main())
