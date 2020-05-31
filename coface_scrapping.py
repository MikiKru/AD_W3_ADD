import bs4
import pandas as pd
import lxml
import html5lib
# 1. Skrapowanie strony: https://www.coface.com/Economic-Studies-and-Country-Risks/Comparative-table-of-country-assessments
# 2. Dwa podejścia bs4 i pd
import requests


class CountryRisk:
    def __init__(self, country, area, risk, climate):
        self.country = country
        self.area = area
        self.risk = risk
        self.climate = climate
    def __str__(self):
        return "%s, %s, %s, %s" % (self.country, self.area, self.risk, self.climate)
class CofaceScrapping:
    def __init__(self):
        print("Jestem w kontruktorze")
        self.countryRisks = []
        self.area = {0 : "Africa", 1 : "America", 2 : "Asia", 3 : "CIS", 4 : "Europe", 5 : "Middle-East"}
        pass
    def getTablesByPandas(self):
        # pobieramy tabele z html do listy coface
        coface = pd.read_html(
                'https://www.coface.com/Economic-Studies-and-Country-Risks/Comparative-table-of-country-assessments')
        for c in coface:
            print(c)
    # def printResults(self):
    #     for i in self.countryRisks.index:
    #         print(self.countryRisks['Country risk assessment'][i])
    def getHtmlCodeByBs4(self):
        page = requests.get('https://www.coface.com/Economic-Studies-and-Country-Risks/Comparative-table-of-country-assessments')
        html = bs4.BeautifulSoup(page.content, 'html.parser')

        # headers = html.find_all('th', attrs={'class' : 'country'})
        rows = html.find_all('tr')
        # print(headers)
        print(rows)
        # print(len(headers))

cs = CofaceScrapping()      # utworzenie obiektu i wywołanie konstruktora domyślnego
cs.getTablesByPandas()      # wywołanie metody
cs.getHtmlCodeByBs4()
# cs.printResults()
