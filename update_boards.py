import requests
import time
import os

# Initialization
max_retries = 3
retry_delay = 30  # seconds
release_data = None

# Define the base URL pattern for direct download
base_url = "https://github.com/ropg/board_definitions/archive/refs/tags/{tag}.zip"

# Retry fetching the release data to get the tag name
for attempt in range(max_retries):
    response = requests.get('https://api.github.com/repos/ropg/board_definitions/releases/146843375')
    if response.ok:
        release_data = response.json()
        break
    else:
        print(f"Attempt {attempt + 1}: Failed to fetch release data, retrying in {retry_delay} seconds...")
        time.sleep(retry_delay)

if not release_data:
    raise Exception("Failed to fetch release data after {} retries.".format(max_retries))

tag_name = release_data['tag_name']

# Construct the download URL
download_url = base_url.format(tag=tag_name)

# Download the zip file
print(f"Downloading {download_url}...")
response = requests.get(download_url)

# Save the file in the same directory as the script
filename = f"{tag_name}.zip"

with open(filename, 'wb') as f:
    f.write(response.content)

print(f"Downloaded {filename}")
