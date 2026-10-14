#!/usr/bin/env python3
"""Serve Rapverse locally with HTTP byte ranges for audio seeking."""
from argparse import ArgumentParser
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


class RangeRequestHandler(SimpleHTTPRequestHandler):
    def send_head(self):
        # Production static hosts support byte ranges. Python's default handler
        # does not, and Chromium otherwise reports MP3 seekable ranges as [0, 0].
        self.byte_range = None
        requested_range = self.headers.get('Range')
        path = Path(self.translate_path(self.path))
        if not requested_range or not path.is_file():
            return super().send_head()
        match = re.fullmatch(r'bytes=(\d*)-(\d*)', requested_range.strip())
        size = path.stat().st_size
        if not match or not any(match.groups()) or not size:
            self.send_error(416, 'Unsupported byte range')
            return None
        first, last = match.groups()
        start = int(first) if first else max(0, size - int(last))
        end = min(int(last), size - 1) if first and last else size - 1
        if start >= size or start > end:
            self.send_error(416, 'Byte range outside resource')
            return None
        source = path.open('rb')
        self.send_response(206)
        self.send_header('Content-Type', self.guess_type(str(path)))
        self.send_header('Content-Length', str(end - start + 1))
        self.send_header('Accept-Ranges', 'bytes')
        self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
        self.send_header('Last-Modified', self.date_time_string(path.stat().st_mtime))
        self.end_headers()
        self.byte_range = (start, end)
        source.seek(start)
        return source

    def copyfile(self, source, outputfile):
        if self.byte_range is None:
            return super().copyfile(source, outputfile)
        remaining = self.byte_range[1] - self.byte_range[0] + 1
        while remaining:
            block = source.read(min(65536, remaining))
            if not block:
                break
            outputfile.write(block)
            remaining -= len(block)


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8000)
    parser.add_argument('--bind', default='127.0.0.1')
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.bind, args.port), partial(RangeRequestHandler, directory=str(ROOT)))
    print(f'Rapverse: http://{args.bind}:{server.server_port}', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
