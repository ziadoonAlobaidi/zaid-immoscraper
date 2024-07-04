from typing import Any, Iterable
import re,json
import scrapy
from bs4 import BeautifulSoup
import requests
from immoeliza.dataprocess import ImmoItem
from scrapy.spiders import SitemapSpider
from scrapy.spiders.sitemap import iterloc
from scrapy.http import Request, Response
import logging
from scrapy.utils.sitemap import Sitemap
from bs4 import BeautifulSoup

class ImmowebscraperSpider(SitemapSpider):
    """
    spider to crawl immoweb website using sitemap
    """
    name = "immowebscraper"
    allowed_domains = ["immoweb.be"]
    sitemap_urls=["https://www.immoweb.be/sitemap.xml"]
    
    def __init__(self, *args, **kwargs):
        self.logger.setLevel(logging.INFO)
        super().__init__(*args, **kwargs)
    
    def _parse_sitemap(self, response):
        """
         function handling the sitemap (.xml file) and send every link to be treated

        Args:
            response (scrapy.http.Response): result of the http requests

        Yields:
            Response: result of http request to the xml files structuring the site
        """
        body=self._get_sitemap_body(response)
        s=Sitemap(body)
        for loc in iterloc(s):
            if "classifieds" in loc:
                self.logger.info("parsing xml : {}".format(loc))
                yield Request(loc,callback=self.parse_xml_page)  
        
        
    def _filter(self,entries):
        for entry in entries:
            if "en/classified" in entry.text and  ("apartment" in entry.text or "house" in entry.text) :
                yield entry.text        
    
    def parse_xml_page(self,response):
        soup=BeautifulSoup(response.body,"xml")
        self.logger.info("parsing properties for  : {}".format(response.url))
        
        for url in self._filter(soup.find_all("loc")):
            
            yield Request(url,callback=self.parse_property)
                

    def parse_property(self,response):
        jscript=response.xpath("//script[contains(.,'window.dataLayer')]/text()")[0].get()
        it=ImmoItem()
        jscript=re.search("window.dataLayer.push\((.+?)\);",jscript,flags=re.DOTALL).group(1)
        it["js"]=json.loads(jscript)["classified"]
        it["html_elems"]=self.get_html_elem(response)
        it["Url"]=response.url
        yield it
        
        
    def get_html_elem(self,response):
        tables=response.xpath("//table[@class='classified-table']//tr").getall()
        res={}
        for t in tables:
            if re.search("<th[^>]+>([^<]+)</th>",t) is not None and re.search("<td[^>]+>([^<]+)<",t) is not None:
                res[re.search("<th[^>]+>([^<]+)<",t).group(1).strip().lower()]=re.search("<td[^>]+>([^<]+)<",t).group(1).strip().lower()
                
        return res

        
