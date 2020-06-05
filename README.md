# Ebay Scraper

This program is designed to scrape active Ebay listings and create a .csv file containing data from the search. The .csv has four columns which are as follows: product name, price, average price of listings, and outliers.

![](images/main.png)
![](images/csv.png)


## Usage

Clone this repo
```
git clone https://github.com/dougenas/ebay_scraper.git
```

Start up your shell
```
pipenv shell
```

Migrate your database
```
python3 manage.py migrate
```

Run the server
```
python3 manage.py runserver
```

### Meta
[https://github.com/dougenas/ebay_scraper](https://github.com/dougenas/)
