# -*- coding: utf-8 -*-
# # FUNCTION
# ## JSON FORMAT

def create_df(date, df):
    df = pd.DataFrame(df)
    if len(df.columns) == 5 :# 無股利年度及財報季度。
        year = str(int(date[0:4])-1911-1) # 股利年度
        df[5] = year
        month = int(date[4:6])
        if month in [1,2,3] : # 財報季度
            df[6] = year+"/4"
        elif month in [4,5,6] :
            df[6] = str(int(year)+1)+"/1"
        elif month in [7,8,9] :
            df[6] = str(int(year)+1)+"/2"
        elif month in [10,11,12] :
            df[6] = str(int(year)+1)+"/3"
        df = df.iloc[:,[0,1,3,5,2,4,6]]
    # 重新定義漲跌價差，將負號入數值之中。
    s = df
    s.columns = ['stockno', 'stock_name', 'dividend_yield', 'dividend_year', 'PE_ratio',  'PB_ratio',  'financial_season']
                #"證券代號"  "證券名稱"        "殖利率",        "股利年度",      "本益比",   "股價淨值比",     "財報季度"

    s['stockno'] = s['stockno'].str.replace(' ', '')
    s['stock_name'] = s['stock_name'].str.replace(' ', '')
    s['dividend_yield'] = s['dividend_yield'].str.replace(',', '')
    s['PE_ratio'] = s['PE_ratio'].str.replace('-', '0.0')
    s['PE_ratio'] = s['PE_ratio'].str.replace(',', '')
    s['PB_ratio'] = s['PB_ratio'].str.replace(',', '')
    s['date'] = date  #新增日期
    s['year'] = date[0:4]  #新增月份欄位
    s['month'] = date[4:6]  #新增月份欄位
    s['day'] = date[6:8]   #新增日欄位
    return s


def get_stock_day(date):
    r = requests.post("https://www.twse.com.tw/exchangeReport/BWIBBU_d?response=json&date="+date+"&selectType=ALL")
    # step3. 篩選出個股盤後資訊
    # step4. 印出選股資訊，解析JSON格式
    data = r.json()
    df = data['data']
    return df








# # MAIN
# ## 設定開始時間 : date
# ## 設定檔案名稱 : filename

# step1. import package 
import requests
import pandas as pd
import numpy as np
from io import StringIO
import re
import os 
import time
from datetime import date, timedelta, datetime
from stock_csv_save import stock_csv_save

# step2. 進入目標網站,爬取盤後資訊
date = '20191219'
filename = "stock_value.csv"
logname = "stock_value_log.txt"
for i in range(7300):

    # Step1 - Date convert day by day 
    # Step2 - Fetch Data From
    # 2_1 Call web data
    # 2_2 create df
    # 2_3 write to csv
    date = date.replace("-","")
    x = datetime.strptime(date, "%Y%m%d").date()
    x = x - timedelta(1)
    date = str(x).replace("-","")

    
    
    
    # 2_1 Call web data
    try:
        df = get_stock_day(date)
    except:
        print(date + " | No this day data")
        time.sleep(10)
        continue

    # 2_2 create df
    df = create_df(date, df)
    stock_csv_save(df, filename, logname, date)

    
    time.sleep(10)
    if(i%100==0):
        time.sleep(60)


