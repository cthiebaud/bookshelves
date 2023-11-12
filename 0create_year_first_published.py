import json

goodreads = {}
goodreads_dictionnary = {}

min = 100000 # very large
max = 0
min_title = None
max_title = None

with open('/Users/christophe.thiebaud/github.com/goodreads-scraper/QWE/all_books.json', 'r') as fp:
    goodreads = json.load(fp)

    for book in goodreads:
        key = book["book_id_title"]
        year = book["year_first_published"]
        if not year is None:
            if year < min : 
                min = year
                min_title = book["book_title"]
            if max  < year: 
                max = year
                max_title = book["book_title"]
        goodreads_dictionnary[key] = year

print(f"min year: {min}, [{min_title}];\nmax year: {max}, [{max_title}];\n{len(goodreads_dictionnary)}")

with open('year_first_published_from_goodreads.json', 'w') as fp:
  json.dump(goodreads_dictionnary, fp, indent=2)

