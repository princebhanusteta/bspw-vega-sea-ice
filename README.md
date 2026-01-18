# BSPW Vega Visualization — Arctic Sea-Ice Edge (2000–2024)

This repository contains an interactive **Vega (not Vega-Lite)** visualization comparing **Arctic sea-ice extent edges** for:

- **March** (typical winter maximum)
- **September** (typical summer minimum)

Across **2000–2024**, with:
- a **year slider**
- an optional **animation toggle**
- a fixed **baseline year (2000)** for comparison

The visualization is implemented as a Vega JSON spec and loads a **processed GeoJSON** from this repository.

---

## Quick links

- **Vega Editor:** https://vega.github.io/editor/
- **Data sources & processing notes:** [DATASOURCES.md](DATASOURCES.md)
- **Visualization iteration log:** [viz/log-visualization.md](viz/log-visualization.md)
- **Vega spec:** [viz/arctic_sea_ice_march_vs_september.vg.json](viz/arctic_sea_ice_march_vs_september.vg.json)

---

## How to view the visualization

### Option A (recommended): Vega Editor (fastest)
1. Open the Vega Editor: https://vega.github.io/editor/
2. Click **Open** → **File** (or paste the spec contents into the editor).
3. Ensure the spec uses **RAW GitHub URLs** for data (not `blob/` links).

Processed dataset in this repo should be referenced like this:

- `https://raw.githubusercontent.com/princebhanusteta/bspw-vega-sea-ice/main/data/processed/arctic_sea_ice_extent_2000_2024.geojson`

Make sure to not use GitHub `blob/` URL, Vega will not load the JSON correctly.

### Option B: View locally (useful for debugging)
From the repository root:
```bash
python3 -m http.server 8000
