import re, json
import spacy, scrapy
from scrapy.selector import Selector
from scrapy.item import Item, Field
from scrapy.crawler import CrawlerProcess
from collections import Counter
from string import punctuation

class JsonWriterPipeline(object):
    def open_spider(self, spider):
        self.file = open('scrapy_RMP.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(item) + "\n"
        self.file.write(line)
        return item

class RateMyProfessor_Spider(scrapy.Spider):
    name = "RateMyProfessorSpider"
    
    def __init__(self):
        pass

    def start_requests(self):
        start_url = r"https://solr-aws-elb-production.ratemyprofessors.com//solr/rmp/select/?solrformat=true&rows=0&wt=json&json.wrf=noCB&callback=noCB&q=*%3A*+AND+schoolid_s%3A1381&defType=edismax&qf=teacherfirstname_t%5E2000+teacherlastname_t%5E2000+teacherfullname_t%5E2000+autosuggest&bf=pow(total_number_of_ratings_i%2C2.1)&sort=total_number_of_ratings_i+desc&siteName=rmp&rows=20&start=0&fl=pk_id+teacherfirstname_t+teacherlastname_t+total_number_of_ratings_i+averageratingscore_rf+schoolid_s&fq="
        yield scrapy.Request(url = start_url, callback = self.parse)

    def parse(self, response):
        header = json.loads(response.body_as_unicode()[5:-1])
        num_found = int(header["response"]["numFound"])
        yield {"count": num_found}
        yield response.follow(url = response.url.replace("rows=0", f"rows={num_found}"), callback = self.parse_list)

    def parse_list(self, response):
        data = json.loads(response.body_as_unicode()[5:-1])["response"]["docs"]
        for pk in data:
            # yield {"pk": pk}
            yield response.follow(url = f"https://www.ratemyprofessors.com/ShowRatings.jsp?tid={pk['pk_id']}&showMyProfs=true", callback = self.parse_prof)
            # break

    def parse_prof(self, response):
        yield {
            "url": response.url, 
            "id": re.search("tid=([0-9]+)", response.url).group(1),
            "type": "instructor",
            "source": "ratemyprofessor",
            # "html": response.body_as_unicode(),
            "name": response.css("div.cjgLEI ::text").extract(),
            "department": response.css("div.wVnqu ::text").extract()[1],
            "school": response.css("div.wVnqu ::text").extract()[5],
            "teach": sorted(set(response.css("div.RatingHeader__StyledClass-sc-1dlkqw1-2.hBbYdP ::text").extract())),
        }

if __name__ == '__main__':

    settings = dict()
    settings['USER_AGENT'] = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    settings['LOG_LEVEL'] = 'INFO'
    settings['LOG_ENABLED'] = True
    settings['ITEM_PIPELINES'] = {
        '__main__.JsonWriterPipeline': 300}

    process = CrawlerProcess(settings=settings)

    process.crawl(RateMyProfessor_Spider)
    process.start()