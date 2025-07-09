from data_loader import (
    load_villages, load_soil, load_rivers, load_highways,
    load_lulc, load_elevation, load_usecases, load_crop_knowledge
)

# Load data
villages = load_villages()
soil = load_soil()
rivers = load_rivers()
highways = load_highways()
lulc = load_lulc()
elevation = load_elevation()
usecases = load_usecases()
crop_knowledge = load_crop_knowledge()

# Print checks
print("Villages:", villages.head())
print("Soil:", soil.head())
print("Rivers:", rivers.head())
print("Highways:", highways.head())
print("LULC CRS:", lulc.crs)
print("Elevation CRS:", elevation.crs)
print("First 3 usecases:", usecases[:3])
print("Crop knowledge keys:", crop_knowledge.keys())
