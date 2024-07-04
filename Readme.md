# IMMO ELIZA SCRAPER

## installation steps

1. clone the repository using git

```
git clone git@github.com:DeLeb86/immoscraper.git
```

2. create a virtual environment using venv

```
python3 -m venv ~/.venv/eliza_scraping
```

3. activate the virtual environment

```
source ~/.venv/eliza_scraping/bin/activate
```

4. install required libraries with pip 

```
pip install -r requirements.txt
```

## Execution
run scrapy command : 

```
scrapy crawl immowescraper -o output.json
```

The output is important because the [post process](immoeliza/pipelines.py#L22) step executed when the spider is done reads data from that file.

Now it's your turn to test  !! 

![spider](img/spider.webp)