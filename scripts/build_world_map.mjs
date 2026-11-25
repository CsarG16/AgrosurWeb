// Genera templates/landing/_world_map.svg: mapa mundial de puntos con los mercados de exportación.
// Uso: npm run build:map   (solo hace falta volver a correrlo si cambian los mercados o el estilo)
//
// Datos: world-atlas (Natural Earth 110m, dominio público). El SVG resultante no necesita
// ninguna librería en el navegador.
import { readFileSync, writeFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { feature } from 'topojson-client';
import { geoContains } from 'd3-geo';

const require = createRequire(import.meta.url);
const topo = JSON.parse(readFileSync(require.resolve('world-atlas/countries-110m.json'), 'utf8'));
const countries = feature(topo, topo.objects.countries).features;

// Recorte del mapa (sin la Antártida) y tamaño del lienzo
const LAT_TOP = 76;
const LAT_BOTTOM = -56;
const WIDTH = 1000;
const HEIGHT = Math.round((WIDTH * (LAT_TOP - LAT_BOTTOM)) / 360);
const STEP = 2.4; // grados entre puntos

const x = (lon) => ((lon + 180) / 360) * WIDTH;
const y = (lat) => ((LAT_TOP - lat) / (LAT_TOP - LAT_BOTTOM)) * HEIGHT;
const r1 = (n) => Math.round(n * 10) / 10;

// Mercados (códigos ISO 3166-1 numéricos)
const EUROPE = ['040', '056', '100', '191', '196', '203', '208', '233', '246', '250', '276', '300', '348', '372', '380',
  '428', '440', '442', '470', '528', '616', '620', '642', '703', '705', '724', '752', '826', '578', '756'];
const MARKETS = {
  usa: { ids: ['840'], target: [-98, 39] },
  europe: { ids: EUROPE, target: [10, 50], lonMin: -30 }, // sin la Guayana Francesa
  asia: { ids: ['156', '392', '410', '158'], target: [116, 35] },
  saudi: { ids: ['682'], target: [45, 24] },
};
const PERU = { ids: ['604'], target: [-75, -10] };

const byId = (ids) => countries.filter((c) => ids.includes(String(c.id)));
const groups = Object.fromEntries(Object.entries(MARKETS).map(([k, m]) => [k, byId(m.ids)]));
const peru = byId(PERU.ids);

const dots = { land: [], market: [], peru: [] };
for (let lat = LAT_TOP - STEP / 2; lat > LAT_BOTTOM; lat -= STEP) {
  for (let lon = -180 + STEP / 2; lon < 180; lon += STEP) {
    const p = [lon, lat];
    if (!countries.some((c) => geoContains(c, p))) continue;
    const pt = `M${r1(x(lon))} ${r1(y(lat))}h0`;
    if (peru.some((c) => geoContains(c, p))) { dots.peru.push(pt); continue; }
    const inMarket = Object.entries(groups).some(([k, cs]) =>
      (MARKETS[k].lonMin === undefined || lon >= MARKETS[k].lonMin) && cs.some((c) => geoContains(c, p)));
    (inMarket ? dots.market : dots.land).push(pt);
  }
}

// Rutas: curva cuadrática desde Perú, con el punto de control elevado hacia el norte
const [px, py] = [x(PERU.target[0]), y(PERU.target[1])];
const routes = Object.entries(MARKETS).map(([k, m], i) => {
  const [tx, ty] = [x(m.target[0]), y(m.target[1])];
  const dist = Math.hypot(tx - px, ty - py);
  const cx = (px + tx) / 2;
  const cy = Math.min(py, ty) - dist * 0.28;
  return { k, i, d: `M${r1(px)} ${r1(py)}Q${r1(cx)} ${r1(cy)} ${r1(tx)} ${r1(ty)}`, tx: r1(tx), ty: r1(ty) };
});

const svg = `<svg class="world-map w-full h-auto" viewBox="0 0 ${WIDTH} ${HEIGHT}" role="img" aria-label="Mapa de exportaciones de Agro Sur Latino desde Perú a EE. UU., Europa, Asia y Arabia Saudí" xmlns="http://www.w3.org/2000/svg">
  <!-- Generado por scripts/build_world_map.mjs (Natural Earth 110m vía world-atlas). No editar a mano. -->
  <path class="wm-land" d="${dots.land.join('')}"/>
  <path class="wm-market" d="${dots.market.join('')}"/>
  <path class="wm-peru" d="${dots.peru.join('')}"/>
${routes.map((r) => `  <path class="wm-route" style="--i:${r.i}" pathLength="1" d="${r.d}"/>`).join('\n')}
${routes.map((r) => `  <circle class="wm-pin" style="--i:${r.i}" cx="${r.tx}" cy="${r.ty}" r="5"/>`).join('\n')}
  <circle class="wm-origin" cx="${r1(px)}" cy="${r1(py)}" r="6"/>
</svg>
`;

writeFileSync(new URL('../templates/landing/_world_map.svg', import.meta.url), svg);
console.log(`_world_map.svg: ${dots.land.length + dots.market.length + dots.peru.length} puntos, ${(svg.length / 1024).toFixed(1)} KB`);
