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
scrapy crawl immowescraper -o data/output.json
```

The output is important because the [post process](immoeliza/pipelines.py#L22) step executed when the spider is done reads data from that file.

## Results

1. raw dataset : 83304 properties
2. remove null prices and postal code : 58667
3. remove postal code that are not from Belgium : 57285
4. clean duplicated entries (same price, bedrooms and living area) : 39939

Now it's your turn to test  !! 

![spider](img/spider.webp)