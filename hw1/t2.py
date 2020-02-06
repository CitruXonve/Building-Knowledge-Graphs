import scrapy
import re
from time import time
from datetime import datetime

class ImdbSpider(scrapy.Spider):
    name = 'imdbspider'
    start_urls = [
        'https://www.imdb.com/search/title/?genres=romance&start=1&ref_=adv_nxt',
        'https://www.imdb.com/search/title/?genres=romance&start=51&ref_=adv_nxt',
        'https://www.imdb.com/search/title/?genres=romance&start=101&ref_=adv_nxt',
        'https://www.imdb.com/search/title/?genres=romance&start=151&ref_=adv_nxt',
        'https://www.imdb.com/search/title/?genres=romance&start=201&ref_=adv_nxt',
        'https://www.imdb.com/search/title/?genres=romance&start=251&ref_=adv_nxt',
        'https://www.imdb.com/search/title/?genres=romance&start=301&ref_=adv_nxt',
        'https://www.imdb.com/search/title/?genres=romance&start=351&ref_=adv_nxt',
        'https://www.imdb.com/search/title/?genres=romance&start=401&ref_=adv_nxt',
    ]
    custom_settings = {
        'CONCURRENT_REQUESTS': 5,
        'CLOSESPIDER_ITEMCOUNT': 401,
        # 'DEPTH_LIMIT': 2
    }

    def parse(self, response):
        for movie in response.css('.lister-item-header>a::attr("href")'):
            movie_url = response.urljoin(movie.get()) # relative url to absolute
            # yield {'movie': movie_url}
            if movie_url is not None:
                request = scrapy.Request(url=movie_url, callback=self.parseMovie)
                yield request

        # next_page = response.css('a.next-page::attr("href")').get()
        # if next_page is not None:
        #     yield response.follow(url=response.urljoin(next_page), callback=self.parse)
    
    def parseMovie(self, response):
        if response is not None:
            release_date = re.sub('<[^>]*>', '', response.xpath('//div[@class="txt-block"][.//text()[contains(., "Release Date")]]').get(default=''))
            budget = re.sub('<[^>]*>', '', response.xpath('//div[@class="txt-block"][.//text()[contains(., "Budget")]]').get(default=''))
            gross_usa = re.sub('<[^>]*>', '', response.xpath('//div[@class="txt-block"][.//text()[contains(., "Gross USA")]]').get(default=''))
            runtime = re.sub('<[^>]*>', '', response.xpath('//div[@class="txt-block"][.//text()[contains(., "Runtime")]]').get(default=''))
            # yield {
            #     # 'id': re.findall('/tt([0-9]+)/', response.url)[0],
            #     'title': response.css('.title_wrapper>h1::text').get(default='').strip(),
            #     # 'url': response.url,
            #     # 'timestamp_crawl': datetime.now().isoformat(),
            #     'release_date': 
            #     re.search(r'Release Date:\s*(\w+\s*\w+\s*\w+)', release_date).group(1).strip() if re.search(r'Release Date:\s*(\w+\s*\w+\s*\w+)', release_date) else '',
            #     'budget': re.search(r'Budget:\s*(\S+)', budget).group(1).strip() if re.search(r'Budget:\s*(\S+)', budget) else '',
            #     'gross_usa': re.search(r'Gross USA:\s*(\S+)', gross_usa).group(1).strip() if re.search(r'Gross USA:\s*(\S+)', gross_usa) else '',
            #     'runtime': re.search(r'Runtime:\s*(\w+\s*\w+)', runtime).group(1).strip() if re.search(r'Runtime:\s*(\w+\s*\w+)', runtime) else ''
            # }
            yield {'output': [
                response.url,
                response.css('.title_wrapper>h1::text').get(default='').strip(),
                # 'timestamp_crawl': datetime.now().isoformat(),
                re.search(r'Release Date:\s*(\w+\s*\w+\s*\w+)', release_date).group(1).strip() if re.search(r'Release Date:\s*(\w+\s*\w+\s*\w+)', release_date) else '',
                re.search(r'Budget:\s*(\S+)', budget).group(1).strip() if re.search(r'Budget:\s*(\S+)', budget) else '',
                re.search(r'Gross USA:\s*(\S+)', gross_usa).group(1).strip() if re.search(r'Gross USA:\s*(\S+)', gross_usa) else '',
                re.search(r'Runtime:\s*(\w+\s*\w+)', runtime).group(1).strip() if re.search(r'Runtime:\s*(\w+\s*\w+)', runtime) else '']}
            pass

#> scrapy runspider t1_1.py -o t1_1.jl --nolog