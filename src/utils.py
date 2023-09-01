# import requests
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import os

def get_number_of_chapters(base_url: str, name: str) -> int:
    formatted_str = name.title().replace(" ", "-")
    url = urljoin(base_url, formatted_str)
    res = requests.get(url)
    print(res.status_code)
    
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, "html.parser")
        spans = soup.find_all("span")
        print(spans)
    

def get_image_url(base_url: str, name: str, chapter: int, page: int) -> str:
    formatted_str = name.title().replace(" ", "-")
    
    zeros = (4 - len(str(chapter))) * "0"
    _chapter = f"{zeros}{chapter}"
    
    page_zeros = (3 - len(str(page))) * "0"
    _page = f"{page_zeros}{page}"
    
    search_url = urljoin(base_url, formatted_str, f"{_chapter}-{_page}.png")
    return search_url


def download_page(img_url: str, output_path: str, chapter_path: str, page_num: int) -> bool:
    output_path = os.path.join(chapter_path, f"{page_num}.png")
    
    res = requests.get(img_url)
    
    status = False
    if res.status_code == 200:
        with open(output_path, "wb") as file:
            file.write(res.content)
        print(f"Page {page_num} downloaded.")
    elif res.status_code == 404:
        status = True
    
    return status
        
    
    
    