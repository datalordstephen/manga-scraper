#!/usr/bin/env python

import os
from tqdm import tqdm
import click
import shutil
from src.utils import * 

BASE_URL = "https://www.mangasee123.com/manga/"
BASE_IMG_URL = ""

@click.command()
@click.option('--name', default="vinland saga", help = "Name of manga you want to download (default: Vinland saga)")
@click.option('--start', default = 1.0, help = "First chapter to download (can be a number or decimal e.g 1, default: 1)")
@click.option('--end', default = 10.0, help = "Last chapter to download (can be a number or decimal e.g 21.5), pass -1 to download till the last chapter (default: 10)")
@click.option('--save_dir', default = os.path.join(os.getcwd(), "manga"),
              help="Absolute path to save the manga. If not specified, a dir `manga` will be created in the pwd and the manga will be saved in a sub folder with the name of the manga e.g manga/Vinland-Saga")

def main(name, start, end, save_dir) -> None:
    no_chapters, formatted_name, chapters = get_chapter_details(BASE_URL, name)
    save_dir = os.path.join(save_dir, formatted_name)
    
    end, start = format_input(end), format_input(start)
    end = no_chapters if end == -1 else end
    
    if end > no_chapters:
        raise ValueError(f"Chapter {end} exceeds the number of chapters in the manga ({no_chapters}). Please enter a valid chapter number (1 - {no_chapters})")
    
    if os.path.exists(save_dir):
        print(f"Path: {save_dir} already exists, deleting it...")
        shutil.rmtree(save_dir)
        
    os.makedirs(save_dir)
    print("Created: {}".format(save_dir))
    print("-" *50)
    
    print(f"Dowloading chapters {start} to {end} of {formatted_name}".title())
    
    chapters.reverse()
    chap_range = chapters[chapters.index(start):chapters.index(end) + 1]

    for chapter_num in chap_range:
        chapter_path = os.path.join(save_dir, f"chap-{chapter_num}")
        os.mkdir(chapter_path)
        
        check_url = False if chapter_num != start else True
        num_pages, result = get_manga_details(BASE_URL, formatted_name, chapter_num, check_url)
        BASE_IMG_URL = result if check_url else BASE_IMG_URL
        
        for page_num in tqdm(range(1, num_pages + 1), desc=f"Chapter {chapter_num}", ncols=100):
            while True:
                img_url = get_image_url(BASE_IMG_URL, chapter_num, page_num)
                            
                new_base_image_url = download_page(img_url, page_num, chapter_path, page_num)
                
                if new_base_image_url:
                    print("\nDetected a change in the cloud storage location, checking again...")
                    _, BASE_IMG_URL = get_manga_details(BASE_URL, formatted_name, chapter_num)
                    continue
                else:
                    break

    print("\nDownload Completed!")
        
            
        
        
        
    
if __name__ == "__main__":
    main()