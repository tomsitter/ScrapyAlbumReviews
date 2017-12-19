""" Review class holds formatted data from scraped album reviews.
"""
import datetime
import html


def sanitize(review):
        return html.unescape(review).replace('\n', ' ').replace('\t', ' ').replace('\r', ' ').strip()