# Scrapy Album Reviews Scraper

Album Review parser from Exclaim and Rollingstone using Scrapy

## Install dependencies

With pip
```
> python3 -m venv .venv
> pip install -r requirements.txt
```

With pipenv

```
> pipenv install
> pipenv shell
```

With Docker:
```
> docker compose run albumreviews
```

## Running
```
> cd albumreviews
> scrapy crawl rollingstone -o rs_reviews.csv
> scrapy crawl exclaim -o exclaim_reviews.csv
```

Produces a CSV with the following contents: date, author, rating, tags, title, review text, and review URL
