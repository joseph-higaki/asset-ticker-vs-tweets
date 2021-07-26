#>pip install pymongo
#>pip install dnspython
#from pymongo import MongoClient
import pymongo

class MyMongoClient:
    def __init__(self, connection_string):
        self.__connection_string = connection_string
        self.__client = pymongo.MongoClient(connection_string)

    def get_tweets(self, database_name, collection_name):
        db = self.__client[database_name]
        mycollection = db[collection_name]
        return list(mycollection.find({}))

    def append_tweet_no_duplicates(self, database_name, collection_name, tweets_batch):
        db = self.__client[database_name]
        mycollection = db[collection_name]
        # Ensure unique tweet id
        # this should be done at collection creation time
        # I hope Mongo is smart enough to detect that the
        # requested index already exists, and does nothing
        mycollection.create_index('id', unique=True)
        for twit in tweets_batch:
            try:
                print(f"Saving To Mongo: {twit['id']} - {twit['username']}")
                mycollection.insert_one(twit)
                print(f"Saved To Mongo: {twit['id']} - {twit['username']}")
            except pymongo.errors.DuplicateKeyError as e:
                print(f"Duplicate tweet insert: {str(e)}")