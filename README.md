# Worldometer_scraper
A web scraper, to scrape data from Worldometer, one of the most relevant websites that provides counters and real-time statistics mainly for demographic topic. The final purpose is to automate the creation of an xlsx file containing info scraped in a tabular view

<details><summary>Tools Needed</summary>
<p>

- Computer where to host the python scripts and xlsx file.
  
- A Python 3 interpreter with Scrapy library installed
 
- Anaconda Navigator to make scrapy library performing on Windows 

</p>
</details>

# Installation  

1. Run a `git clone https://github.com/Feder07/worldometer_scraper/` command or download files from my repo.
2. pip install scrapy
3. scrapy startproject 'projectname'
4. scrapy genspider worldometer 'https://www.worldometers.info/population'
5. run python3 worldometer.py
