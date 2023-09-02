# import requests
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import os
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service

DRIVER_PATH = os.path.join(os.getcwd(), "chromedriver.exe")
API_URL = "https://webdis-9a33.onrender.com/search"

def convert_anime_name(formatted_str: str) -> str:
    query_params = {"keyw": formatted_str}
    res = requests.get(API_URL, params=query_params)
    data = res.json()
    value = data[0]["animeTitle"]
    return value

def get_number_of_chapters(base_url: str, name: str) -> int:
    formatted_str = name.title().replace(" ", "-")
    
    right_name = convert_anime_name(formatted_str)
    right_name = right_name.title().replace(" ", "-")
    
    if right_name != formatted_str:
        print(f"By '{name}' did you mean '{right_name}'?")
        formatted_str = right_name
        
    url = urljoin(base_url, formatted_str)
    print("Getting number of chapters of {}...".format(formatted_str))
    
    service = Service(executable_path=DRIVER_PATH)
    options = ChromeOptions()
    options.add_argument("--headless=new")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    
    
    driver = Chrome(service=service, options=options)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()
    
    html_attrs = {
        "class": "ng-binding",
        "style": "font-weight:600"
    }
    
    latest_chapter_span = soup.find("span", attrs= html_attrs)
    
    latest_chapter = latest_chapter_span.text.strip()
    chapter = latest_chapter.split()[1]
    print(f"{formatted_str} currently ends at chapter {chapter}")
    print("-" * 50)
    
    return int(chapter), formatted_str

    

def get_image_url(base_url: str, name: str, chapter: int, page: int) -> str:
    formatted_str = name.title().replace(" ", "-")
    
    zeros = (4 - len(str(chapter))) * "0"
    _chapter = f"{zeros}{chapter}"
    
    page_zeros = (3 - len(str(page))) * "0"
    _page = f"{page_zeros}{page}"
    
    joined = f"{_chapter}-{_page}.png"
    sub_url = formatted_str + "/" + joined
    
    search_url = urljoin(base_url, sub_url)
    return search_url


def download_page(img_url: str, output_path: str, chapter_path: str, page_num: int) -> bool:
    output_path = os.path.join(chapter_path, f"{page_num}.png")
    
    res = requests.get(img_url)
    
    not_found = False
    if res.status_code == 200:
        with open(output_path, "wb") as file:
            file.write(res.content)
    elif res.status_code == 404:
        not_found = True
    
    return not_found
        
    
if __name__ == "__main__":
    name = input("Enter an anime: ")
    convert_anime_name(name)
    