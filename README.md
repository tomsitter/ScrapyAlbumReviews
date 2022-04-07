# Scrapy Album Reviews Scraper

Album Review parser from Exclaim and Rollingstone using Scrapy

## Install dependencies

Dependencies and virtualenv managed with pipenv

```
> pip install pipenv
> pipenv --install
> pipenv shell
```
or with Docker:
```
> docker compose run albumreviews
```


## Running
```
> scrapy crawl rollingstone -o rs_reviews.csv
> scrapy crawl exclaim -o exclaim_reviews.csv
```

Produces a CSV with the following contents: date, author, rating, tags, title, and review text, and URL
