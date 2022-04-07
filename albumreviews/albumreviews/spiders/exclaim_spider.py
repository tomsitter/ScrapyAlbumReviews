import scrapy
import dateparser
from albumreviews.util import sanitize
import re

class ExclaimSpider(scrapy.Spider):
    name = "exclaim"
    start_urls = [
        'https://exclaim.ca/all/album',
    ]

    def parse(self, response):
        for review in response.css('li.streamItem>article>a::attr(href)'):
            yield response.follow(review, callback=self.parse_review)
           
        # next_page_url = next_page(response.url)
        next_page = response.css('div.pull-right>strong>a::attr(href)').get()
        if next_page is not None:
            # will automatically extract href attribute and works with relative urls
            yield response.follow(next_page, callback=self.parse)

    def parse_review(self, response):

        date = dateparser.parse(
            response.css("div.article-published::text").get()[10:]
        )

        author = response.css("div.article-author>a::text").get()
        rating = response.css("div.article-rating::text").get(default="")
        title = response.css("span.article-title::text").get()
        album = response.css("span.article-subtitle::text").get()
        # This will get all text, including title, data publish, author, review
        # We will filter out everything before the review by finding the
        # rating (the first element returned that is just a number)
        review = response.css("div.article ::text").getall()
        for i, text in enumerate(review):
            if text.isnumeric():
                review = review[i+1:]
                break

        tags = response.css("li.filters-selected-item>a::text").getall()

        # if rating != "":
        #     review = re.split('(\n[0-9]\n)', review)[2]
        # review = re.split('(\([^()]+\)\n\n)', review)[0]
        review = sanitize(' '.join(review))

        yield {
            "date": date.strftime("%Y-%m-%d"),
            "author": author,
            "rating": rating,
            "tags": tags,
            "title": title,
            "album": album,
            "review": review,
            "url": response.url
        }
    

def next_page(url):
    """Given a URL for a page of album reviews, return the next page"""
    current_page = re.search('page/(\d+)$', url)
    if not current_page:
        return url + '/page/2'
    page_number = current_page.groups()[0]
    page_digits = len(page_number)
    return url[:-page_digits] + str(int(page_number) + 1)
