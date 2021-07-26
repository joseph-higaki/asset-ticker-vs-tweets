import time

from utils import *


if __name__ == "__main__":
    #term = 'joseph_higaki'
    #term = 'VitalikButerin'
    term = 'elonmusk'
    #term = 'SatoshiLite'
    #term = 'officialmcafee'
    #term = 'aantonop'
    #term = 'rogerkver'
    #term = 'brian_armstrong'
    #term = 'cz_binance'
    since = '2020-01-14'
    until = '2020-03-21'
    lang="en"
    max_error_iter = 20

    while (max_error_iter > 0):
        try:
            init(term)
            documents=historicalMentions(term,since,until,lang)
        except Exception as e:
            time.sleep(10)
            print(e)
            max_error_iter = max_error_iter - 1
            pass


