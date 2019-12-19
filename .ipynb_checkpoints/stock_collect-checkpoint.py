# -*- coding: utf-8 -*-
# # Stock Data Fetch 

# - ## Funciton

# - ### 抓取股價歷史資訊(get_stock_history)
# -**input **
#   - date : 西元日期
#   - stock_no : 股票編號
#      - 萃取API的json資料並將資料做轉換。(日期及資料上)
#      - API: 'http://www.twse.com.tw/exchangeReport/STOCK_DAY?date=%s&stockNo=%s'

# +
import numpy as np
import requests
import pandas as pd
import datetime

#   http://www.twse.com.tw/exchangeReport/STOCK_DAY?date=20180817&stockNo=2330  取一個月的股價與成交量
def get_stock_history(date, stock_no):
    quotes = []
    url = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY?date=%s&stockNo=%s' % ( date, stock_no)
    r = requests.get(url)
    data = r.json()
    return transform(data['data'])  #進行資料格式轉換


# -

# - ### 轉換歷史資訊(transform_date, transform_data)
# -**input **
#   - date : 西元日期
#   - data : 股票編號
#      - 轉換API的日期為西元、將數值格式從數學符號轉換為數字。(日期及資料上)

# +
def transform_date(date):
        y, m, d = date.split('/')
        return str(int(y)+1911) + '/' + m  + '/' + d  #民國轉西元
    
def transform_data(data):
    data[0] = datetime.datetime.strptime(transform_date(data[0]), '%Y/%m/%d')
    data[1] = int(data[1].replace(',', ''))  #把千進位的逗點去除
    data[2] = int(data[2].replace(',', ''))
    data[3] = float(data[3].replace(',', ''))
    data[4] = float(data[4].replace(',', ''))
    data[5] = float(data[5].replace(',', ''))
    data[6] = float(data[6].replace(',', ''))
    data[7] = float(0.0 if data[7].replace(',', '') == 'X0.00' else data[7].replace(',', ''))  # +/-/X表示漲/跌/不比價
    data[8] = int(data[8].replace(',', ''))
    return data

def transform(data):
    return [transform_data(d) for d in data]


# -

# - ### 建立目標資料表(transform_date, transform_data)
# -**input **
#   - date : 西元日期
#   - stock_no : 股票編號
#      - 建立資料表DataFrame with columns 日期、成交股數、成交金額、開盤價、最高價、最低價、漲跌價差、成交筆數 + 股票代碼欄

# +
def create_df(date,stock_no):
    s = pd.DataFrame(get_stock_history(date, stock_no))
    s.columns = ['date', 'shares', 'amount', 'open', 'high', 'low', 'close', 'change', 'turnover']
                #"日期","成交股數","成交金額","開盤價","最高價","最低價","收盤價","漲跌價差","成交筆數" 
    stock = []
    for i in range(len(s)):
        stock.append(stock_no)
    s['stockno'] = pd.Series(stock ,index=s.index)  #新增股票代碼欄，之後所有股票進入資料表才能知道是哪一張股票
    datelist = []
    for i in range(len(s)):
        datelist.append(s['date'][i])
    s.index = datelist  #索引值改成日期
    s2 = s.drop(['date'],axis = 1)  #刪除日期欄位
    mlist = []
    for item in s2.index:
        mlist.append(item.month)
    s2['month'] = mlist  #新增月份欄位
    return s2
        

# -

# - ## Main

# - ### 獲取全股票代碼
# -**input **
#   - API : http://isin.twse.com.tw/isin/C_public.jsp?strMode=2
#   - 市場別 : "上市"
#      - 萃取上市個股代碼 (包含近幾年的)
#
#  -**output **
#    - stock_no_vec : 股票代碼列表

# +
import requests
import pandas as pd

res = requests.get("http://isin.twse.com.tw/isin/C_public.jsp?strMode=2")
df = pd.read_html(res.text)[0]
# 設定column名稱
df.columns = df.iloc[0]
# 刪除第一行
df = df.iloc[1:]
# 先移除row，再移除column，超過三個NaN則移除
df = df.dropna(thresh=3, axis=0).dropna(thresh=3, axis=1)
filt = df["市場別"] =="上市" # 參賽人數大於 10
df = df[filt] # 篩選 data fram
import re 
sotock_no_vec = [re.split ("\s",x)[0] for x in set(df["有價證券代號及名稱"].values) ]
# -





# - ### 獲取全股票歷史資訊(排除未達20年以上之股票)

listDji = ['044472']
for i in range(len(listDji)):
    result = create_df('20180701', listDji[i])



print(result.groupby('month').close.count())  #每個月幾個營業日
print(result.groupby('month').shares.sum())  #每個月累計成交股數
