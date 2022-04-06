# ScrapyAlbumReviews
Album Review parser from Exclaim and Rollingstone using Scrapy

Dependencies and virtualenv managed with pipenv

> pip install pipenv
> pipenv --install
> pipenv shell

scrapy crawl rollingstone -o rs_reviews.csv

Can now all use Docker.

> docker compose run --rm app
