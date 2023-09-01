# Manga Downloader

This is a simple `CLI` tool made with the **click** library. It simply takes in the *name* of the manga, *start chapter*, *end chapter*, and *output_dir* to save the downladed images.

Manga is downloaded from [MangaSee](https://www.mangasee123.com/), a free website to download manga from. It downloads the manga and saves it to your local machine.


## Installation / Usage

To install this project, `clone` the repo, `cd` into the directory
```bash
  git clone https://www.github.com/datalordstephen/manga-scraper.git
  cd manga-scraper
```

Next is to install requirements
```
pip install -r requirements.txt
```

To use, run the file with the arguments listed above e.g
```bash
py main.py --name "vinland saga" --path ./download
```
    
