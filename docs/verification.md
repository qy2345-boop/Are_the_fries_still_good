# Final verification, 2026-10-08

Actual Chrome browser, offline `file://` load:
- 29,123 embedded features including both factual campus outlines.
- 208 initial filtered markers and 208 matching result cards.
- Hot Meals toggle: marker count 208 → 112.
- Fried/Burger range [1,3): stages 2+3; range [0,3): stages 1+2+3.
- ETA-derived glyph state array identical before/after brush.
- Free input accepted before release; commit snapped to stage boundaries.
- Zoom clamped to viewport-derived minimum 13.25 and maximum 15.75 at 1512×982.
- Actual pointer drag exercised; subsequent forced exterior pan clamped inside study bounds.
- Clicking a restaurant card opened its corresponding map popup.
- No active categories: zero markers and explanatory empty-result text.
- Desktop widths 1512 and 1280: body width matched viewport width.
- Zero page/console errors, zero network requests.
- Screenshot visually inspected: black shell/strip, off-white geometry map, pale green land cover, five road styles, solid university outlines, colored glyphs, black/white delivery target.

Limitations are disclosed in README and the page: unknown restaurant source CRS, no exact collection doorstep documentation, incomplete OSM coverage, illustrative quality thresholds.
