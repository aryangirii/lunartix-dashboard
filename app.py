import streamlit as st
import geopandas as gpd
import folium
import rasterio
from rasterio.plot import show
from streamlit_folium import st_folium
import matplotlib.pyplot as plt

# ✅ NEW: download large tif files from S3 if missing
import download_big_files

# Streamlit page config
st.set_page_config(page_title="🗺 Geospatial Dashboard", layout="wide")
st.title("🗺️ Geospatial Dashboard")

# --------------------------
# 🧩 Load vector data
# --------------------------
rivers = gpd.read_file("data/rivers.geojson")
soil = gpd.read_file("data/soil.geojson")
villages = gpd.read_file("data/pune_villages.geojson")
highways = gpd.read_file("data/highways.geojson")

# Convert non-geometry columns in highways to string
for col in highways.columns:
    if col != 'geometry':
        highways[col] = highways[col].astype(str)

highways_clean = highways[['geometry']]

# --------------------------
# ✅ Sidebar controls
# --------------------------
st.sidebar.header("🛠 Controls")

show_rivers = st.sidebar.checkbox("Show Rivers", value=True)
show_soil = st.sidebar.checkbox("Show Soil", value=True)
show_villages = st.sidebar.checkbox("Show Villages", value=True)
show_highways = st.sidebar.checkbox("Show Highways", value=True)
show_buffer = st.sidebar.checkbox("Show Buffer around Rivers", value=True)

buffer_distance = st.sidebar.slider("Buffer distance (meters)", min_value=50, max_value=500, value=100, step=50)

# --------------------------
# 🗺 Create folium map
# --------------------------
m = folium.Map(location=[18.7, 74.2], zoom_start=9)

if show_rivers:
    folium.GeoJson(rivers, name="Rivers", style_function=lambda x: {'color': 'blue'}).add_to(m)

if show_soil:
    folium.GeoJson(soil, name="Soil", style_function=lambda x: {'color': 'brown', 'weight': 0.5}).add_to(m)

if show_villages:
    folium.GeoJson(villages, name="Villages", style_function=lambda x: {'color': 'green', 'weight': 0.3}).add_to(m)

if show_highways:
    folium.GeoJson(highways_clean, name="Highways", style_function=lambda x: {'color': 'red', 'weight': 1}).add_to(m)

# ✅ Dynamic buffer: reproject, buffer, reproject back
if show_buffer:
    rivers_projected = rivers.to_crs(epsg=32643)  # UTM zone 43N (for Maharashtra)
    buffered = rivers_projected.buffer(buffer_distance)
    buffered_gdf = gpd.GeoDataFrame(geometry=buffered).set_crs(32643).to_crs(4326)
    folium.GeoJson(buffered_gdf, name=f"Buffer {buffer_distance}m", style_function=lambda x: {'color': 'purple', 'fillOpacity': 0.2}).add_to(m)

folium.LayerControl().add_to(m)

# --------------------------
# 🌐 Show map
# --------------------------
st.subheader("🗺 Vector Layers Map")
st_folium(m, width=1000, height=600)

# --------------------------
# 🌄 Raster previews
# --------------------------
st.subheader("🌄 Raster Layers Preview")

cols = st.columns(2)

with cols[0]:
    st.text("Elevation (rescaled_Elevation.tif)")
    with rasterio.open("data/rescaled_Elevation.tif") as src:
        fig, ax = plt.subplots()
        show(src, ax=ax, title='Elevation')
        st.pyplot(fig)

with cols[1]:
    st.text("Land Use Land Cover (resampled_lulc.tif)")
    with rasterio.open("data/resampled_lulc.tif") as src:
        fig, ax = plt.subplots()
        show(src, ax=ax, title='LULC')
        st.pyplot(fig)

# --------------------------
# 📊 Show data tables
# --------------------------
st.subheader("📊 Data Tables (first 5 rows)")
st.write("**Villages:**")
st.dataframe(villages.head())

st.write("**Highways:**")
st.dataframe(highways.head())

st.write("**Soil:**")
st.dataframe(soil.head())

st.write("**Rivers:**")
st.dataframe(rivers.head())

st.info(f"Dynamic buffer distance: **{buffer_distance} meters** (live update)")
