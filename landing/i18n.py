"""Traducción ES -> EN de las páginas /en/ en el servidor.

El diccionario vive en landing/i18n.json (única fuente):
- "translations": textos con clave, en elementos con data-i18n="clave".
- "phraseEN": frases sin clave (texto exacto en español -> inglés), en texto y en
  atributos placeholder / aria-label / title / alt.
Además, los elementos con data-en="..." (nombres desde la base de datos) se envían con ese texto.

main.js usa el mismo diccionario (lo recibe en <script id="i18n-data">) para lo que se pinta
después en el navegador (modal de producto, resumen del cotizador, etc.).
"""
import html
import json
import re
from functools import lru_cache
from pathlib import Path

I18N_FILE = Path(__file__).resolve().parent / 'i18n.json'
ATTRS = ('placeholder', 'aria-label', 'title', 'alt')


@lru_cache(maxsize=1)
def load():
    with open(I18N_FILE, encoding='utf-8') as fh:
        return json.load(fh)


def _norm(text):
    return re.sub(r'\s+', ' ', text).strip()


@lru_cache(maxsize=1)
def _phrases():
    """{texto ES normalizado: texto EN}, con y sin escape HTML (el HTML puede traer &amp; etc.)."""
    phrases = {}
    for es, en in load()['phraseEN'].items():
        phrases[_norm(es)] = en
        phrases[_norm(html.escape(es, quote=False))] = en
    return phrases


# <tag ... data-i18n="clave" ...>contenido</tag>
_I18N_EL = re.compile(r'<(?P<tag>[a-zA-Z0-9]+)(?P<attrs>[^>]*?\sdata-i18n="(?P<key>[\w-]+)"[^>]*)>(?P<inner>.*?)</(?P=tag)>', re.S)
# <tag ... data-en="Texto EN" ...>texto ES</tag>  (sin etiquetas dentro)
_DATA_EN_EL = re.compile(r'<(?P<tag>[a-zA-Z0-9]+)(?P<attrs>[^>]*?\sdata-en="(?P<en>[^"]*)"[^>]*)>(?P<inner>[^<]*)</(?P=tag)>')
# texto entre etiquetas
_TEXT_NODE = re.compile(r'>(?P<text>[^<>]+)<')
_ATTR = re.compile(r'\s(?P<name>' + '|'.join(re.escape(a) for a in ATTRS) + r')="(?P<value>[^"]*)"')
# <option data-en-text="...">texto ES</option>
_DATA_EN_TEXT_EL = re.compile(r'<(?P<tag>[a-zA-Z0-9]+)(?P<attrs>[^>]*?\sdata-en-text="(?P<en>[^"]*)"[^>]*)>(?P<inner>[^<]*)</(?P=tag)>')
# etiquetas con data-alt-en / data-label-en: el alt / aria-label en inglés ya viene en la plantilla
_OPEN_TAG = re.compile(r'<[a-zA-Z0-9]+\s[^>]*\sdata-(?:alt|label)-en="[^"]*"[^>]*>')
_SKIP_BLOCKS = re.compile(r'(<script\b.*?</script>|<style\b.*?</style>)', re.S | re.I)


def _keep_spacing(original, new):
    lead = original[:len(original) - len(original.lstrip())]
    trail = original[len(original.rstrip()):]
    return f'{lead}{new}{trail}'


def translate_html(page):
    """Devuelve el HTML con los textos ya en inglés (no toca <script> ni <style>)."""
    en = load()['translations'].get('en', {})
    phrases = _phrases()

    def i18n_element(m):
        value = en.get(m.group('key'))
        if not value:
            return m.group(0)
        inner = m.group('inner')
        # los valores con etiquetas (<strong>) se insertan tal cual; el resto se escapa
        text = value if '<' in value else html.escape(value, quote=False)
        return f"<{m.group('tag')}{m.group('attrs')}>{_keep_spacing(inner, text)}</{m.group('tag')}>"

    def data_en_element(m):
        if not m.group('en'):
            return m.group(0)
        return f"<{m.group('tag')}{m.group('attrs')}>{_keep_spacing(m.group('inner'), m.group('en'))}</{m.group('tag')}>"

    def data_en_text_element(m):
        return f"<{m.group('tag')}{m.group('attrs')}>{_keep_spacing(m.group('inner'), m.group('en'))}</{m.group('tag')}>"

    def open_tag(m):
        tag = m.group(0)
        for src, dest in (('data-alt-en', 'alt'), ('data-label-en', 'aria-label')):
            value = re.search(rf'\s{src}="([^"]*)"', tag)
            if value:
                tag = re.sub(rf'(\s{dest}=)"[^"]*"', lambda mm: f'{mm.group(1)}"{value.group(1)}"', tag, count=1)
        return tag

    def text_node(m):
        text = m.group('text')
        new = phrases.get(_norm(text))
        return f'>{_keep_spacing(text, html.escape(new, quote=False))}<' if new else m.group(0)

    def attr(m):
        new = phrases.get(_norm(m.group('value')))
        return f' {m.group("name")}="{html.escape(new)}"' if new else m.group(0)

    def translate_chunk(chunk):
        chunk = _I18N_EL.sub(i18n_element, chunk)
        chunk = _DATA_EN_EL.sub(data_en_element, chunk)
        chunk = _DATA_EN_TEXT_EL.sub(data_en_text_element, chunk)
        chunk = _OPEN_TAG.sub(open_tag, chunk)
        chunk = _TEXT_NODE.sub(text_node, chunk)
        return _ATTR.sub(attr, chunk)

    parts = _SKIP_BLOCKS.split(page)
    return ''.join(part if i % 2 else translate_chunk(part) for i, part in enumerate(parts))
