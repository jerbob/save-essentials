SaveEssentials
===================
Scrape and download all module sections from CyberStart Essentials.
- - - - 

# Requirements: #
Use `pip install -r requirements.txt` to install dependencies.

# Usage: #
Before starting the scraper, make sure that you have saved your cookies to a local file.
1. First, login to the **[CyberStart Essentials page](https://essentials.joincyberdiscovery.com/)**.
1. Now, open the **Dev Tools** window with F12, navigate to the **Network** tab, and refresh the page.
![image1](https://i.snag.gy/2hWRXu.jpg)
1. Click one of the items and view the headers. Copy the contents of the **Cookie** header.
![image2](https://i.snag.gy/kRljiV.jpg)
1. Paste the contents of the **Cookie** header in a file, **cookies.txt**, in the same directory as the script.
![image3](https://i.snag.gy/EZA67g.jpg)
1. Use `python main.py` to start scraping the pages.
