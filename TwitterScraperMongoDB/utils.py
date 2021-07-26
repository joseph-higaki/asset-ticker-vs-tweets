import shutil

import null as null
from tweepy import OAuthHandler
import glob
import os
import json
import time
from itertools import chain
from pathlib import Path
from tqdm import tqdm
import tweepy
from tweepy import RateLimitError

import config
import my_mongo_client

spark = null
sparkSQL = null
api = null
scopedUser = ""
path = "./extraction/"
user = ""
tweetsPath = ""
followersPath = ""
mentionsPath = ""
sentimentPath = ""
ROOT_DIR = "path"

def init(user1):
    global user
    global tweetsPath
    global followersPath
    global mentionsPath
    global sentimentPath

    user = user1
    tweetsPath = path + user + "/tweets/"
    followersPath = path + user + "/followers/"
    mentionsPath = path + user + "/mentions/"
    sentimentPath = path + user + "/sentiment/"

    this_api = initAPI()

    Path(path + user).mkdir(parents=True, exist_ok=True)
    Path(tweetsPath).mkdir(parents=True, exist_ok=True)
    Path(followersPath).mkdir(parents=True, exist_ok=True)
    Path(mentionsPath).mkdir(parents=True, exist_ok=True)
    Path(sentimentPath).mkdir(parents=True, exist_ok=True)

    global mongo_client
    mongo_client = init_mongo_client()

    return this_api

def init_mongo_client():
    return my_mongo_client.MyMongoClient(config.get_config("mongo_connection_string"))

def getAPI():
    return api

def initAPI():
    global api
    consumer_key = config.get_config("twitter_consumer_key")
    consumer_secret = config.get_config("twitter_consumer_secret")
    access_token = config.get_config("twitter_access_token")
    access_token_secret = config.get_config("twitter_access_token_secret")

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    return api

def historicalMentions(user, since, until, lang='es', batch_size=50):
    save_dir = os.path.dirname(os.path.abspath(__file__))+"/"+tweetsPath
    json_name = user + "_tweets"+since+"."+until+".json"
    fetch_tweets('search', [user], since, until, lang, batch_size, save_dir, json_name,api)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def saveToJSON(listToSave, save_dir, json_name):
    jsonFile=save_dir + json_name
    with open(jsonFile, mode='w') as json_file:
        json.dump(listToSave, json_file,indent=4)


def merge_txt_files_scraped(dir_name):
    os.chdir(os.path.join(ROOT_DIR, dir_name))
    read_files = glob.glob("*.txt")
    joined_txt = [open(f, "r").readlines() for f in read_files if not f.startswith("tweets_ids")]
    joined_txt_no_duplicate_url = list(set(list(chain.from_iterable(joined_txt))))

    print(
        f"Deleted {len(list(chain.from_iterable(joined_txt))) - len(joined_txt_no_duplicate_url)} duplicated tweets")

    return [str(j.split('/')[3] + " " + j.split('/')[-1]) for j in joined_txt_no_duplicate_url]

def snscrape_ids(keyword_user_search_param, keywords_users_list, since, until, lang):
    dir_name = f"{since.replace('-', '')}_{until.replace('-', '')}"

    Path("./scraped_tweet").mkdir(exist_ok=True)
    os.chdir(os.path.join(ROOT_DIR, "scraped_tweet"))
    Path(dir_name).mkdir(exist_ok=True)

    temppath = "C:/twittertest/twits.json"
    for keyword in keywords_users_list:
        if len(keyword) > 0:
            output_name = f"{keyword.replace(' ', '_')}_{since.replace('-', '')}_{until.replace('-', '')}.txt"
            output_path = os.path.join(ROOT_DIR, 'scraped_tweet', dir_name, output_name)

            print(f'scraping tweets with keyword: "{keyword}" ...')
            try:
                os.system(f'snscrape twitter-user {keyword} > {temppath}')
                print('Searching for twitter-user:', keyword)
            except Exception as err:
                print(f"SNSCRAPE ERROR: {err}")
    shutil.move(temppath,output_path)
    print(f'Scraped all tweets in keywords list.')

    # merge all txt files in a folder in a single txt file and delete duplicated ids
    joined_txt_no_duplicate = merge_txt_files_scraped(os.path.join("scraped_tweet", dir_name))

    with open(f"tweets_ids_{dir_name}.txt", "w") as outfile:
        outfile.writelines(joined_txt_no_duplicate)
        print(f"'tweets_ids_{dir_name}.txt' saved in folder {dir_name}")

    return joined_txt_no_duplicate


