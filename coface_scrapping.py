import pandas as pd
import lxml
import html5lib
# 1. Skrapowanie strony: https://www.coface.com/Economic-Studies-and-Country-Risks/Comparative-table-of-country-assessments
# 2. Dwa podejścia bs4 i pd

# definicja klasy
class CofaceScrapping:
    def __init__(self):
        print("Jestem w kontruktorze")
        pass
    def getTablesByPandas(self):
        coface = pd.read_html(
                'https://www.coface.com/Economic-Studies-and-Country-Risks/Comparative-table-of-country-assessments')
        index = 0
        print(len(coface))
        while(len(coface)):
            print("TABELA "+ str(index + 1))
            coface = pd.read_html(
                'https://www.coface.com/Economic-Studies-and-Country-Risks/Comparative-table-of-country-assessments')[index]
            index += 1
            print(coface)
    def getHtmlCodeByBs4(self):
        pass


cs = CofaceScrapping()      # utworzenie obiektu i wywołanie konstruktora domyślnego
cs.getTablesByPandas()      # wywołanie metody
