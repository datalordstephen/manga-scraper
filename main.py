#!/usr/bin/env python

import requests
import os
import click
import shutil
from src.utils import get_image_url, download_page, get_number_of_chapters
import sys

BASE_URL = "https://www.mangasee123.com/manga/"
BASE_IMG_URL = "https://hot.leanbox.us/manga/"

@click.command()
@click.option('--name', default="vinland saga", help = "Name of manga you want to download (default: Vinland saga)")
@click.option('--start', default = 1, help = "First chapter to download")
@click.option('--last', default = 10, help = "Last chapter to download")
@click.option('--save_dir', default = os.path.join(os.getcwd(), "manga"), help="Path to save the manga")

def main(name, start, last, save_dir) -> None:
    no_chapters = get_number_of_chapters(BASE_URL, name)
    sys.exit(0)
    
    
    if os.path.exists(save_dir):
        print(f"Path: {save_dir} already exists, deleting it...")
        shutil.rmtree(save_dir)
    os.makedirs(save_dir)
    print("Created: {}".format(save_dir))
        
    for chapter_num in range(start, last + 1):
        chapter_path = os.path.join(save_dir, f"chap-{chapter_num}")
        os.mkdir(chapter_path)
        print(f"Created the chapter {chapter_num} directory. Downloading pages...")
        page_num = 1
        
        while True:
            img_url = get_image_url(BASE_IMG_URL, name, chapter_num, page_num)
                        
            chapter_ended = download_page(img_url, page_num, chapter_path, page_num)
            
            if not chapter_ended:
                page_num += 1
            else:
                break
        
            
        
        
        
    
if __name__ == "__main__":
    main()