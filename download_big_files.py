import os
import requests

def download_file(url, local_path):
    if not os.path.exists(local_path):
        print(f"📥 Downloading {local_path} ...")
        r = requests.get(url, stream=True)
        with open(local_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"✅ Downloaded {local_path}")
    else:
        print(f"✅ {local_path} already exists, skipping download.")

# Make sure 'data/' folder exists
os.makedirs('data', exist_ok=True)

# ✅ Small S3 URLs
elevation_url = 'https://lunartix-data.s3.us-east-1.amazonaws.com/rescaled_Elevation_small.tif'
slope_url = 'https://lunartix-data.s3.us-east-1.amazonaws.com/cleaned_Slope_small.tif'

# ✅ Local file paths to save (can keep same names your app expects)
elevation_path = 'data/rescaled_Elevation.tif'
slope_path = 'data/cleaned_Slope.tif'

# Download them if missing
download_file(elevation_url, elevation_path)
download_file(slope_url, slope_path)
