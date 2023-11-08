import json

goodreads = {}
goodreads_dictionnary = {}

min = 2024
max = 0

with open('/Users/christophe.thiebaud/github.com/goodreads-scraper/QWE/all_books.json', 'r') as fp:
    goodreads = json.load(fp)

    for book in goodreads:
        key = book["book_id_title"]
        year = book["year_first_published"]
        if not year is None:
            if year < min : min = year
            if max  < year: max = year
        goodreads_dictionnary[key] = year

print(min, max)

with open('year_first_published.json', 'w') as fp:
  json.dump(goodreads_dictionnary, fp, indent=2)

