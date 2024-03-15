import requests
import hashlib

# Fetch release data
release_data = requests.get('https://api.github.com/repos/ropg/board_definitions/releases/146841975', headers={'Accept': 'application/vnd.github.v3+json'}).json()
tag_name = release_data['tag_name']
assets = release_data['assets']
source_zip = [asset for asset in assets if asset['name'].endswith('.zip') and asset['content_type'] == 'application/zip']

if not source_zip:
    raise Exception('Source code zip not found.')

source_zip = source_zip[0]
asset_url = source_zip['browser_download_url']
asset_size = source_zip['size']

# Download and compute SHA-256
response = requests.get(asset_url)
sha256_hash = hashlib.sha256(response.content).hexdigest()

# Update boards.json.editme
with open('boards.json.editme', 'r') as file:
    content = file.read()

content = content.replace('{tag}', tag_name).replace('{hash}', sha256_hash).replace('{filesize}', str(asset_size))

with open('boards.json', 'w') as file:
    file.write(content)
