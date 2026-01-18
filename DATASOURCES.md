# Data Sources & Processing Notes — Arctic Sea-Ice Edge Visualization (2000–2024)

This document describes the datasets used for the Vega visualization (March vs September Arctic sea-ice extent edges), including provenance, processing decisions, and key limitations.

## Quick links (inside this repo)

- **Final Vega spec (interactive):** [`viz/arctic_sea_ice_march_vs_september.vg.json`](viz/arctic_sea_ice_march_vs_september.vg.json)
- **Visualization iteration log:** [`viz/log-visualization.md`](viz/log-visualization.md)
- **Final render screenshot:** [`viz/visualization_itr_3.png`](viz/Final.png)
- **Processed dataset used by Vega:** [`data/processed/arctic_sea_ice_extent_2000_2024.geojson`](data/processed/arctic_sea_ice_extent_2000_2024.geojson)
- **Build script (raw → processed):** [`scripts/03_build_geojson.py`](scripts/03_build_geojson.py)

---

## 1) Primary dataset — Sea-ice extent edges (NSIDC Sea Ice Index, Version 4)

### What I used
- **Product:** NSIDC **Sea Ice Index, Version 4** (Sea-ice extent)
- **Region:** **Northern Hemisphere (Arctic)**
- **Temporal coverage in my processed file:** **2000–2024**
- **Months extracted (as seasonal proxies):**
  - **March** (winter maximum proxy)
  - **September** (summer minimum proxy)
- **Geometry choice (important):** I used **extent “edge/outlines” as polylines**, i.e., *line geometry* (not filled polygons).

### Where it comes from (docs + downloads)
- **Dataset landing page (Version 4):**  
  https://nsidc.org/data/G02135/versions/4
- **DOI (Version 4):**  
  https://doi.org/10.7265/a98x-0f50
- **User Guide (Version 4):**  
  https://nsidc.org/sites/default/files/documents/user-guide/g02135-v004-userguide.pdf
- **Official HTTPS file system (NOAA@NSIDC “Get Data”):**  
  https://noaadata.apps.nsidc.org/NOAA/G02135/
- **Monthly extent shapefiles (North → monthly → shapefiles → shp_extent):**  
  https://noaadata.apps.nsidc.org/NOAA/G02135/north/monthly/shapefiles/shp_extent/
  - March folder: `03_Mar/`
  - September folder: `09_Sep/`

### Version note (why filenames may say v4.0)
My time range is **2000–2024**. NSIDC states that **Version 4 files prior to 2025 are copies of Version 3** (but distributed under the Version 4 structure/filenames). This means the “v4.0” naming is expected even for older years.

---

## 2) Secondary dataset — Basemap land geometry (context)

### What I used
- **Basemap:** `world-atlas` land polygons (TopoJSON), loaded directly in Vega for context.

### Link used in the Vega spec
- Land:  
  https://unpkg.com/world-atlas@2/land-110m.json

*(This basemap is only visual context; it is not part of the scientific sea-ice measurements.)*

---

## 3) What is committed to Git (and what is not)

### Committed
- **Processed GeoJSON** used directly by Vega:  
  `data/processed/arctic_sea_ice_extent_2000_2024.geojson`
- **Build script** that produced the processed file:  
  `scripts/03_build_geojson.py`
- **Vega spec** and **iteration screenshots/logs** under `viz/`

### Not committed
- **Raw shapefile archives** downloaded from NOAA@NSIDC (they are large and reproducible from the official directory links above).

---

## 4) Processed file structure (what Vega reads)

### File
- `data/processed/arctic_sea_ice_extent_2000_2024.geojson`

### Feature count and meaning
- The processed dataset contains **one feature per (year, month)** for the selected months.
- For 2000–2024 and two months (March + September), that is **25 × 2 = 50 features**.

### Properties per feature
Each feature carries metadata fields used for filtering in Vega:
- `year` (e.g., 2017)
- `month` (3 or 9)
- `month_name` (“March” / “September”)
- `date` (string label for the month/year)

---

## 5) Important limitation (why the visualization is outlines, not filled “ice area”)

The upstream source provides extent products as both **polylines** and **polygons**. In this project I intentionally processed and committed only the **polyline outline** representation.

That means:
- The Vega visualization is designed to show **how the ice edge moves** over time.
- It does **not** show a physically filled ice mask/area from polygons.
- If a filled “satellite-like” area view is required later, the pipeline can be extended by processing the **polygon** shapefiles instead of the **polyline** shapefiles.

---

## 6) Direct “raw” link used by Vega (for GitHub Pages / Vega Editor)

The Vega spec loads the processed file via GitHub Raw:

https://raw.githubusercontent.com/princebhanusteta/bspw-vega-sea-ice/main/data/processed/arctic_sea_ice_extent_2000_2024.geojson
