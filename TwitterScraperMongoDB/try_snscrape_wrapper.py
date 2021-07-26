import snscrape.modules.twitter as sntwitter

#One improvement I can think of, is using the snscrape wrapper
# and do this all in-memory.
# first iteration will be to see how it goes
# eventually I would need to dump it to disk
# so that this has pause/resume options

# Creating list to append tweet data to
tweets_list1 = []

# Using TwitterSearchScraper to scrape data and append tweets to list
for i, tweet in enumerate(sntwitter.TwitterSearchScraper('from:joseph_higaki').get_items()):
    if i > 10:
        break
    tweets_list1.append([tweet.date, tweet.id, tweet.content, tweet.username])

print(tweets_list1)
# it looks like you can already extract tweet id, date, text and username without going to the
# tweepy API
# needs further exploring