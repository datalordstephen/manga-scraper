#!/usr/bin/env python

import os
from tqdm import tqdm
import click
import shutil
from src.utils import get_image_url, download_page, get_number_of_chapters

BASE_URL = "https://www.mangasee123.com/manga/"
BASE_IMG_URL = "https://hot.leanbox.us/manga/"

@click.command()
@click.option('--name', default="vinland saga", help = "Name of manga you want to download (default: Vinland saga)")
@click.option('--start', default = 1, help = "First chapter to download")
@click.option('--end', default = 10, help = "Last chapter to download")
@click.option('--save_dir', default = os.path.join(os.getcwd(), "manga"),
              help="Absolute path to save the manga. If not specified, a dir `manga` will be created in the pwd and \
                  the manga will be saved in a sub folder with the name of the manga e.g manga/vinland-saga")

def main(name, start, end, save_dir) -> None:
    no_chapters, formatted_name = get_number_of_chapters(BASE_URL, name)

    save_dir = os.path.join(save_dir, formatted_name)
    
    if end > no_chapters:
        print(f"{formatted_name} only has {no_chapters} chapters, {end} exceeds that")
        raise ValueError("Last chapter exceeds the number of chapters in the manga")
    
    if os.path.exists(save_dir):
        print(f"Path: {save_dir} already exists, deleting it...")
        shutil.rmtree(save_dir)
        
    os.makedirs(save_dir)
    print("Created: {}".format(save_dir))
    print("-" *50, end="\n\n")
        
    print(f"Dowloading chapters {start} to {end} of {formatted_name}".title())
    
    for chapter_num in tqdm(range(start, end + 1), desc="Chapters Downloaded", ncols=100):
        chapter_path = os.path.join(save_dir, f"chap-{chapter_num}")
        os.mkdir(chapter_path)
        page_num = 1
        
        while True:
            img_url = get_image_url(BASE_IMG_URL, name, chapter_num, page_num)
                        
            chapter_ended = download_page(img_url, page_num, chapter_path, page_num)
            
            if not chapter_ended:
                page_num += 1
            else:
                break
    print("\nDownload Completed!")
        
            
        
        
        
    
if __name__ == "__main__":
    main()