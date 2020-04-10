import scrapy, re
from urllib.parse import urljoin
import lxml.etree as ET

class USC_Class_Spider(scrapy.Spider):
    name = 'USCClassSpider'
    start_urls = ['https://classes.usc.edu/term-20201/classes/csci']
    course_urls = set()

    def parse(self, response):
        for course in response.xpath('//div[@class[contains(., "course-info")]]/@id').extract():
            full_url = urljoin('https://classes.usc.edu/term-20201/course/', course)
            yield response.follow(url = full_url, callback = self.parse_course)
            # yield {'url': full_url, 'abbr': course, 'type': 'course'}

    def parse_course(self, response):
        #(ET.fromstring(instructor).xpath('//a[@href]'), ET.fromstring(instructor).xpath('//a/text()'))
        instructor_list = [ET.fromstring(instructor) for instructor in response.xpath('//td[@class="instructor"]').extract()]
        for book in response.xpath('//td[@class="info"]/a/@href').extract():
            yield response.follow(url = book, callback = self.parse_book)

        yield {
            'url': response.url,
            'type': 'course',
            'abbr': response.url.split('/')[-1],
            'title': response.xpath('//div[@id="content-main"]/h2/text()').get(),
            'brief': response.xpath('//div[@class="course-table"]/div[@class="catalogue"]/text()').get(),
            'instructor': [__.xpath('//a/text()')[0] for __ in instructor_list],
        }

        for obj in instructor_list:
            yield {
                'type': 'instructor',
                'name': obj.xpath('//a/text()')[0],
                'link': obj.xpath('//a/@href')[0],
            }

    def parse_book(self, response):
        for book in response.xpath('//li[@class="books"]//ul/li').extract():
            text = re.split(r'<[^>]+>', book)

            yield {
                'type': 'textbook',
                'title': text[2].strip(),
                'author': text[1].strip(),
                'ISBN': text[6].strip(),
                'for': response.url.split('/')[-3].upper(),
            }