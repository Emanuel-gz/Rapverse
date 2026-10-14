#!/usr/bin/env python3
"""Validate local references and package Rapverse without Git or test caches."""

from argparse import ArgumentParser
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit
from zipfile import ZIP_DEFLATED, ZipFile
import re

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {'.git', '.venv', '__pycache__', 'node_modules', 'test-results'}


class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = []

    def handle_starttag(self, _tag, attrs):
        self.paths.extend(value for key, value in attrs
                          if key in ('href', 'src') and value)


def validate_references():
    document = References()
    document.feed((ROOT / 'index.html').read_text(encoding='utf-8'))
    paths = document.paths
    paths.extend(re.findall(r'url\([\s\'"]*([^\)\'"\s]+)',
                            (ROOT / 'styles.css').read_text(encoding='utf-8')))
    for value in paths:
        url = urlsplit(value)
        if url.scheme or url.netloc or not url.path:
            continue
        target = (ROOT / unquote(url.path)).resolve()
        if not target.is_relative_to(ROOT) or not target.is_file():
            raise ValueError(f'Recurso local ausente o fuera del proyecto: {value}')


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT.parent / 'Rapverse-mejorado.zip')
    parser.add_argument('--extras-archive', type=Path,
                        help='Conservar también los materiales fuera de Rapverse del ZIP original.')
    args = parser.parse_args()
    output = args.output.resolve()
    validate_references()
    files = [path for path in sorted(ROOT.rglob('*')) if path.is_file()
             and not EXCLUDED.intersection(path.relative_to(ROOT).parts)
             and path.name != '.DS_Store' and path.suffix != '.pyc'
             and path.resolve() != output]
    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, 'w', ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            archive.write(path, 'Rapverse/' + path.relative_to(ROOT).as_posix())
        if args.extras_archive:
            with ZipFile(args.extras_archive) as original:
                for entry in original.infolist():
                    parts = PurePosixPath(entry.filename).parts
                    if not parts or parts[0] == 'Rapverse':
                        continue
                    if entry.filename.startswith('/') or '..' in parts or '.git' in parts:
                        raise ValueError(f'Ruta no válida en materiales originales: {entry.filename}')
                    archive.writestr(entry, original.read(entry))
    with ZipFile(output) as archive:
        if archive.testzip():
            raise ValueError('La comprobación de integridad del ZIP falló.')
        expected = {'Rapverse/' + path.relative_to(ROOT).as_posix() for path in files}
        if not expected.issubset(set(archive.namelist())):
            raise ValueError('El ZIP omite archivos del proyecto.')
    print(f'ZIP verificado: {output} ({len(files)} archivos del proyecto).')


if __name__ == '__main__':
    main()
