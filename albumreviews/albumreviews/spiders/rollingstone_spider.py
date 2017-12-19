import scrapy
import dateparser
from albumreview.util import sanitize

class RollingStoneSpider(scrapy.Spider):
    name = "rollingstone"
    start_urls = [
        'http://www.rollingstone.com/music/albumreviews',
    ]

    def parse(self, response):
        """Pull URLs to reviews"""
        for review in response.css('a.content-card-link'):
            yield response.follow(review, callback=self.parse_review)
           
        next_page = response.css('a.load-more::attr(href)').extract_first()
        if next_page is not None:
            # will automatically extract href attribute and works with relative urls
            yield response.follow(next_page, callback=self.parse)

    def parse_review(self, response):
        """Pull data from individual review pages"""
        date = dateparser.parse(
            response.css("time.content-published-date::text").extract_first(default="1900-01-01")
        )

        author = response.css("a.content-author::text").extract_first(default="Not Found").strip()

        title = response.css("h1.content-title::text").extract_first(default="Not Found")

        if title.startswith("Review:"):
            title = title.lstrip("Review:")
        artist, album = title.strip(), ""
        
        review = sanitize(" ".join(
            response.css("div.article-content p::text").extract()
        ))

        stars = response.css("span.percentage.full").extract()
        half_stars = response.css("span.percentage.half").extract()
        rating = len(stars) + (len(half_stars) * 0.5)

        yield {
            "date": date.strftime("%Y-%m-%d"),
            "author": author,
            "rating": rating,
            "artist": artist,
            "album": album,
            "review": review,
        }
    