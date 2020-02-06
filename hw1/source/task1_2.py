import scrapy
import re
from time import time
from datetime import datetime

class ImdbSpider(scrapy.Spider):
    name = 'imdbspider'
    # start_urls = ['https://www.imdb.com/search/name/?gender=male,female']
    start_urls = ['https://www.imdb.com/search/name/?death_date=1990-01-01,&gender=male,female']
    custom_settings = {
        'CONCURRENT_REQUESTS': 5,
        'CLOSESPIDER_ITEMCOUNT': 5001,
        # 'DEPTH_LIMIT': 2
    }

    def parse(self, response):
        for cast_dom in response.css('.lister-item-content'):
            identity_dom = re.sub('<[^>]*>', '',cast_dom.css('p.text-small').get(default=''))
            identity = re.search('(\w+)', identity_dom).group(1) if re.search('(\w+)', identity_dom) else ''

            if identity == 'Actor' or identity == 'Actress':
                cast_url = response.urljoin(cast_dom.css('h3>a::attr(href)').get(default=''))

                request = scrapy.Request(url=cast_url, callback=self.parseCast)
                yield request

        next_page = response.css('a.next-page::attr("href")').get()
        if next_page is not None:
            yield response.follow(url=response.urljoin(next_page), callback=self.parse)
    
    def parseCast(self, response):
        if response is not None:
            birth = re.sub('\s+',' ', 
                re.sub('<[^>]*>', '', 
                    response.xpath('//div[@id="name-born-info"]').get(default='').strip()
                )
            )
            death = re.sub('\s+',' ', 
                re.sub('<[^>]*>', '', 
                    response.css('#name-death-info').get(default='').strip()
                )
            )
            yield {
                'id': re.findall('/nm([0-9]+)', response.url)[0],
                'url': response.url,
                'timestamp_crawl': datetime.now().isoformat(),
                'name': response.css('#name-overview-widget-layout h1 span.itemprop::text').get(default='').strip(),
                'date_of_birth': re.search(r'Born: (.+) in (.+)', birth).group(1).strip() if re.search(r'Born: (.+) in (.+)', birth) is not None else '',
                'place_of_birth': re.search(r'Born: (.+) in (.+)', birth).group(2).strip() if re.search(r'Born: (.+) in (.+)', birth) is not None else '',
                'date_of_death': re.search(r'Died: (.+) \(.+\) in (.+)', death).group(1).strip() if re.search(r'Died: (.+) \(.+\) in (.+)', death) is not None else '',
                'place_of_death': re.search(r'Died: (.+) \(.+\) in (.+)', death).group(2).strip() if re.search(r'Died: (.+) \(.+\) in (.+)', death) is not None else '',
            }
            pass

#> scrapy runspider t1_1.py -o t1_1.jl -t json 2> log.txt