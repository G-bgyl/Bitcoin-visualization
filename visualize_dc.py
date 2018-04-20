
from datetime import timedelta, date, datetime
from coinbase.wallet.client import Client
import csv
import sqlite3
import json
import pandas as pd
from calendar import monthrange
import pprint
import matplotlib as mpl
# use TkAgg when debugging at local
# mpl.use('TkAgg')
# use Agg when launch on heroku
mpl.use('Agg')
import matplotlib.pyplot as plt
import os
DBNAME='digital_currency.db'

'''

CACHE_coinbase = 'coinbase.json'
try:
    cache_file = open(CACHE_coinbase, 'r')
    cache_coinbase = cache_file.read()
    CACHE_DICTION_coinbase = json.loads(cache_coinbase)
    cache_file.close()

# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION_coinbase = {}

CACHE_okcoin = 'okcoin.json'
try:
    with open(CACHE_okcoin, 'r') as cache_file:
        cache_okcoin = cache_file.read()
        CACHE_DICTION_okcoin = json.loads(cache_okcoin)


# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION_okcoin = {}


def main_get_data_from_twitter(begin_date,end_date):
    # now = datetime.now(pytz.utc)
    # youngest = max(dt for dt in datetimes if dt < now)
    #
    # ## first, look in the cache to see if we already have this data
    # if unique_ident in CACHE_DICTION:
    #     print("Getting cached data...")
    #     return CACHE_DICTION[unique_ident]


    #TODO: get a list of date in coinbase dataset ,and check if begindate and end date is include by this
    if True:
        pass

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file
    else:
        print("Making a request for new data...")
        # Make the request and cache the new data
        for single_date in daterange(start_date, end_date):
            pre_date = single_date.strftime("%Y-%m-%d")
            pre_price = client.get_spot_price(currency=currency_code, date=pre_date)
            sell_price = client.get_sell_price(currency=currency_code, date=pre_date)
            buy_price = client.get_buy_price(currency=currency_code, date=pre_date)
            coinbase_d_cur_his.append(
                [pre_date, pre_price['base'], pre_price['currency'], pre_price['amount'], sell_price['amount'],
                 buy_price['amount']])'''
def boxplot(year):
    conn = sqlite3.connect('digital_currency.db')
    cur = conn.cursor()
    statement = '''select spot_price, month
           from Coinbase
           where year=%s'''%(year)
    result = cur.execute(statement)
    conn.commit()
    boxplot = result.fetchall()
    conn.close()
    print('print type of boxplot',type(boxplot))
    return boxplot
def boxplot_get_K_line_data(year,freq='Month'):
    conn = sqlite3.connect('digital_currency.db')
    cur = conn.cursor()

    year_data=[]

    statement = '''select [month],max(spot_price),min(spot_price)
            from Coinbase
            where year =%s
            group by [month];
                ''' % (year)
    result = cur.execute(statement)
    conn.commit()
    max_min_price = result.fetchall()
    year_data.extend(max_min_price)
    # pprint.pprint(year_data)

    for i in range(12):
        month=i+1
        month_data=[]


        m_length = monthrange(year, month)[1]
        # print(m_length)

        # get price of first and last day of the month
        for day in [1,m_length]:
            # print('year, month, day',year,month,day)
            stm='''select spot_price
from Coinbase
where year =%s and [month]=%s and [day]=%s;'''%(year,month,day)
            result = cur.execute(stm)
            first=result.fetchone()[0]
            month_data.append(first)
            conn.commit()
        year_data[i] += tuple(month_data)
        # print(year_data)
    conn.close()
    return year_data


def line_chart(year):
    conn = sqlite3.connect('digital_currency.db')
    cur = conn.cursor()



    statement = '''select [date], spot_price
from Coinbase
where year =%s''' % (year)
    result = cur.execute(statement)
    conn.commit()
    line_chart = result.fetchall()

    conn.close()
    return line_chart

def area_depth(type):
    conn = sqlite3.connect('digital_currency.db')
    cur = conn.cursor()

    statement = '''select price, volume
from Okcoin 
where type="%s" ''' % (type)
    result = cur.execute(statement)
    conn.commit()
    area_data = result.fetchall()

    conn.close()
    return area_data

def rate_bar(year):
    conn = sqlite3.connect('digital_currency.db')
    cur = conn.cursor()

    statement = '''select [month], avg(spot_price)
from Coinbase
where year =%s
group by [month];
 ''' % (year)
    result = cur.execute(statement)
    conn.commit()
    avg_data = result.fetchall()
    # print(avg_data)
    conn.close()
    rate_data=[]
    for i in range(1,12):
        rate=round(100*(avg_data[i][1]-avg_data[i-1][1])/avg_data[i-1][1],2)
        rate_data.append(rate)
    return rate_data
if __name__=='__main__':
    currency='BTC'
    year = input("which year's data do you want to take a look at?")
    type = input("which type's data do you want to take a look at?")
    boxplot = boxplot(year)
    line_plot = line_chart(year)
    area_data=area_depth(type)
    rate_data=rate_bar(year)
    print('__file__:',__file__)
    __file__='/Users/G_bgyl/si507/final_project/visualize_dc.py'
    my_path = os.path.dirname(__file__)
    print('my path:',my_path)


    df_line = pd.DataFrame(line_plot)
    df_line.plot.line()
    plt.savefig(my_path +"/plot/line_plot_%s.png"%(year))

    df_box_plot = pd.DataFrame(boxplot, columns=['spot_price', 'month'])
    df_box_plot.boxplot(column='spot_price',by='month')
    plt.title('%s Price for %s'%(currency,year))
    plt.suptitle("")
    plt.savefig(my_path +"/plot/boxplot_%s.png"%(year))

    df_area=pd.DataFrame(area_data)
    df_area.plot.area(title='Current Price Depth')
    plt.savefig(my_path +"/plot/area_data_%s.png"%(year))

    df_rate=pd.DataFrame(rate_data)
    df_rate.plot.bar(title='growth rate')
    plt.savefig(my_path +"/plot/rate_data_%s.png"%(year))

    plt.show()

    # df.boxplot(column=None, by=None, ax=None, fontsize=None, rot=0, grid=True, figsize=None, layout=None, return_type=None, **kwds)[source]