from datetime import date
from pytrends.request import TrendReq
import os
import json
from time import sleep
from math import ceil
from googlesearch import search
import requests
import csv
import sys
from bs4 import BeautifulSoup


#Save the top N search URLs
URL_COUNT = 5
URL_FILE = "URLs-record.csv"
WEBSITE = "USCIS"
PUBLIC_FIGURE = " Serena Williams"
URL_HEADER = ['Website', 'PublicFigure', 'Question', 'SearchEngine'] + list('URL ' + str(index + 1) for index in range(URL_COUNT))

# subscription key
#BING_SUBSCRIPTION_KEY = 'd0138d4b9bf842c09dcba8d0058e0b74'
def readCSV(filename):
    with open(filename, newline='') as csvfile:
        questions = list(csv.reader(csvfile, delimiter=','))
    questions.remove(questions[0])

def appendCsv(filename, headers, data):
    with open(filename, mode = 'a') as file:
        if os.path.getsize(filename) == 0:
            file.write(','.join(headers) + '\n')
        file.write(','.join(data) + '\n')

#Search Google Results
def searchGoogleResults(query, Source, question):
    results = list(search(query, num_results=URL_COUNT))
    print("Search Results for", query, ": ", results, "\n")
    appendCsv(URL_FILE, URL_HEADER, [WEBSITE, PUBLIC_FIGURE, question, Source] + results)
    return results


#webscrapping
def webscrapper(URL, filename=PUBLIC_FIGURE):
    #Make a request to URL
    page = requests.get(URL)

    # Parse the HTML content of the page
    soup = BeautifulSoup(page.content, "html.parser")
    with open(filename, mode = 'a') as file:
        if os.path.getsize(filename) == 0:
            file.write(soup.get_text() + "\n")
        file.write(soup.get_text() + "\n")




'''
#Search Bing Results
def searchBingResults(bing_subscription_key,trendSource, trend):
    search_url = "https://api.bing.microsoft.com/v7.0/search"
    headers = {"Ocp-Apim-Subscription-Key": bing_subscription_key}
    params = {
        "q": trend,
        "count": URL_COUNT,
        "responseFilter": "Webpages",
        "textDecorations": True,
        "textFormat": "HTML"}
    results = requests.get(search_url, headers = headers, params = params)
    urllist = []
    for i in range(0,10):
        urllist.append(results.json()['webPages']['value'][i]['url'])
    appendCsv(URL_FILE, URL_HEADER, [DATE, trendSource,'Bing', trend] + urllist)
    
'''        


if __name__ == "__main__":
    with open("questions.txt" , "r") as f:
        questions = [line.strip() for line in f]


    for question in questions:
        URLs = searchGoogleResults(question + PUBLIC_FIGURE, Source="Google", question=question)
        for URL in URLs:
            webscrapper(URL)

        