import datetime as dt 
import pandas as pd 
import numpy as np 
from pandas_datareader import data as pdr 
import plotly.offline as pyo 
from plotly.subplots import make_subplots
import bs4 as beautifulsoup 
import concurrent.futures as concf 
from yahoofinancials import YahooFinancials
import re 
import ast 
import time 
import requests 
from bs4 import BeautifulSoup


with open ('balancesheet_sp500.txt','r') as input:
        balancesheet = ast.literal_eval(input.read())
with open ('incomestatement_sp500.txt' , 'r' ) as input : 
        incomestatement = ast.literal_eval(input.read()) 
with open('cashflowstatement_sp500.txt' , 'r' ) as input: 
        cashflowstatement = ast.literal_eval(input.read())


def StockList():
    sp500list = [] 
    requrl = "https://www.slickcharts.com/sp500"
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    }

    sp500 = [requrl]
    for i, val in enumerate(sp500):
        res = requests.get(requrl, headers=header)
        webscrape = BeautifulSoup(res.text, 'html.parser')
        listscrape = webscrape.findAll(
            'table',  class_='table table-hover table-borderless table-sm')[0].findAll('tbody')
        for index, value in enumerate(listscrape[0]):
            if len(value) > 1:
                text = re.sub(r"[<td>]", "", str(value))
                text1 = re.split('/', text)

                for i in range(len(text1[3])):
                    if text1[3][i] == '"':
                        sp500list.append((text1[3][0:i]))

    stockset = set(sp500list)
    if len(stockset) != len(sp500list):
        print("Contains Duplicates")
    else:
        print("No Duplicates")

    return sp500list

class Financialstatements() : 
    def __init__(self,type,frequency = 'Annual') : 
        self.yearlydict = {} 
        self.type = []
        self.frequency = frequency

    def addstatement(self,yearidx,statement) : 
        self.yearlydict[yearidx]  = statement 

class Stock() : 
    def __init__(self,ticker,listid ,freq = 'Annual') : 
        self.ticker = ticker 
        self.financialstatements = [Financialstatements(balancesheet),Financialstatements(incomestatement) , Financialstatements(cashflowstatement)]
        self.listid = listid
        self.netchangedic = {} 

sp500list = StockList()

array = [] 

for i in range(500) : 
    array.append(Stock(sp500list[i],i))




bslist = []
years = 4 


for i in array:
                for year in range(0,4) : 
                    try:
                        for dates in balancesheet[sp500list[i.listid]][year].items(): 
                                i.financialstatements[0].addstatement(year,dates)
                    except : 
                        print("error" , i )


for i in array:
                for year in range(0,4) : 
                    try:
                        for dates in incomestatement[sp500list[i.listid]][year].items(): 
                                i.financialstatements[1].addstatement(year,dates)
                    except : 
                        print("error" , i )
                    


for i in array:
                for year in range(0,4) : 
                    try:
                        for dates in cashflowstatement[sp500list[i.listid]][year].items(): 
                                i.financialstatements[2].addstatement(year,dates)
                    except : 
                        print("error" , i ) 

s1 = array[0] 
print(s1.financialstatements[0])
      






        
        






































