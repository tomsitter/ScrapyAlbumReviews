import scrapy
import dateparser
from albumreviews.util import sanitize
import re

class ExclaimSpider(scrapy.Spider):
    name = "exclaim"
    start_urls = [
        'http://exclaim.ca/music/reviews',
    ]

    def parse(self, response):
        for review in response.css('li.streamSingle-item'):
            yield response.follow(review, callback=self.parse_review)
           
        next_page_url = next_page(response.url)
        if next_page_url is not None:
            # will automatically extract href attribute and works with relative urls
            yield response.follow(next_page, callback=self.parse)

    def parse_review(self, response):

        date = dateparser.parse(
            response.css("div.article-published::text").extract_first()[10:]
        )

        author = response.css("div.article-author::text").extract_first()[3:]
        rating = response.css("div.article-rating::text").extract_first(default="")
        artist = response.css("span.article-title::text").extract_first()
        album = response.css("span.article-subtitle::text").extract_first()
        review = response.find("div.article::text").get_text()

        if rating != "":
            review = re.split('(\n[0-9]\n)', review)[2]
        review = re.split('(\([^()]+\)\n\n)', review)[0]
        review = sanitize(review)

        yield {
            "date": date.strftime("%Y-%m-%d"),
            "author": author,
            "rating": rating,
            "artist": artist,
            "album": album,
            "review": review,
        }
    

def next_page(url):
    """Given a URL for a page of album reviews, return the next page"""
    current_page = re.search('page/(\d+)$', url)
    if not current_page:
        return url + '/page/2'
    page_number = current_page.groups()[0]
    page_digits = len(page_number)
    return url[:-page_digits] + str(int(page_number) + 1)
