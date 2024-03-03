import requests
from bs4 import BeautifulSoup


url = "https://www.pond5.com/search?kw=hospital-beep&media=sfx"

response = requests.get(url)

if response.status_code == 200:
    html_content = response.text

    print(html_content[:500])
else:
    print(f"Failed to retrieve content, status code: {response.status_code}")


soup = BeautifulSoup(html_content, 'html.parser')

# Find all items by their class
items = soup.find_all(class_="MusicList-item js-searchResultItem js-searchResult js-musicListSearchResult")


files_to_download = {}

for item in items:
    file_name = item.find(class_="MusicList-itemTitle js-searchResultTitle").text.strip()
    download_link = item.find('button', class_="js-downloadPreviewButton")['data-download-href']

    files_to_download[file_name] = download_link

def download_files(files_dict):
    for file_name, url in files_dict.items():
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_name + ".m4a", 'wb') as f:
                f.write(response.content)
            print(f"Downloaded: {file_name}")
        else:
            print(f"Failed to download: {file_name}")

download_files(files_to_download)
