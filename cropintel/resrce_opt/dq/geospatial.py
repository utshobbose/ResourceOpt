import geopandas as gpd

def ensure_valid(districts: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    # Fix invalid polygons and ensure CRS is WGS84
    gdf = districts.to_crs(4326)
    gdf["geometry"] = gdf["geometry"].buffer(0)  # common fix
    if gdf.is_empty.any() or (~gdf.is_valid).any():
        raise ValueError("Invalid geometries after repair.")
    return gdf

def check_overlaps(districts: gpd.GeoDataFrame) -> list[tuple[str,str]]:
    overlaps = []
    sindex = districts.sindex
    for i, geom in enumerate(districts.geometry):
        for j in sindex.query(geom, predicate="overlaps"):
            if j > i:
                overlaps.append((districts.iloc[i]["code"], districts.iloc[j]["code"]))
    return overlaps