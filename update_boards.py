import requests
import hashlib
import time

max_retries = 5
retry_delay = 60  # Wait for 60 seconds before retrying

for attempt in range(max_retries):
    response = requests.get('https://api.github.com/repos/ropg/board_definitions/releases/146843375', headers={'Accept': 'application/vnd.github.v3+json'})
    release_data = response.json()
    assets = release_data.get('assets', [])
    source_zip = next((asset for asset in assets if asset['name'].endswith('.zip') and asset['content_type'] == 'application/zip'), None)

    if source_zip:
        break

    if attempt < max_retries - 1:
        time.sleep(retry_delay)
else:
    raise Exception('Source code zip not found after {} retries.'.format(max_retries))

asset_url = source_zip['browser_download_url']
asset_size = source_zip['size']
response = requests.get(asset_url)
sha256_hash = hashlib.sha256(response.content).hexdigest()

with open('boards.json.editme', 'r') as file:
    content = file.read()

content = content.replace('{tag}', release_data['tag_name']).replace('{hash}', sha256_hash).replace('{filesize}', str(asset_size))

with open('boards.json', 'w') as file:
    file.write(content)
