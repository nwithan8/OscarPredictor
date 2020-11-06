import json
import argparse
from lxml.html import fromstring
import requests
from itertools import cycle
import traceback
from bs4 import BeautifulSoup
import re
from data_collection import helpers

import imdb

im = imdb.IMDb()


def parse_box_office_ratings(page):
    highest_rank = None
    soup = BeautifulSoup(page.content, "html5lib")
    table = soup.find('table', attrs={'class': 'a-bordered a-horizontal-stripes a-size-base a-span12 mojo-body-table mojo-table-annotated'})
    if not table:
        return None
    ranks = table.find_all('td', attrs={'class': 'a-text-right mojo-field-type-rank mojo-sort-column'})
    if ranks:
        for rank in ranks:
            try:
                if not highest_rank or int(rank.string) < highest_rank:
                    highest_rank = int(rank.string)
            except:
                pass
    return highest_rank


def get_domestic_release(imdb_id):
    release_link = None
    url = f"https://www.boxofficemojo.com/title/tt{imdb_id}"
    page = requests.get(url, timeout=10)
    soup = BeautifulSoup(page.content, "html5lib")
    table = soup.find('table', attrs={'class': 'a-bordered a-horizontal-stripes a-size-base-plus'})
    if not table:
        return None
    rows = table.find_all('tr')
    if len(rows) > 0:
        for row in rows:
            column = row.find('td')
            if column:
                link = column.find('a')
                if link is not None and link['href'] is not None and link.string == 'Original Release':
                    release_link = link['href']
                    break
    if not release_link:
        return None
    url = f"https://www.boxofficemojo.com{release_link}"
    page = requests.get(url, timeout=10)
    soup = BeautifulSoup(page.content, "html5lib")
    table = soup.find('table', attrs={'class': 'a-bordered a-horizontal-stripes mojo-table releases-by-region'})
    if not table:
        return None
    rows = table.find_all('tr')
    if len(rows) > 0:
        for row in rows:
            column = row.find('td')
            if column:
                link = column.find('a')
                if link is not None and link['href'] is not None and link.string == 'Domestic':
                    release_link = link['href']
                    break
    if not release_link:
        return None
    release_link = f"{release_link.split('?')[0]}weekend?sort=rank&sortDir=asc"
    url = f"https://www.boxofficemojo.com{release_link}"
    return requests.get(url, timeout=10)


while True:
    movieId = None
    name = input(f"Movie title: ")
    year = input(f"Movie year: ")
    if int(year) > 2020:
        print("Typo in year")
        pass
    else:
        results = im.search_movie(name)
        if results:
            for this_movie in results:
                if (int(year) - 1) < this_movie.data['year'] < (int(year) + 1):
                    print(f"Using {this_movie.data['title']} ({this_movie.data['year']})...")
                    movieId = this_movie.movieID
                    break
            html = get_domestic_release(movieId)
            if html:
                rank = parse_box_office_ratings(html)
                if rank:
                    print(f"Highest box office ranking: {rank}")
                else:
                    print("Could not find box office rankings.")
            else:
                print("Could not parse movie page.")
        else:
            print("Could not find movie.")
