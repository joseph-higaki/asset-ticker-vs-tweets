# When we're as cool as JLo, we will get this from a secret's file
# for now, we'll probably just .gitignore this
def get_config(key):
    __config_settings = {
        "mongo_connection_string": "mongodb+srv://admin:xxx@cluster0.5ryg7.mongodb.net/",
        "twitter_consumer_key": "nullablenull",
        "twitter_consumer_secret": "nullablenull",
        "twitter_access_token": "nullablenull-nullablenull",
        "twitter_access_token_secret": "nullablenull"
    }
    return __config_settings[key]

