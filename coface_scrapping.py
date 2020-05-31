import pandas as pd
import lxml
import html5lib
# 1. Skrapowanie strony: https://www.coface.com/Economic-Studies-and-Country-Risks/Comparative-table-of-country-assessments
# 2. Dwa podejścia bs4 i pd

class CountryRisk:
    def __init__(self, country, area, risk, climate):
        self.country = country
        self.area = area
        self.risk = risk
        self.climate = climate
class CofaceScrapping:
    def __init__(self):
        print("Jestem w kontruktorze")
        pass
    def getTablesByPandas(self):
        # pobieramy tabele z html do listy coface
        coface = pd.read_html(
                'https://www.coface.com/Economic-Studies-and-Country-Risks/Comparative-table-of-country-assessments')
        for c in coface:
            print(c)
    def getHtmlCodeByBs4(self):
        pass



cs = CofaceScrapping()      # utworzenie obiektu i wywołanie konstruktora domyślnego
cs.getTablesByPandas()      # wywołanie metody
