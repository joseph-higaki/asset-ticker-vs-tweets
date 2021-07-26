#  Asset Ticker vs Tweets

We are extracting tweets from crypto influencers on a given timeline, identifying keywords related to a cryptocurrency and visualize the tweets along with a price line chart from the asset.

This is a [group](#team) assignment from the **Big Data Technology and Architecture** course from the Big Data &amp; Analytics Masters @ [EAE](https://www.eae.es/) class of 2021.

![image](https://github.com/joseph-higaki/asset-ticker-vs-tweets/blob/7454c40556836822119ec2577a9be21416018d25/Final-SolutionDiagram.png)

## First, extract the tweets

Our first step was to use [Twitter API](https://developer.twitter.com/en/docs/twitter-api) using [Tweepy](https://www.tweepy.org/) from a [Databricks](https://databricks.com/) notebook and store the influencer tweets into a [MongoDB](https://www.mongodb.com/cloud/atlas) collection.

<img src="https://github.com/joseph-higaki/asset-ticker-vs-tweets/blob/7454c40556836822119ec2577a9be21416018d25/First-SolutionDiagram.png" width="600">

We realized that, not only we would need to do trial & error with things like [time delays in code execution](https://docs.python.org/3/library/time.html?highlight=sleep#time.sleep) and  [wait_on_rate_limit](https://docs.tweepy.org/en/v3.5.0/api.html#tweepy-api-twitter-api-wrapper) settings, WE COULDN'T connect to the Twitter APIs from our [community cluster at databricks](https://databricks.com/product/faq/community-edition#:~:text=Where%20is%20the%20Databricks%20Community,hosted%20on%20Amazon%20Web%20Services.).

[JLo](https://www.linkedin.com/in/jlsanchezros/) helped our class out, providing a python console program to extract tweets using [web scraping](https://github.com/JustAnotherArchivist/snscrape).
Even though this way of extracting the tweets would not be using the distributing processing benefits of the Databricks runtime [Apache Spark](https://spark.apache.org/), we were still somehow limited to massively get twitter data due to API usage limits. So this was our next best thing to do, with the resources we had at hand. 

<img src="https://user-images.githubusercontent.com/11904085/127054865-d7759bfb-f5db-4c2c-912e-3e9c33b10804.png" width="600">

## Second, store the tweets in MongoDB 

We did some changes to the [Python console](https://github.com/joseph-higaki/asset-ticker-vs-tweets/tree/main/TwitterScraperMongoDB) extracting the tweets. Every web-scraped batch would append the tweets into our MongoDB collection. 

First and second step are at the folder [TwitterScraperMongoDB](https://github.com/joseph-higaki/asset-ticker-vs-tweets/tree/main/TwitterScraperMongoDB) containing the python console program.

## Third, get prices for crypto

Instead of using a cryptocurrency specific API like [CoinMarketCap](https://coinmarketcap.com/api/) or [CoinGecko](https://www.coingecko.com/es/api) we went with [Yahoo Finance](https://finance.yahoo.com/) as data source, using web-scraping-based library [yfinance](https://pypi.org/project/yfinance/)
The reasons of doing this were:
1. Should we want to extend our analysis to a company stock, commodity or index fund; we could do it with yfinance. Example: [$TSLA](https://finance.yahoo.com/quote/TSLA)
1. For the purposes of this homework, we're getting a single price on crypto to USD per day. For example: [Ethereum](https://finance.yahoo.com/quote/ETH-USD). And, Yahoo finance is good enough 
1. [yfinance](https://pypi.org/project/yfinance/) was very easy to use, does not require API keys

## Fourth, plot tweets and prices together

Having the data, we had the possibility to determine a plot-legible date-span using keywords and sentiment analysis from the tweets, but...

So we just used expert's judgement and some old-fashioned twitter browing to determing hard-coded parameters for what we chose to plot.

Example: 

![ElonvsDoge](https://user-images.githubusercontent.com/11904085/127054871-d8d90f2b-1d9d-4113-b276-7b3eff662615.jpg)

Steps three and four, are at [Asset Ticker vs Tweets](https://github.com/joseph-higaki/asset-ticker-vs-tweets/blob/7454c40556836822119ec2577a9be21416018d25/Asset%20Ticker%20vs%20Tweets.dbc) Databricks notebook.
This is the [IPython notebook version](https://github.com/joseph-higaki/asset-ticker-vs-tweets/blob/7454c40556836822119ec2577a9be21416018d25/Asset%20Ticker%20vs%20Tweets.ipynb) exported from a Databricks notebook. Github won't a *.dbc file. Just notice that *.ipynb won't be able to run over a Jupyter Notebook as is.

## Team
* [Henrique Avila](https://www.linkedin.com/in/henrique-avila-101170a0/) 
* [Joseph Higaki](https://www.linkedin.com/in/josephhigaki/) ([GitHub](https://github.com/joseph-higaki/))
* [Raquel Ganuza](https://www.linkedin.com/in/raquel-ganuza-catal%C3%A1n/)
* [Romain Baleynaud](https://www.linkedin.com/in/romain-baleynaud/) ([GitHub](https://github.com/RomainBal)) 
* [Ziyad Ashukri](https://www.linkedin.com/in/ziyadashukri/)

# Professor
* [José Luis Sánchez Ros](https://www.linkedin.com/in/jlsanchezros/)
* [Gerard Reverté Busca](https://www.linkedin.com/in/greverte/)
 
