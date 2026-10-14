#!/usr/bin/env python3
"""Mejora las fotografías de baja resolución sin alterar su contenido.

    python3 tools/enhance-photos.py            # lee assets/photos/originals
    python3 tools/enhance-photos.py --dry-run  # sólo muestra el plan

Pasos para cada JPEG pequeño: reducción suave del ruido y de los bloques de
compresión, ampliación x2 (bicúbica), nitidez moderada y un dither mínimo
contra el banding. No añade, elimina ni recompone elementos de la imagen. Los originales
se conservan en assets/photos/originals/ y las versiones mejoradas sustituyen
a las de assets/photos/. Requiere opencv-python y numpy (sólo para este paso;
la web no los necesita).
"""
import argparse
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
PHOTOS = ROOT / "assets/photos"
ORIGINALS = PHOTOS / "originals"
SMALL_SIDE = 900      # por debajo de este lado menor se amplía x2
LARGE_SIDE = 2048     # las fotos grandes sólo se recomprimen
QUALITY = 88


def enhance_small(image):
    # 1) Quita bloques y ruido JPEG sin borrar rasgos.
    clean = cv2.fastNlMeansDenoisingColored(image, None, 5, 5, 7, 21)
    # 2) Suaviza el escalonado de la compresión en zonas lisas conservando bordes.
    clean = cv2.bilateralFilter(clean, 5, 22, 5)
    height, width = clean.shape[:2]
    big = cv2.resize(clean, (width * 2, height * 2), interpolation=cv2.INTER_CUBIC)
    # 3) Nitidez moderada con radio pequeño.
    blur = cv2.GaussianBlur(big, (0, 0), 1.6)
    sharp = cv2.addWeighted(big, 1.45, blur, -0.45, 0)
    # 4) Dither casi imperceptible: evita bandas en degradados ampliados.
    rng = np.random.default_rng(7)
    noise = rng.normal(0, 1.6, sharp.shape[:2]).astype(np.float32)[..., None]
    return np.clip(sharp.astype(np.float32) + noise, 0, 255).astype(np.uint8)


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    for source in sorted(ORIGINALS.glob("*.jpg")):
        image = cv2.imread(str(source), cv2.IMREAD_COLOR)
        if image is None:
            raise SystemExit(f"No se pudo leer {source}")
        height, width = image.shape[:2]
        small = min(height, width) < SMALL_SIDE
        plan = "ampliar x2 + nitidez" if small else "recomprimir"
        print(f"{source.name}: {width}x{height} -> {plan}")
        if args.dry_run:
            continue
        result = enhance_small(image) if small else image
        longest = max(result.shape[:2])
        if longest > LARGE_SIDE:
            scale = LARGE_SIDE / longest
            result = cv2.resize(result, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        ok, buffer = cv2.imencode(".jpg", result, [
            cv2.IMWRITE_JPEG_QUALITY, QUALITY, cv2.IMWRITE_JPEG_PROGRESSIVE, 1,
            cv2.IMWRITE_JPEG_OPTIMIZE, 1])
        if not ok:
            raise SystemExit(f"No se pudo codificar {source.name}")
        (PHOTOS / source.name).write_bytes(buffer.tobytes())


if __name__ == "__main__":
    main()
