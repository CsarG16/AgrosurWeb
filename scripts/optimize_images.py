"""Optimiza las imágenes del sitio: convierte PNG/JPG pesados a WebP.

Uso (desde la raíz del proyecto, con Pillow instalado):

    python scripts/optimize_images.py                 # convierte static/images/products y company
    python scripts/optimize_images.py --delete        # ídem y borra los originales PNG/JPG convertidos
    python scripts/optimize_images.py --convert ORIGEN.png static/images/products/kiwicha.webp

Objetivo: 80–150 KB por foto, sin pérdida visible a los tamaños en que se muestran.
"""
import argparse
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
IMAGES = ROOT / 'static' / 'images'

# carpeta -> (ancho máximo en px, calidad WebP)
SETTINGS = {
    'products': (900, 78),   # tarjeta ~400 px y modal ~340 px; 900 cubre pantallas retina
    'company': (1400, 76),   # fotos grandes (hero, fachada, almacén, campo)
}
SOURCE_SUFFIXES = {'.png', '.jpg', '.jpeg'}


def convert(src: Path, dest: Path, max_width: int, quality: int) -> int:
    """Convierte `src` a WebP en `dest` y devuelve el peso final en bytes."""
    with Image.open(src) as im:
        im.load()
        if im.mode not in ('RGB', 'RGBA'):
            im = im.convert('RGB')
        if im.width > max_width:
            height = round(im.height * max_width / im.width)
            im = im.resize((max_width, height), Image.LANCZOS)
        dest.parent.mkdir(parents=True, exist_ok=True)
        im.save(dest, 'WEBP', quality=quality, method=6)
    return dest.stat().st_size


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--delete', action='store_true', help='borrar el PNG/JPG original tras convertirlo')
    parser.add_argument('--convert', nargs=2, metavar=('ORIGEN', 'DESTINO.webp'), help='convertir un archivo suelto')
    args = parser.parse_args()

    if args.convert:
        src, dest = Path(args.convert[0]), Path(args.convert[1])
        size = convert(src, dest, *SETTINGS['products'])
        print(f'{dest}: {size / 1024:.0f} KB')
        return 0

    total_before = total_after = 0
    for folder, (max_width, quality) in SETTINGS.items():
        for src in sorted((IMAGES / folder).iterdir()):
            if src.suffix.lower() not in SOURCE_SUFFIXES:
                continue
            dest = src.with_suffix('.webp')
            before = src.stat().st_size
            after = convert(src, dest, max_width, quality)
            total_before += before
            total_after += after
            print(f'{src.relative_to(ROOT)}: {before / 1024:.0f} KB -> {dest.name} {after / 1024:.0f} KB')
            if args.delete:
                src.unlink()
    print(f'TOTAL: {total_before / 1024 / 1024:.1f} MB -> {total_after / 1024 / 1024:.1f} MB')
    return 0


if __name__ == '__main__':
    sys.exit(main())
