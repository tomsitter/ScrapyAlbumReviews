import scrapy
import dateparser
from albumreviews.util import sanitize

class RollingStoneSpider(scrapy.Spider):
    name = "rollingstone"
    start_urls = [
        'https://www.rollingstone.com/music/albumreviews',
    ]

    def parse(self, response):
        """Pull URLs to reviews"""
        for review in response.css('a.c-card__wrap::attr(href)').getall():
            yield response.follow(review, callback=self.parse_review)
           
        next_page = response.css('div.c-pagination.a::attr(href)').get()
        if next_page is not None:
            # will automatically extract href attribute and works with relative urls
            yield response.follow(next_page, callback=self.parse)

    def parse_review(self, response):
        """Pull data from individual review pages"""
        date = dateparser.parse(
            response.css("time::attr(datetime)").get(default="1900-01-01")
        )
        stars = [star.attrib["xlink:href"] for star in response.css("svg.c-rating__star--active>use")]
        if any("half" in star for star in stars):
            rating = len(stars) - 1.5
        else:
            rating = len(stars) - 1

        author = response.css("a.c-byline__link::text").get(default="null").strip()
        title = response.css("h1.l-article-header__row::text").get(default="null").strip()
        artists = response.css("a.c-tags__item::text").getall()
        review = sanitize(" ".join(
            response.css("div.pmc-paywall>p::text").getall()
        ))


        yield {
            "date": date.strftime("%Y-%m-%d"),
            "author": author,
            "rating": rating,
            "artist": artists,
            "title": title,
            "review": review,
        }
    