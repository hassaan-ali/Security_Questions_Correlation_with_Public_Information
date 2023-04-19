from datetime import date
from pytrends.request import TrendReq
import os
import json
import time
from time import sleep
from math import ceil
from googlesearch import search
import requests
import csv
import re
from bs4 import BeautifulSoup



#Save the top N search URLs
URL_COUNT = 4
URL_FILE = "URLs-record.csv"
WEBSITE = ['bcs', 'united_airlines', 'usps', 'spectrum']
PUBLIC_FIGURE = "Barack Obama"
URL_HEADER = ['Website', 'PublicFigure', 'Question', 'SearchEngine'] + list('URL ' + str(index + 1) for index in range(URL_COUNT))

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
def searchGoogleResults(query, Source, question, website):
    results = list(search(query, num_results=URL_COUNT, lang="en"))
    print("Search Results for", query, ": ", results, "\n")
    appendCsv(URL_FILE, URL_HEADER, [website, PUBLIC_FIGURE, question, Source] + results)
    return results




#webscrapping
def webscrapper(URL, filename):
    #Make a request to URL
    params = {'q': 'python', 'key': 'AIzaSyCRBkVM2PRMGABvM2JARQRYcFOy9v4fmlg'}
    page = requests.get(URL, params)

    # Parse the HTML content of the page
    soup = BeautifulSoup(page.content, "html.parser")
    all_text = soup.get_text(strip=True)
    clean_text = re.sub(r"[^a-zA-Z0-9.]+", " ", all_text)
    with open(filename, mode = 'a', buffering=1024) as file:
        if os.path.getsize(filename) == 0:
            file.write(clean_text + "\n")
        file.write(clean_text + "\n")    


if __name__ == "__main__":
    for website in WEBSITE:
        with open("questions" + '-' + website + '.txt' , "r") as f:
            questions = [line.strip() for line in f]


        for question in questions:
            URLs = searchGoogleResults(question + ' ' + PUBLIC_FIGURE, Source="Google", question=question, website=website)

            for URL in URLs:
                webscrapper(URL, PUBLIC_FIGURE + '_' + website + '.txt')
                sleep(2)
            sleep(5)

        