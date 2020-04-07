import scrapy, re

class USCSpider(scrapy.Spider):
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
                yield response.follow(url = full_url, callback = self.parse_program)
                yield result
        
        for course in self.course_urls():
            yield response.follow(url = course, callback = self.parse_course)

    def parse_program(self, response):
        course_list = []
        for course in response.css('li.acalog-course a'):
            course_attr = re.search('([0-9]+).*?([0-9]+)', course.css('a::attr("onclick")').get())
            if course_attr:
                course_composite_url = f'https://catalogue.usc.edu/preview_course.php?catoid={course_attr.group(1)}&coid={course_attr.group(2)}'
                # yield({
                #     'type': 'course', 
                #     'label': course.css('a ::text').get(),
                #     'url': course_composite_url,
                # })
                self.course_urls.add(course_composite_url)
                course_list.append(course_composite_url)

        yield {
            "url": response.url, 
            'type': 'program',
            'title': response.css('title ::text').get(),
            'description': response.css('table.table_default tr p:not(.acalog-breadcrumb) ::text').get(),
            'course': course_list,
        }
        pass

    def parse_course(self, response):
        yield {
            'title': response.css('h1#course_preview_title ::text').get(),
            'url': response.url,
            'type': 'course',
            'text': response.css('td.block_content_popup ::text').get(),
        }
        pass
