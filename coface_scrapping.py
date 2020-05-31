from time import time

import bs4
import pandas as pd
import lxml
import html5lib
# 1. Skrapowanie strony: https://www.coface.com/Economic-Studies-and-Country-Risks/Comparative-table-of-country-assessments
# 2. Dwa podejścia bs4 i pd
import pymysql
import requests
import xlsxwriter
import matplotlib
import matplotlib.pyplot as plt


class CountryRisk:
    def __init__(self, country, ref, area, risk, climate):
        self.country = country
        self.ref = ref
        self.area = area
        self.risk = risk
        self.climate = climate
    def __str__(self):
        return "%s; %s; %s; %s; %s" % (self.country, self.ref, self.area, self.risk, self.climate)
class CofaceScrapping:
    def __init__(self):
        self.countryRisks = []
        self.area = {0 : "Africa", 1 : "America", 2 : "Asia", 3 : "CIS", 4 : "Europe", 5 : "Middle-East"}
    def getTablesByPandas(self):
        # pobieramy tabele z html do listy coface
        coface = pd.read_html(
                'https://www.coface.com/Economic-Studies-and-Country-Risks/Comparative-table-of-country-assessments')
        for c in coface:
            print(c)
    def getHtmlCodeByBs4(self):
        page = requests.get('https://www.coface.com/Economic-Studies-and-Country-Risks/Comparative-table-of-country-assessments')
        html = bs4.BeautifulSoup(page.content, 'html.parser')
        tables = html.find_all('table', attrs={'class' : 'eval_tab'})   # lista 6 tabel
        headers = []
        for i,t in enumerate(tables):
            headers.append(str(tables[i].findAll('th'))\
                .replace('</th>','')\
                .replace('[<th class="country">','')\
                .replace('<th class="old_eval">\n','')\
                .replace('<th class="new_eval">\n','')\
                .replace(']','').split(', '))
            tableMarkerA = tables[i].findAll('a')
            tableMarkerTd = tables[i].findAll('td',attrs={'class' : 'eval'})
            tableTd = []
            for index, value in enumerate(tableMarkerTd):
                tableTd.append(str(tableMarkerTd[index])\
                    .replace('<td class="eval">', '')\
                    .replace('<span class="value">', '')\
                    .replace('</span>', '')\
                    .replace('</td>', '').strip())
            risks = tableTd[::2]      # nieparzyste
            climates = tableTd[1::2]  # parzyste
            for index, a in enumerate(tableMarkerA):
                self.countryRisks.append(CountryRisk(
                    str(a).replace('</a>', '').split('">')[1],
                    "https://www.coface.com/" + str(a).replace('<a href="', '').split('">')[0],
                    headers[i][0],
                    risks[index],
                    climates[index]))
    def printResults(self):
        for cs in self.countryRisks:
            print(cs)

class ExportController(CofaceScrapping):
    def exportToXlsx(self):
        tableTitle = [
            "COUNTRY",
            "REFERENCE LINK",
            "GEOGRAPHICAL AREA",
            "COUNTRY RISK ASSESSMENT",
            "BUSINESS CLIMATE ASSESSMENT"]
        workbook = xlsxwriter.Workbook('BusinessRisks.xlsx')    # utworzenie pliku excel
        worksheet = workbook.add_worksheet()                    # utworzenie arkusz
        tableFormat = workbook.add_format({'border': 1})
        headerFormat = workbook.add_format({'bold': True, 'bg_color': 'yellow', 'border': 1})
        worksheet.set_column(0, 0, 40)
        worksheet.set_column(1, 1, 100)
        worksheet.set_column(2, 2, 20)
        worksheet.set_column(3, 5, 40)

        row = 0
        column = 0
        while(column < len(tableTitle)):
            worksheet.write(row, column, tableTitle[column], headerFormat)
            column += 1
        row = 1
        while(row - 1 < len(self.countryRisks)):        # pętla iterująca po wierszach
            column = 0
            while(column < len(tableTitle)):    # pętla iterująca po kolumnach
                worksheet.write(row, column, str(self.countryRisks[row - 1]).split("; ")[column], tableFormat)
                column += 1
            row += 1
        workbook.close()
    def exportToDatabase(self):
        conn = pymysql.connect("localhost", "root", "miki123", "tm_db")
        self.c = conn.cursor()
        conn.autocommit(True)
        # utworzenie tabelki SQL
        self.c.execute("DROP TABLE business_risk");
        self.c.execute("CREATE TABLE business_risk ("
                  "risk_id int primary key auto_increment, "
                  "country varchar(255), "
                  "reflink varchar(512), "
                  "geolocation varchar(255), "
                  "risk varchar(5), "
                  "climate varchar(5)"
                  ")")
        for row in self.countryRisks:
            self.c.execute("INSERT INTO business_risk VALUES (default, %s,%s,%s,%s,%s)",
                      (row.country, row.ref, row.area, row.risk, row.climate))
    def generatePlots(self):
        self.c.execute("SELECT country, geolocation, risk, climate FROM business_risk")
        businessRisk = self.c.fetchall()
        risk_df = pd.DataFrame(businessRisk, columns=['country','area','risk','climate'])
        counties = risk_df['country'].tolist()[:5]
        areas = risk_df['area'].tolist()[:5]
        risks = risk_df['risk'].tolist()[:5]
        climates = risk_df['climate'].tolist()[:5]
        categories = {"A1" : 1, "A2" : 2, "A3" : 3, "A4" : 4, "B" : 5, "C" : 6, "D" : 7, "E" : 8}
        x = pd.np.arange(len(counties))  # the label locations
        width = 0.35  # the width of the bars
        risks_cat = []
        climates_cat = []
        for v in risks:
            risks_cat.append(categories[v])
        for v in climates:
            climates_cat.append(categories[v])
        fig, ax = plt.subplots()
        rects1 = ax.bar(x - width / 2, risks_cat, width, label='Business Risk Asesm.')
        rects2 = ax.bar(x + width / 2, climates_cat, width, label='Business Climate Asesm.')
        ax.set_ylabel('Categories')
        ax.set_title('Business risk & climate assesments')
        ax.set_xticks(x)
        ax.set_xticklabels(counties)
        ax.legend()
        fig.tight_layout()
        plt.show()

    def generatePieChart(self):
        self.c.execute("SELECT climate, 100*(count(*)/(SELECT count(*) FROM business_risk)) "
                       "FROM business_risk GROUP BY climate ORDER climate")
        result = self.c.fetchall()
        agg_df = pd.DataFrame(result, columns=['climate', 'count'])
        climates = agg_df['climate'].tolist()
        contribution = agg_df['count'].tolist()

        


cs = ExportController()      # utworzenie obiektu i wywołanie konstruktora domyślnego
# cs.getTablesByPandas()      # wywołanie metody
cs.getHtmlCodeByBs4()
cs.printResults()
cs.exportToXlsx()
cs.exportToDatabase()
cs.generatePlots()