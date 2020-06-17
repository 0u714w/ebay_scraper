from django.shortcuts import render, HttpResponseRedirect
import pandas as pd
import requests
import getpass
from bs4 import BeautifulSoup
from multiply.forms import SearchForm
from multiply.models import GenericFile
from services import helpers
import re


def create_csv_sold(keyword):
    item_name = []
    prices = []
    average_price = []
    prices_stripped = []
    outliers = []
    url = "https://www.ebay.com/sch/i.html?_from=R40&_nkw={}&_in_kw=1&_ex_kw=&_sacat=0&LH_Sold=1&_udlo=&_udhi=&_samilow=&_samihi=&_sadis=15&_stpos=46201&_sargn=-1%26saslc%3D1&_salic=1&_sop=12&_dmd=1&_ipg=50&LH_Complete=1&_fosrp=1".format(keyword)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    listings = soup.find_all('li')
    for listing in listings:
        prod_name = " "
        prod_price = " "
        for name in listing.find_all('a', attrs={'class': "vip"}):
            if(str(name.find(text=True, recursive=False)) != "None"):
                prod_name = str(name.find(text=True, recursive=False))
                item_name.append(prod_name)
            if(prod_name != " "):
                price = listing.find('span', attrs={'class': "bold bidsold"})
                price_to = listing.find('span', attrs={'class': "prRange"})
                prod_price = str(price.find(text=True, recursive=False))
                match = re.search(r'\b\$?[\d,.]+\b', str(prod_price))
                match_2 = re.search(r'\b\$?[\d,.]+\b', str(price_to))
                if match_2 == 'None':
                    pass
                elif match_2:
                    prices.append(str(match_2.group()))
                if match:
                    prices.append(str(match.group()))

    for i in prices:
        prices_stripped.append(int(float(i.replace('$', '').replace(',', '').replace('None', '0'))))

    for num in range(len(prices)):
        average_price.append(str(round(helpers.generate_average(prices), 2)))
        outliers.append(helpers.detect_outlier(prices_stripped))

    if len(average_price) < len(outliers):
        average_price.append(helpers.generate_average(prices_stripped))

    username = getpass.getuser()
    chart = pd.DataFrame({"Name": item_name, "Prices": prices, "Average Price": helpers.remove_outlier_from_average(outliers, average_price), "Outliers": outliers})
    chart.to_csv(r'/Users/{}/Desktop/{}_sold.csv'.format(username, keyword), index=False)


def create_csv_active(keyword):
    item_name = []
    prices = []
    average_price = []
    prices_stripped = []
    outliers = []
    url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1311.R1.TR12.TRC2.A0.H0.X&_nkw={}&_sacat=0".format(keyword)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    listings = soup.find_all('li', attrs={'class': 's-item'})
    for listing in listings:
        prod_name = " "
        prod_price = " "
        for name in listing.find_all('h3', attrs={'class': "s-item__title"}):
            if(str(name.find(text=True, recursive=False)) != "None"):
                prod_name = str(name.find(text=True, recursive=False))
                item_name.append(prod_name)
            if(prod_name != " "):
                price = listing.find('span', attrs={'class': "s-item__price"})
                prod_price = str(price.find(text=True, recursive=False))
                prices.append(prod_price)

    for i in prices:
        prices_stripped.append(int(float(i.replace('$', '').replace(',', '').replace('None', '0'))))

    for num in range(len(prices)):
        average_price.append(str(round(helpers.generate_average(prices), 2)))
        outliers.append(helpers.detect_outlier(prices_stripped))

    if len(average_price) < len(outliers):
        average_price.append(helpers.generate_average(prices_stripped))

    username = getpass.getuser()
    chart = pd.DataFrame({"Name": item_name, "Prices": prices, "Average Price": helpers.remove_outlier_from_average(outliers, average_price), "Outliers": outliers})
    chart.to_csv(r'/Users/{}/Desktop/{}_active.csv'.format(username, keyword), index=False)


def homepage(request):
    html = "homepage.html"
    form = SearchForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data
            active_url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1311.R1.TR12.TRC2.A0.H0.X&_nkw={}&_sacat=0".format(data['search'])
            sold_url = "https://www.ebay.com/sch/i.html?_from=R40&_nkw={}&_in_kw=1&_ex_kw=&_sacat=0&LH_Sold=1&_udlo=&_udhi=&_samilow=&_samihi=&_sadis=15&_stpos=46201&_sargn=-1%26saslc%3D1&_salic=1&_sop=12&_dmd=1&_ipg=50&LH_Complete=1&_fosrp=1".format(data['search'])
            if data['download_csv_sold'] is True and data['download_csv_active'] is True:
                create_csv_active(data['search'])
                create_csv_sold(data['search'])
                GenericFile.objects.create(title=data['search'])
                return HttpResponseRedirect('/')
            elif data['download_csv_sold'] is True:
                create_csv_sold(data['search'])
                GenericFile.objects.create(title=data['search'])
                return HttpResponseRedirect(sold_url)
            elif data['download_csv_active'] is True:
                create_csv_active(data['search'])
                GenericFile.objects.create(title=data['search'])
                return HttpResponseRedirect(active_url)
            else:
                GenericFile.objects.create(title=data['search'])
                return HttpResponseRedirect(active_url)
        else:
            form = SearchForm()

    return render(request, html, {'form': form})


def history(request):
    html = "history.html"
    items = GenericFile.objects.all().order_by('created_date')
    return render(request, html, {'list': items})
