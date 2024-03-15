import requests
import hashlib
import time

# Set maximum number of retries and delay between retries
max_retries = 5
retry_delay = 60  # in seconds

for attempt in range(max_retries):
    # Fetch release data from GitHub API
    response = requests.get('https://api.github.com/repos/ropg/board_definitions/releases/146843375', headers={'Accept': 'application/vnd.github.v3+json'})
    release_data = response.json()
    assets = release_data.get('assets', [])

    # Log the assets for debugging
    print(f"Attempt {attempt + 1}: Found assets: {assets}")

    # Try to find the zip file in the assets
    source_zip = next((asset for asset in assets if asset['name'].endswith('.zip') and asset['content_type'] == 'application/zip'), None)

    if source_zip:
        break  # Exit loop if zip file is found
    time.sleep(retry_delay)  # Wait before the next attempt

# Raise an exception if the zip file was not found after all retries
if not source_zip:
    raise Exception(f'Source code zip not found after {max_retries} retries.')

# Proceed with downloading the zip file and updating the hash and size in boards.json
asset_url = source_zip['browser_download_url']
asset_size = source_zip['size']
response = requests.get(asset_url)
sha256_hash = hashlib.sha256(response.content).hexdigest()

# Update boards.json.editme with the new values
with open('boards.json.editme', 'r') as file:
    content = file.read()

content = content.replace('{tag}', release_data['tag_name']).replace('{hash}', sha256_hash).replace('{filesize}', str(asset_size))

with open('boards.json', 'w') as file:
    file.write(content)
