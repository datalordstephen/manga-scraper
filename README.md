# Manga Downloader

This is a simple `CLI` tool made with the **click** library. It simply takes in the *name* of the manga, *start chapter*, *end chapter*, and *output_dir* to save the downladed images.

Manga is downloaded from [MangaSee](https://www.mangasee123.com/), a free website to download manga from. It downloads the manga and saves it to your local machine.

## Prerequisites

A prerequisite to run this is to have **[Google Chrome](https://www.google.com/chrome/)** installed on your computer, as well as a **Chromedriver** executeable file.

If your chrome version is *114.0.5735.90* or lower, you can download it [here](https://chromedriver.chromium.org/downloads). If it's a newer version of chrome, you can download a stable version of the executeable from [here](https://googlechromelabs.github.io/chrome-for-testing/)

To check your chrome version, paste this link in your chrome browser:

```
chrome://settings/help
```
## Installation / Usage

To install this project, `clone` the repo, `cd` into the directory
```bash
  git clone https://www.github.com/datalordstephen/manga-scraper.git
  cd manga-scraper
```

Next is to install the requirements
```
pip install -r requirements.txt
```
After that, place the `chromedriver.exe` downloaded earlier in this directory (i.e `manga-scraper`). This step is necessary as the driver is needed.

To see all arguments and their defaults, run:
```bash
py main.py --help
```

To use, run the file with the arguments listed above e.g
```bash
py main.py --name "attack on titan" --end 20
```
## Side Notes

This is still in development, so for the meantime I'm sure that these manga would get downloaded:

* **Attack on Titan**
* **My Hero Academia**
* **Demon Slayer**
* **Vinland Saga**

## Update
The tool should be able to successfully download ANY manga on the mangasee website. Working on checking availability on the website and supporting other download sites 

Yours Sincerely **o_O**
