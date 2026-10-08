# The Real Arrival — final desktop edition

Open `the_real_arrival_final.html` directly in a desktop browser. The HTML embeds Leaflet, restaurant records and all displayed basemap geometry. No server, live tiles, runtime API or internet connection is required. Designed for desktop widths of 1180px and above.

## Data and visual treatment

OpenStreetMap contributors / ODbL: https://www.openstreetmap.org/copyright . Downloaded through https://overpass.private.coffee/api/interpreter on 2026-10-08; the exact OSM snapshot timestamp is recorded in `data/basemap-audit.json`. The reproducible query is `data/basemap-query.overpass`; the original response is `data/osm-source.json`; the displayed features are `data/basemap.geojson`.

Factual geometry: 20,567 road ways; 2,258 mapped green-space polygons; 340 water polygons; 4,358 building footprints in the core; 1,598 mapped residential/commercial areas. Main campus outlines are Peking University way 1330709889 (https://www.openstreetmap.org/way/1330709889) and Tsinghua University relation 7469216 (https://www.openstreetmap.org/relation/7469216). Relation outer member segments are joined by their original matching endpoints. No road, campus or vegetation shape is hand-drawn; original vertices are retained. OSM coverage is incomplete and is not an official cadastral survey.

Graphic abstraction: line weights, pale colors, footprint opacity, fixed-size restaurant glyphs and English labels. Road styles group motorway/trunk as arterial, primary as major, secondary/tertiary as secondary, other vehicular streets as local, and local/internal ways lying within the two campus outlines as campus/internal. General footpaths outside campuses are omitted. Buildings are intentionally limited to the Wudaokou/university core.

## Destination and coordinate transparency

V15 uses Huaqing Jiayuan, not Qingnianhui Jiayuan / Chaoyang North Road 106. Its reference coordinates 39.992347, 116.333755 are verified against Amap's Huaqing Business Club (Huaqing Jiayuan): https://www.amap.com/place/B000A835NS . These are GCJ-02 coordinates and cannot be placed directly over WGS84 OSM. An iterative GCJ-02 inversion yields approximately 39.991033029, 116.327611541 in WGS84; the result is consistent with the OSM Huaqing Jiayuan community polygon https://www.openstreetmap.org/way/473654608 . Provenance is saved in `data/delivery-point.json`.

This is a community reference inherited from V15, not independently documented proof of the exact doorstep used to collect this dataset. The original CSV does not declare its coordinate system. Restaurant coordinates are retained without speculative conversion; point-to-road alignment is therefore unverified. The page and methodology disclose this limitation.

## Quality and interactions

CSV bytes are unchanged. V15 category colors, 2–4 stage quality models, single-stage Sushi/Fresh and ETA-fixed glyph state logic are retained. Thresholds remain illustrative prototype proxies, not locally calibrated measurements or food-safety conclusions. Name-based categories can be uncertain or mixed-menu.

The two brush clips select a continuous stage range; dragging is continuous and release snaps to stage boundaries. The brush only filters visibility. Initial active layers match V15; their initial range now includes all stages so the distribution is visible at first open. FOOD / DRINKS / DESSERT toggles, category expansion, black restaurant strip, English/Latin display labels and card-to-map focus are retained. Incomplete historical labels are replaced by conservative Latin transliteration; source names remain in the underlying records and unchanged CSV. Display names are not asserted as official English trading names.

CORE restores the university/Wudaokou framing. STUDY zooms to the widest allowed study frame; distant dataset points remain reachable by bounded panning. The minimum zoom adapts to the viewport so the map cannot reveal an empty exterior; maximum zoom is 15.75. Map navigation does not change stage filters. The full result strip includes every matching restaurant, supports horizontal scrolling and keyboard activation, and explains empty selections.

## Verification

Chrome loaded the actual final file via `file://`, with zero page/console errors and zero network requests. Tested layer toggling, stages 2+3 and 1+2+3, unchanged glyph states after brushing, matching marker/result counts, zoom limits, pointer map dragging, pan bounds, card popup/focus, empty state and 1512×982 / 1280×800 desktop widths. Evidence: `docs/final-desktop.png`, `docs/verification.md`; runnable check: `scripts/verify.cjs` (requires locally installed Playwright and Chrome). Build source: `scripts/build.py`.

Leaflet 1.9.4, copyright Vladimir Agafonkin and contributors, BSD-2-Clause: https://github.com/Leaflet/Leaflet/blob/v1.9.4/LICENSE . Vendor files and notices are included.

## Visual hierarchy update
Basemap contrast is deliberately reduced so factual geography remains contextual: buildings and local roads are faint, major roads remain legible, green space and campus extents remain readable, and restaurant glyphs are enlarged. The redundant map legend is hidden because the right-side quality layers already explain the glyph states.
