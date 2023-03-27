import virustotal3.enterprise
import virustotal3.core
from virustotal_python import   VirustotalError
from time import sleep
import os
import csv
from scrapeData import appendCsv

FILENAME = './{malicious_or_benign}/{date}_{source}_{trend}_{id}.json'

API_key = 'd9be5ab0910a56a56744c76daab1347a00efd92b257ed562a90dc47f8d69d75d'
VIRUSTOTAL_MAX_RETRIES = 5

URL_HEADER = ['Date', 'Source', 'SearchEngine', 'Trend', 'URL', 'harmless', 'malicious', 'suspicious', 'undetected', 'timeout']

def readCSV(filename):
    with open(filename, newline='') as csvfile:
        URLList = list(csv.reader(csvfile, delimiter=','))
    URLList.remove(URLList[0])
    return URLList



def analyzeURL(url,date, source, searchEngine, trend, retries = 0):
    url = url.split('?')[0]
    print("Analyzing: ", url)
    try:
        processVirusTotal = virustotal3.core.URL(api_key = API_key)
        analysis = processVirusTotal.info_url(url, timeout = 120)
        print('Waiting for results...')
    except Exception as error:
        if '"code": "NotFoundError"' in error.message and retries <= VIRUSTOTAL_MAX_RETRIES:
            print('Analysis in progress; retrying to fetch result in ', 60, ' seconds...')
            sleep(60)
            return analyzeURL(url=url, date=date, source=source, searchEngine=searchEngine, trend=trend, retries= retries + 1)
        else:
            print("Error analyzing URL: ", error)
            return None
    
    malicousOrBenignAnalysisStats = analysis['data']['attributes']['last_analysis_stats']
    print(malicousOrBenignAnalysisStats)
    appendCsv('analysis.csv', URL_HEADER, [date, source, searchEngine, trend, url, str(malicousOrBenignAnalysisStats['harmless']), str(malicousOrBenignAnalysisStats['malicious']), str(malicousOrBenignAnalysisStats['suspicious']), str(malicousOrBenignAnalysisStats['undetected']), str(malicousOrBenignAnalysisStats['timeout'])])


if __name__ == "__main__":
    URLList = (readCSV('URLs-final.csv'))

    for x in range(0,len(URLList)):
        for y in range(4,14):
            analyzeURL(URLList[x][y], URLList[x][0], URLList[x][1], URLList[x][2], URLList[x][3])
