#!/usr/bin/env python3
import argparse
import re
from pathlib import Path

import geopandas as gpd
import pandas as pd


def find_shapefile(year_dir: Path) -> Path:
    """
    Find the main .shp inside a year directory.
    We prefer the longest/most specific filename if multiple exist.
    """
    shps = sorted(year_dir.glob("*.shp"), key=lambda p: len(p.name), reverse=True)
    if not shps:
        raise FileNotFoundError(f"No .shp found in: {year_dir}")
    return shps[0]


def month_label_to_int(m: str) -> int:
    m = m.lower().strip()
    if m in ["mar", "march", "03", "3"]:
        return 3
    if m in ["sep", "sept", "september", "09", "9"]:
        return 9
    raise ValueError(f"Unknown month label: {m} (use mar or sep)")


def main():
    parser = argparse.ArgumentParser(
        description="Convert yearly Arctic sea-ice extent shapefiles to one merged GeoJSON (with year+month)."
    )
    parser.add_argument("--raw-root", default="data/raw", help="Raw folder containing mar/ and sep/ subfolders.")
    parser.add_argument("--out-dir", default="data/processed", help="Where to write processed GeoJSON files.")
    parser.add_argument("--months", nargs="+", default=["mar", "sep"], help="Months to process (mar sep).")
    parser.add_argument("--start-year", type=int, default=2000)
    parser.add_argument("--end-year", type=int, default=2024)
    args = parser.parse_args()

    repo_raw = Path(args.raw_root).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    all_frames = []

    for month in args.months:
        month_int = month_label_to_int(month)
        month_dir = repo_raw / month

        if not month_dir.exists():
            raise FileNotFoundError(f"Missing month folder: {month_dir}")

        for year in range(args.start_year, args.end_year + 1):
            year_dir = month_dir / str(year)
            if not year_dir.exists():
                raise FileNotFoundError(f"Missing year folder: {year_dir}")

            shp_path = find_shapefile(year_dir)

            gdf = gpd.read_file(shp_path)

            # Ensure CRS is WGS84 for web mapping / Vega geoshape
            # If CRS is missing, we keep it as-is but this is rare for official shapefiles.
            if gdf.crs is None:
                print(f"[WARN] CRS missing for {shp_path.name}. Keeping as-is.")
            else:
                gdf = gdf.to_crs(epsg=4326)

            # Add metadata columns for filtering/slider in Vega
            gdf["year"] = year
            gdf["month"] = month_int
            gdf["month_name"] = "March" if month_int == 3 else "September"
            gdf["date"] = f"{year}-{month_int:02d}-01"

            # Keep geometry + metadata + (optional) any useful original fields
            keep_cols = ["year", "month", "month_name", "date", "geometry"]
            gdf = gdf[keep_cols].copy()

            all_frames.append(gdf)

            print(f"[OK] Loaded {month} {year}: {shp_path.name} ({len(gdf)} features)")

    merged = pd.concat(all_frames, ignore_index=True)
    merged_gdf = gpd.GeoDataFrame(merged, geometry="geometry", crs="EPSG:4326")

    out_file = out_dir / "arctic_sea_ice_extent_2000_2024.geojson"
    merged_gdf.to_file(out_file, driver="GeoJSON")
    print(f"\n[DONE] Wrote merged GeoJSON: {out_file}")
    print(f"       Rows: {len(merged_gdf)} | Years: {args.start_year}-{args.end_year} | Months: {args.months}")


if __name__ == "__main__":
    main()
