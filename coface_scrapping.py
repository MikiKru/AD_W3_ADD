import bs4
import pandas as pd
import lxml
import html5lib
# 1. Skrapowanie strony: https://www.coface.com/Economic-Studies-and-Country-Risks/Comparative-table-of-country-assessments
# 2. Dwa podejścia bs4 i pd
import requests


class CountryRisk:
    def __init__(self, country, ref, area, risk, climate):
        self.country = country
        self.ref = ref
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

        tables = html.find_all('table', attrs={'class' : 'eval_tab'})   # lista 6 tabel
        headers = []
        data = []
        refs = []
        countries = []
        for i,t in enumerate(tables):
            headers.append(str(tables[i].findAll('th'))\
                .replace('</th>','')\
                .replace('[<th class="country">','')\
                .replace('<th class="old_eval">\n','')\
                .replace('<th class="new_eval">\n','')\
                .replace(']','').split(', '))
            tableMarkerA = tables[i].findAll('a')
            for index, a in enumerate(tableMarkerA):
                self.countryRisks.append(CountryRisk(
                    str(a).replace('</a>', '').split('">')[1],
                    str(a).replace('<a href="', '').split('">')[0],
                    headers[i][0],
                    "X",
                    "X"))
            # print(tables[i].findAll('span'))
        for cs in self.countryRisks:
            print(cs)


cs = CofaceScrapping()      # utworzenie obiektu i wywołanie konstruktora domyślnego
# cs.getTablesByPandas()      # wywołanie metody
cs.getHtmlCodeByBs4()
# cs.printResults()