# send request to twitter using tweepy (input: batch of 50 ids, output: for each ids a tweet containing:
# {id, username, text, date, location, keyword} )
def twitter_api_caller(keyword_user_search_param, keywords_list, ids, batch_size, save_dir, json_name,api):

    if keyword_user_search_param == 'search':
        csv_columns = ['id', 'username', 'text', 'keywords', 'date', 'location']
    else:
        csv_columns = ['id', 'username', 'text', 'date', 'location']

    try:
        os.chdir(os.path.join(ROOT_DIR, "scraped_tweet"))
        os.mkdir(save_dir)
    except FileExistsError:
        print("Directory 'final_tweet_csv' already exists")

    n_chunks = int((len(ids) - 1) // batch_size + 1)

    tweets = []
    i = 0
    for i in tqdm(range(0, n_chunks), ncols=150):
        if i > 0 and i % 300 == 0:
            # if batch number exceed 300 request could fail
            time.sleep(60)

        if i != n_chunks-1:
            batch = ids[i * batch_size:(i + 1) * batch_size]
        else:
            batch = ids[i * batch_size:]

        #print(f"Processing batch n° {i+1}/{n_chunks} ...")
        time.sleep(2)
        try:
            list_of_tw_status = api.statuses_lookup(batch, tweet_mode="extended")
        except RateLimitError as err:
            print('Tweepy: Rate Limit exceeded')
            # https://developer.twitter.com/en/docs/twitter-api/v1/tweets/timelines/faq
            saveToJSON(tweets, os.path.join("scraped_tweet", save_dir), f"{json_name}_last_batch_{i}")
            break
        except Exception as err:
            saveToJSON(tweets, os.path.join("scraped_tweet", save_dir), f"{json_name}_last_batch_{i}")
            print(f"General Error: {str(err)}")
            break

        tweets_batch = []
        for status in list_of_tw_status:
            try:
                tweet = {"id": status.id,
                         "username": status.user.screen_name,
                         "text": status.full_text,
                         "date": str(status.created_at),
                         "location": status.user.location}

                if keyword_user_search_param == 'search':
                    kl1 = [e for e in keywords_list if e.lower() in status.full_text.lower()]
                    kl2 = [e for e in keywords_list if e.lower() in status.user.screen_name.lower()]
                    keywords = [x for x in set(kl1 + kl2) if len(x) > 0]
                    tweet["keywords"] = keywords

            except Exception as err:
                print(f"General Error: {str(err)}")
                continue
            tweets_batch.append(tweet)
        #print(f"Processed - scraped {len(tweets_batch)} tweets.")
        if len(tweets_batch) == 0:
            saveToJSON(tweets, os.path.join("scraped_tweet", save_dir), f"{json_name}_last_batch_{i}")
            print("No tweets scraped")
            break
        i += 1
        #when saving to mongo, objects in list are changed and Json serialization fails later
        tweets_batch_copy = [t.copy() for t in tweets_batch]
        mongo_client.append_tweet_no_duplicates("twitter", "user_tweets", tweets_batch_copy)
        tweets.append(tweets_batch)


    saveToJSON(tweets, os.path.join("scraped_tweet", save_dir), json_name)
    return tweets


def fetch_tweets(keyword_user_search_param, keywords_users_list, since, until, lang, batch_size, save_dir, json_name,api):
    users_and_ids = snscrape_ids(keyword_user_search_param, keywords_users_list, since, until, lang)
    ids = list(map(lambda x: x.split(" ")[1].strip('\n'), users_and_ids))
    ids_at_mongo = mongo_client.get_tweets("twitter", "user_tweets")
    ids_at_mongo = [str(idm["id"]) for idm in ids_at_mongo]
    ids = list(set(ids) - set(ids_at_mongo))
    tweets = twitter_api_caller(keyword_user_search_param, keywords_users_list, ids, batch_size, save_dir, json_name,api)
    os.chdir(ROOT_DIR)
    return tweets