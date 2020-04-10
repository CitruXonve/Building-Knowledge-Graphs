import scrapy, re

class USC_Catalogue_Spider(scrapy.Spider):
    name = 'USCCatalogueSpider'
    start_urls = ['https://catalogue.usc.edu/content.php?catoid=11&navoid=3756']
    course_urls = set()

    def parse(self, response):
        for program in response.css('td.block_content_outer>table.table_default a'):
            full_url = response.urljoin(program.css('a::attr("href")').get())
            if re.search('preview_program\.php', full_url):
                result = {
                    'label': program.css('a ::text').get(), 
                    'url': full_url, 
                    'type': 'program',
                }
                if re.search('Computer Science', result['label']):
                    yield response.follow(url = full_url, callback = self.parse_program)
                    yield result

    def parse_program(self, response):
        course_list = []
        for course in response.css('li.acalog-course a'):
            course_attr = re.search('([0-9]+).*?([0-9]+)', course.css('a::attr("onclick")').get())
            if course_attr:
                course_composite_url = f'https://catalogue.usc.edu/preview_course.php?catoid={course_attr.group(1)}&coid={course_attr.group(2)}'

                if not course_composite_url in self.course_urls:
                    yield response.follow(url = course_composite_url, callback = self.parse_course)
                    self.course_urls.add(course_composite_url)
                    pass

                course_list.append('-'.join(course.css('::text').get().split()[:2]))

        yield {
            "url": response.url, 
            'type': 'program',
            'title': response.css('title ::text').get(),
            'description': response.css('table.table_default tr p:not(.acalog-breadcrumb) ::text').get(),
            'course': course_list,
        }
        pass

    def parse_course(self, response):
        text = response.xpath('//td[@class="block_content_popup"][.//text()]').get(default='')
        yield {
            'title': response.css('h1#course_preview_title ::text').get(),
            'url': response.url,
            'type': 'course',
            'description': text,
        }
        pass
