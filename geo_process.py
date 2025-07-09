import geopandas as gpd
from data_loader import load_rivers, load_villages

def buffer_rivers():
    rivers = load_rivers()
    print("✅ Loaded rivers data")

    # Step 1: Check original CRS
    print("Original CRS:", rivers.crs)

    # Step 2: Reproject to projected CRS (example: EPSG:32643 → UTM zone 43N)
    # Change EPSG if your area is in a different zone!
    rivers_projected = rivers.to_crs(epsg=32643)
    print("Reprojected CRS:", rivers_projected.crs)

    # Step 3: Buffer in meters
    buffered = rivers_projected.copy()
    buffered['geometry'] = buffered.geometry.buffer(100)  # buffer 100 meters

    # Step 4: Reproject back to EPSG:4326
    buffered = buffered.to_crs(epsg=4326)

    # Step 5: Save to output
    buffered.to_file("output/rivers_buffered.geojson", driver="GeoJSON")
    print("✅ Saved buffered rivers to output/rivers_buffered.geojson")


def clip_villages_to_area():
    villages = load_villages()
    print("✅ Loaded villages data")

    # Example: clip to a small bounding box (change numbers as needed)
    clipped = villages.cx[74.0:74.5, 18.5:19.0]
    clipped.to_file("output/villages_clipped.geojson", driver="GeoJSON")
    print("✅ Saved clipped villages to output/villages_clipped.geojson")


if __name__ == "__main__":
    buffer_rivers()
    clip_villages_to_area()

