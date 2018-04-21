### final project of SI 507

from datetime import timedelta, date, datetime
from secrets import *
from coinbase.wallet.client import Client
import sqlite3
import json
import csv
import pprint

def collect_coinbase():

    # ------------------------------
    # collect data from Coinbase API
    # ------------------------------


    # Before implementation, set environmental variables with the names API_KEY_COINBASE and API_SECRET_COINBASE
    # API_KEY_COINBASE = '7wFz0CndMuduPhaO'
    # API_SECRET_COINBASE = 'SwN2NPlrak3t6gVrNpQmxphTSC40lRNH'


    client = Client(API_KEY_COINBASE, API_SECRET_COINBASE)#api_version='YYYY-MM-DD'

    currency_code = 'USD'  # can also use EUR, CAD, etc.
    # currency=currency_code
    # Make the request
    price = client.get_spot_price(currency=currency_code,date='2017-04-11')
    currencies = client.get_currencies()
    rates = client.get_exchange_rates(currency='BTC')
    time = client.get_time()
    # print ('Current bitcoin price in %s: %s %s' % (currencies, price,rates))

    def daterange(start_date, end_date):
        for n in range(int ((end_date - start_date).days)):
            yield start_date + timedelta(n)

    start_date = date(2013, 1, 1)
    end_date = date(2018, 1, 13)

    coinbase_d_cur_his=[]
    for single_date in daterange(start_date, end_date):
        pre_date = single_date.strftime("%Y-%m-%d")
        pre_price = client.get_spot_price(currency=currency_code, date=pre_date)

        # sell_price = client.get_sell_price(currency=currency_code, date=pre_date)
        # buy_price = client.get_buy_price(currency=currency_code, date=pre_date)
        print([pre_date,pre_price['base'],pre_price['currency'],pre_price['amount'],single_date.day,single_date.month,single_date.year])
        # print(pre_price['amount'], sell_price['amount'], buy_price['amount'])
        coinbase_d_cur_his.append([pre_date,pre_price['base'],pre_price['currency'],pre_price['amount'],single_date.day,single_date.month,single_date.year])


def collect_okcoin():
    # ------------------------------
    # collect data from Okcoin API
    # ------------------------------

    # API_KEY_OKCOIN='b4dd3278-df06-48af-8925-40120f46563b'
    # API_SECRET_OKCOIN='1F8A97B89F03A095238823CB1FAA3827'

    import sys
    sys.path.insert(0, '/Users/G_bgyl/si507/final_project/okcoin_lib')
    from OkcoinSpotAPI import OKCoinSpot
    from OkcoinFutureAPI import OKCoinFuture

    #初始化apikey，secretkey,url

    okcoinRESTURL = 'www.okcoin.com'   #请求注意：国内账号需要 修改为 www.okcoin.cn

    #现货API
    okcoinSpot = OKCoinSpot(okcoinRESTURL,API_KEY_OKCOIN,API_SECRET_OKCOIN)

    #期货API
    okcoinFuture = OKCoinFuture(okcoinRESTURL,API_KEY_OKCOIN,API_SECRET_OKCOIN)


    # pprint.pprint (okcoinSpot.depth('btc_usd'))
    okcoin_depth= okcoinSpot.depth('btc_usd')
    # pprint.pprint(okcoin_depth)
    bids=[]
    for each_b in okcoin_depth['bids']:
        bids.append(['bids']+each_b)
    asks=[]
    for each_a in okcoin_depth['bids']:
        asks.append(['asks']+each_a)
    okcoin_data= bids+asks
    # print(len(okcoin_depth['bids']),len(okcoin_depth['asks']),len(okcoin_data))
    return okcoin_data
def cache_data(coinbase_d_cur_his,okcoin_data):
    # ------------------------------------
    # cache data into csv file
    # ------------------------------------
    with open('coinbase.csv', 'w') as coinbase:  # , open('untrack_question.csv', 'w') as untrack_question
        writer = csv.writer(coinbase)
        writer.writerow(['time', 'digital_currency', 'currency','spot price','day','month','year'])
        for row in coinbase_d_cur_his:
            writer.writerow(row)

    with open('okcoin.csv', 'w') as okcoin:  # , open('untrack_question.csv', 'w') as untrack_question
        writer = csv.writer(okcoin)
        writer.writerow(['d_currency','type', 'price', 'volume'])
        for line in okcoin_data:
            line.insert(1,)
            writer.writerow(line)

def cached_data():
    with open('coinbase.csv', 'r') as coinbase, open('coinbase_.json','w')as json_coinbase:
        reader = csv.reader(coinbase)
        next(reader)
        coinbase_data = []
        for r in reader:
            coinbase_data.append([r[0],r[1],r[3]])
            json_coinbase.write(json.dumps(coinbase_data))

# ------------------------------------
# read data from csv file into database
# ------------------------------------

def create_dig_cur_db():
    try :

        conn = sqlite3.connect('digital_currency.db', timeout=10)
        cur = conn.cursor()
        print('successfully create an database')
    except:
        print('there\'s an error when creating an database')

    # Code below provided for your convenience to clear out the big10 database
    # This is simply to assist in testing your code.  Feel free to comment it
    # out if you would prefer

    statement = '''
        DROP TABLE IF EXISTS 'Coinbase';
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS 'Okcoin';
    '''
    cur.execute(statement)
    # year,month,day,digital_currency,currency
    statement = '''create table 'Coinbase'(  
                    'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                    'date' INTEGER NOT NULL,
                    'digital_currency' TEXT NOT NULL,
                    'currency' TEXT NOT NULL,
                    'spot_price' INTEGER NOT NULL,
                    'day' INTEGER NOT NULL,
                    'month' INTEGER NOT NULL,
                    'year' INTEGER NOT NULL
                    )
                    '''
    cur.execute(statement)
    conn.commit()
    statement = '''create table 'Okcoin'(  
                    'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                    'd_currency' TEXT NOT NULL,
                    'type' TEXT NOT NULL,
                    'price' INTEGER NOT NULL,
                    'volume' INTEGER NOT NULL,
                    FOREIGN KEY('d_currency') REFERENCES Coinbase(digital_currency)
                    )
                    '''

    cur.execute(statement)
    conn.commit()


    filename='coinbase.csv'
    with open(filename) as coinbase:
        reader = csv.reader(coinbase)
        next(reader)
        print('in function:')
        for each_line in reader:
            statement = '''insert into Coinbase Values (Null,?,?,?,?,?,?,?)'''
            # print(each_line)
            cur.execute(statement, tuple(each_line))
            conn.commit()
    filename = 'okcoin.csv'
    with open(filename) as okcoin:
        reader = csv.reader(okcoin)
        next(reader)

        for each_line in reader:
            print(each_line)
            statement = '''insert into Okcoin Values (Null,'BTC',?,?,?)'''
            cur.execute(statement, tuple(each_line))
            conn.commit()
    conn.close()

if __name__ == "__main__":
    cached_data()
    # create_dig_cur_db()
    exit()

