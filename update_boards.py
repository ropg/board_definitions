import requests

# Define the base URL pattern for direct download
base_url = "https://github.com/ropg/board_definitions/archive/refs/tags/{tag}.zip"

# Fetch release data to get the tag name
response = requests.get('https://api.github.com/repos/ropg/board_definitions/releases/latest')
release_data = response.json()
tag_name = release_data['tag_name']

# Construct the download URL
download_url = base_url.format(tag=tag=tag_name)

# You can print out the URL or use it in any way required
# This script assumes you're only logging the URL and not downloading the file here
print(f"Download URL: {download_url}")

# This is a placeholder for where you'd update boards.json
# It assumes boards.json is in the current directory and updates it directly.
# Add your logic here to update boards.json as needed.
with open('boards.json', 'r') as file:
    content = file.read()

# Assuming you have some logic to update the content
# content = content.replace('some_placeholder', 'new_value')

with open('boards.json', 'w') as file:
    file.write(content)
