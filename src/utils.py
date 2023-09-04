from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
import os
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

DRIVER_PATH = os.path.join(os.getcwd(), "chromedriver.exe")
API_URL = "https://webdis-9a33.onrender.com/search"

def convert_anime_name(formatted_str: str) -> str:
    query_params = {"keyw": formatted_str}
    res = requests.get(API_URL, params=query_params)
    data = res.json()
    value = data[0]["animeTitle"]
    return value

def create_driver(headless: bool = True) -> Chrome:
    service = Service(executable_path=DRIVER_PATH)
    options = ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    if headless:
        options.add_argument("--headless=new")
    
    driver = Chrome(service=service, options=options)
    return driver


def get_chapter_details(base_url: str, name: str):
    formatted_str = name.title().replace(" ", "-")
    
    right_name = convert_anime_name(formatted_str)
    right_name = right_name.title().replace(" ", "-")
    
    if right_name != formatted_str:
        print(f"By '{name}' did you mean '{right_name}'?")
        formatted_str = right_name
        
    url = urljoin(base_url, formatted_str)
    driver = create_driver()
    driver.get(url)
    driver.find_element(By.CSS_SELECTOR, "div[class='list-group-item ShowAllChapters ng-scope']").click()
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()
    
    html_attrs = {
        "class": "ng-binding",
        "style": "font-weight:600"
    }
    
    chapter_spans = soup.find_all("span", attrs= html_attrs)
    chapters = [str(chapter.text).strip().split()[1] for chapter in chapter_spans]
    
    chapters = process_chapter_list(chapters)
    most_recent = chapters[0]
    
    print(f"{formatted_str} currently ends at chapter {most_recent}")
    print("-" * 50)
    
    return most_recent, formatted_str, chapters

    
def get_manga_details(base_url: str, formatted_name: str, chapter, check_url: bool = True) -> tuple[int, str]:
    first_part = base_url.replace("manga/", "")
    second_part = f"read-online/{formatted_name}-chapter-{chapter}-page-1.html"
    page_1_url = urljoin(first_part, second_part)
    
    if check_url:
        print("-" *50)
        print("Getting the details of {} Chapter {}...".format(formatted_name, chapter))
    
    driver = create_driver()
    driver.set_page_load_timeout(7)
    
    try:
        driver.get(page_1_url)
    except TimeoutException:
        driver.execute_script("window.stop();")
    
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()
    
    page_buttons = soup.find_all("button", attrs={"ng-click":"vm.GoToPage(Page)"})
    page_buttons = [int(str(page_num.text).strip()) for page_num in page_buttons]
    no_of_pages = page_buttons[-1]
    
    img_url = None
    if check_url:
        img = soup.find("img", attrs={"class": "img-fluid HasGap"})
        img_url = img["src"]
        img_url = img_url[:img_url.find(formatted_name)]
        
    print('-' * 50)
    return no_of_pages, img_url
    
    

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
    get_manga_details("https://www.mangasee123.com/manga/", "Vinland-Saga", 193)
    