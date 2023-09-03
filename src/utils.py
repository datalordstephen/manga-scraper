# import requests
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import os
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

DRIVER_PATH = os.path.join(os.getcwd(), "chromedriver.exe")
API_URL = "https://webdis-9a33.onrender.com/search"

def convert_anime_name(formatted_str: str) -> str:
    query_params = {"keyw": formatted_str}
    res = requests.get(API_URL, params=query_params)
    data = res.json()
    value = data[0]["animeTitle"]
    return value

def get_chapter_details(base_url: str, name: str):
    formatted_str = name.title().replace(" ", "-")
    
    right_name = convert_anime_name(formatted_str)
    right_name = right_name.title().replace(" ", "-")
    
    if right_name != formatted_str:
        print(f"By '{name}' did you mean '{right_name}'?")
        formatted_str = right_name
        
    url = urljoin(base_url, formatted_str)
    print("Getting the list of chapters of {}...".format(formatted_str))
    
    service = Service(executable_path=DRIVER_PATH)
    options = ChromeOptions()
    options.add_argument("--headless=new")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    
    
    driver = Chrome(service=service, options=options)
    driver.get(url)
    driver.find_element(By.CSS_SELECTOR, "div[class='list-group-item ShowAllChapters ng-scope']").click()
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()
    
    html_attrs = {
        "class": "ng-binding",
        "style": "font-weight:600"
    }
    
    chapter_span = soup.find_all("span", attrs= html_attrs)
    chapters = [str(chapter.text).strip().split()[1] for chapter in chapter_span]
    
    chapters = process_chapter_list(chapters)
    most_recent = chapters[0]
    
    print(f"{formatted_str} currently ends at chapter {most_recent}")
    print("-" * 50)
    
    return most_recent, formatted_str, chapters

    

def get_image_url(base_url: str, name: str, chapter, page: int) -> str:
    formatted_str = name.title().replace(" ", "-")
    
    if type(chapter) == float:
        zeros = (4 - len(str(int(chapter)))) * "0"
    else:
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
        
def process_chapter_list(chapters_list: list[str]) -> list:
    to_return = []
    for chapter in chapters_list:
        try:
            res = int(chapter)
        except ValueError:
            res = float(chapter)
        to_return.append(res)
    
    assert len(to_return) == len(chapters_list), "Something went wrong"
    return to_return

def format_input(end: float):
    if int(end) == end:
        return int(end)
    else:
        return end
    
if __name__ == "__main__":
    name = input("Enter an anime: ")
    convert_anime_name(name)
    