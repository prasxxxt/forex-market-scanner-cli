# importing libraries
import requests
from bs4 import BeautifulSoup
from tradingview_ta import TA_Handler, Interval


# economic indicators url codes
fundamental_codes = {
    "EUR": "euro-area",
    "GBP": "united-kingdom",
    "AUD": "australia",
    "NZD": "new-Zealand",
    "USD": "united-states",
    "CAD": "canada",
    "CHF": "switzerland",
    "JPY": "japan",
}


# cot data url codes
cot_codes = {
    "EUR": "099741",
    "GBP": "096742",
    "AUD": "232741",
    "NZD": "112741",
    "USD": "098662",
    "CAD": "090741",
    "CHF": "092741",
    "JPY": "097741",
}


# creating a Pair class to fetch and store all financial data
class Pair:

    def __init__(self, pair_name):
        # setting pair name & splitting base, quote currency
        self.pair = pair_name
        self.base = pair_name[:3]
        self.quote = pair_name[3:]
        # class vars to store callable data
        self.economic_data = {self.base: {}, self.quote: {}}
        self.cot_data = {self.base: {}, self.quote: {}}
        self.retail_data = {}
        self.technical_data = {}
        self.retail_data = {}
        self.technical_data = {}
        print("Collecting financial data please wait...")
        # calling all data function
        self.get_economic_data(self.base)
        self.get_cot_data(self.base)
        self.get_economic_data(self.quote)
        self.get_cot_data(self.quote)
        self.get_retail_data(self.pair)
        self.get_technical_data(self.pair)


    # function to get  tradingeconomics.com economic data
    def get_economic_data(self, currency):

        # getting webpage data
        url = f"https://tradingeconomics.com/{fundamental_codes[currency]}/indicators"
        r = requests.get(url, headers={'User-Agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1 (compatible; AdsBot-Google-Mobile; +http://www.google.com/mobile/adsbot.html)"})

        # picking economic data from html
        soup = BeautifulSoup(r.content, "html.parser")
        table = soup.find("tbody")
        rows = table.findAll("tr")
        for row in rows:
            row = row.get_text().strip().splitlines()
            data_type = row[0].lower().strip().replace(" ", "-")

            # storing data
            self.economic_data[currency][data_type] = {}
            self.economic_data[currency][data_type]["current"] = row[2]
            self.economic_data[currency][data_type]["previous"] = row[3]
            self.economic_data[currency][data_type]["unit"] = row[4]
            self.economic_data[currency][data_type]["date"] = row[5]


    # function to get tradingster.com non-commercial cot data
    def get_cot_data(self, currency):

        # getting webpage data
        url = f"https://www.tradingster.com/cot/legacy-futures/{cot_codes[currency]}"
        r = requests.get(url, headers={'User-Agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1 (compatible; AdsBot-Google-Mobile; +http://www.google.com/mobile/adsbot.html)"})

        # picking economic data from html
        soup = BeautifulSoup(r.content, "html.parser")
        rows = (soup.find("tbody")).findAll("tr")
        row = rows[1].get_text().strip().splitlines()
        l, s = int(row[0].replace(",", "")), int(row[1].replace(",", ""))
        long = round((l / (l + s)) * 100, 1)
        short = round((s / (l + s)) * 100, 1)

        # storing data
        self.cot_data[currency]["long"] = long
        self.cot_data[currency]["short"] = short


    # function to get myfxbook.com retail traders data
    def get_retail_data(self, pair):

        # getting webpage data
        r = requests.get(f"https://www.myfxbook.com/community/outlook/{pair}", headers={'User-Agent': "Mozilla/5.0"})


        # picking economic data from html
        soup = BeautifulSoup(r.content, "html.parser")
        table = soup.find("table", {"id": "currentMetricsTable"})
        rows = table.findAll("td")
        long = int((rows[6].get_text().splitlines())[1])
        short = int((rows[2].get_text().splitlines())[1])

        # storing data
        self.retail_data["long"] = long
        self.retail_data["short"] = short


    # function to get tradingview technical indicators data
    def get_technical_data(self, pair):

        # collecting technical data
        handler = TA_Handler(symbol=pair, exchange="FX_IDC", screener="forex", interval=Interval.INTERVAL_1_DAY, timeout=None)

        # storing data
        self.technical_data = handler.get_analysis().summary
