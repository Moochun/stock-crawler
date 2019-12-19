# -*- coding: utf-8 -*-
# # FUNCTION
# ## JSON FORMAT

def create_df(date, df):
    df = pd.DataFrame(df)
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
# ## 設定記錄檔名稱 : logname

# step1. import package 
import requests
import pandas as pd
import numpy as np
from io import StringIO
import re
import os 
import time
from datetime import date, timedelta, datetime
import sys
from stock_csv_save import stock_csv_save

# step2. 進入目標網站,爬取盤後資訊
if __name__ == "__main__":
    # Step1 - 爬取今日日期===============================
    date = str(datetime.today().date())
    date = date.replace("-","")
    filename = "stock_value.csv"
    logname = "stock_value_log.txt"
    
    
    # Step2 - Fetch Data From
    # 2_1 Call web data
    # 2_2 create df
    # 2_3 write to csv
    
    # 2_1 Call web data
    try:
        df = get_stock_day(date)
    except:
        print(date + " | No this day data")
         # ====== write to log file =============
        if logname in os.listdir(os.getcwd()):
            with open(logname, 'a') as f:
                f.write(date + " |  No this day data")
        else:
            with open(logname, 'w') as f:
                f.write(date + " |  No this day data")
        sys.exit()

        
    # 2_2 create df
    df = create_df(date, df)
    stock_csv_save(df, filename, logname, date)



