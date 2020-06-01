from django.shortcuts import render, HttpResponseRedirect
import pandas as pd
import numpy as np
import requests
import getpass
from bs4 import BeautifulSoup
from multiply.forms import SearchForm
from multiply.models import GenericFile


def create_csv(keyword):
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
        average_price.append(str(round(generate_average(prices), 2)))
        outliers.append(detect_outlier(prices_stripped))

    username = getpass.getuser()
    chart = pd.DataFrame({"Name": item_name, "Prices": prices, "Average Price": average_price, "Outliers": outliers})
    chart.to_csv(r'/Users/{}/Desktop/{}.csv'.format(username, keyword), index=False)


def generate_average(list_to_average):
    sum_num = 0
    for i in list_to_average:
        if i == 'None':
            i = 0
        else:
            sum_num = sum_num + int(float(i.replace('$', '').replace(',', '')))
    avg = sum_num / len(list_to_average)
    return avg


def detect_outlier(data_1):
    outliers = []
    threshold = 3
    mean_1 = np.mean(data_1)
    std_1 = np.std(data_1)
    
    for y in data_1:
        z_score = (y - mean_1) / std_1 
        if np.abs(z_score) > threshold:
            outliers.append(y)
    return outliers

def homepage(request):
    html = "homepage.html"
    form = SearchForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data
            ebay_url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1311.R1.TR12.TRC2.A0.H0.X&_nkw={}&_sacat=0".format(data['search'])
            if data['download_csv'] is True:
                create_csv(data['search'])
                GenericFile.objects.create(title=data['search'])
                return HttpResponseRedirect(ebay_url)
            else:
                GenericFile.objects.create(title=data['search'])
                return HttpResponseRedirect(ebay_url)
        else:
            form = SearchForm()

    return render(request, html, {'form': form})


def history(request):
    html = "history.html"
    items = GenericFile.objects.all().order_by('title')
    return render(request, html, {'list': items})
