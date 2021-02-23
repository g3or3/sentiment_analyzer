from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import matplotlib.pyplot as plt

finvizUrl = 'https://finviz.com/quote.ashx?t='

tickers = ['JPM', 'GS', 'V', 'AAPL', 'MSFT']

newsTables = {}

for ticker in tickers:
    url = finvizUrl + ticker

    req = Request(url = url, headers = {'user-agent': 'sentiment_analyzer'})
    response = urlopen(req)

    html = BeautifulSoup(response, features = "html.parser")

    newsTable = html.find(id = 'news-table')
    newsTables[ticker] = newsTable

parsedData = []

for ticker, newsTable in newsTables.items():
    for row in newsTable.findAll('tr'):
        title = row.a.text
        dateData = row.td.text.split(' ')

        if len(dateData) == 1:
            time = dateData[0]
        else:
            date = dateData[0]
            time = dateData[1]

        parsedData.append([ticker, date, time, title])

df = pd.DataFrame(parsedData, columns = ['ticker', 'date', 'time', 'title'])

vader = SentimentIntensityAnalyzer()

f = lambda title: vader.polarity_scores(title)['compound']
df['compound'] = df['title'].apply(f)
df['date'] = pd.to_datetime(df.date).dt.date

plt.figure(figsize = (10, 8))

meanDf = df.groupby(['ticker', 'date']).mean()
meanDf = meanDf.unstack()
meanDf = meanDf.xs('compound', axis = 'columns').transpose()
meanDf.plot(kind = 'bar')

print(meanDf)
plt.show()
