import requests
from bs4 import BeautifulSoup
import html5lib
import lxml
import csv
import re
import datetime

"""
    Scrape data from 4D Website. 
    1. User inputs website to scrape into URL 
    2. File will be saved according to the Drawn Date of the poll
    # Eg. Sun 25 Apr 2021.csv


"""

Prizes = {
    "FirstPrize": "",
    "SecondPrize": "",
    "ThirdPrize": ""
}
Starter_Prizes = []
Consolation_Prizes = []
drawDate = ""
drawNumber = ""

URL = input("Enter 4D URL: ")
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')


def ScrapeFirstToThirdPrizes():
    # This function collects first to third prizes.

    prizes_data = soup.find_all('tbody')
    for prizes in prizes_data:
        first_prize = prizes.find('td', class_="tdFirstPrize")
        second_prize = prizes.find('td', class_="tdSecondPrize")
        third_prize = prizes.find('td', class_="tdThirdPrize")
        if None in (first_prize, second_prize, third_prize):
            continue
        Prizes["FirstPrize"] = first_prize.text.strip()
        Prizes["SecondPrize"] = second_prize.text.strip()
        Prizes["ThirdPrize"] = third_prize.text.strip()


def StarterPrizes():
    # This function collects starter prizes.

    starter_data = soup.find_all('table', class_="table table-striped")
    for starters in starter_data:
        starter_prize = starters.find('tbody', class_="tbodyStarterPrizes")
        if starter_prize is None:
            continue
        Starter_Prizes.append(starter_prize.text)
        return starters


def ConsoPrizes():
    # This function collects consolation prizes.

    consolation_data = soup.find_all('table', class_="table table-striped")
    for consos in consolation_data:
        consolation_prize = consos.find('tbody', class_="tbodyConsolationPrizes")
        if consolation_prize is None:
            continue
        Consolation_Prizes.append(consolation_prize.text)
        return consos


def DrawDate():
    # This function collects drawn date

    dd = soup.find('th', class_="drawDate").text
    return dd


def DrawNumber():
    # This function collects the number drawn

    dn = soup.find('th', class_="drawNumber").text
    return dn


def cleanList(_list):
    # This function cleans the data scraped.
    # _list: List Type
    # Collected list data will be cleaned using regex.
    # _list will be cleared first, then appended with new data.

    if type(_list) == list:
        text = str(_list)
        r = re.findall("\d{4}", text)
        _list.clear()
        for item in r:
            _list.append(item)

    else:
        print("Error. List required.")


# Main loop.
ScrapeFirstToThirdPrizes()
StarterPrizes()
ConsoPrizes()
drawDate = DrawDate()
drawNumber = DrawNumber()
cleanList(Starter_Prizes)
cleanList(Consolation_Prizes)

# TODO: Append to file, instead of creating a new one
with open(str(drawDate) + ".csv", 'w') as file:
    # Writing to file
    # open('XXX.csv', 'w')
    # XXX is your file name
    # 'w' means write to file

    writer = csv.writer(file)
    writer.writerow([drawNumber])
    writer.writerow(["Prizes", "Number"])
    writer.writerow(["First", Prizes["FirstPrize"]])
    writer.writerow(["Second", Prizes["SecondPrize"]])
    writer.writerow(["Third", Prizes["ThirdPrize"]])
    for s in Starter_Prizes:
        writer.writerow(["Starter Prize", s])
    for c in Consolation_Prizes:
        writer.writerow(["Consolation Prize", c])
    print("CSV File dumped.")
