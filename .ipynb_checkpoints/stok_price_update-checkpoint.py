# -*- coding: utf-8 -*-
# # FUNCTION

def create_df(date, df):
    # 重新定義漲跌價差，將負號入數值之中。
    
    s = df
    s.columns = ['stockno', 'stock_name', 'shares', 'turnover', 'amount',  'open',  'high',
                 'low',   'close', 'negpos' ,'change', 'finalprice', 'finalamount', 'finalsoldprice', 'finalsoldamount', 'PEratio']
                #"證券代號"  "證券名稱"   "成交股數","成交筆數",  "成交金額","開盤價","最高價",
                #"最低價","收盤價",  "漲跌(+/-)"   "漲跌價差", "最後揭示買價", "最後揭示買量" , "最後揭示賣價"  , "最後揭示賣量" ,  "本益比"
    s["change"][s["negpos"]=="-"]=-s["change"][s["negpos"]=="-"]
    del s["negpos"]
    s['shares'] = s['shares'].str.replace(',','')
    s['turnover'] = s['turnover'].str.replace(',','')
    s['amount'] = s['amount'].str.replace(',','')
    s['date'] = date #新增日期
    s['month'] = date[4:6]  #新增月份欄位
    s['day'] = date[6:8]   #新增日欄位
    return s


def get_stock_day(date):
    r = requests.post('http://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + date + '&type=ALL')
    # step3. 篩選出個股盤後資訊
    str_list = []
    for i in r.text.split('\n'):
        if len(i.split('",')) == 17 and i[0] != '=':       
            i = i.strip(",\r\n")
            str_list.append(i) 
    # step4. 印出選股資訊
    df = pd.read_csv(StringIO("\n".join(str_list)))  
    return df





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

# # MAIN
# ## 設定開始時間 : date
# ## 設定檔案名稱 : filename
# ## 設定記錄檔名稱 : logname

# +
# step2. 進入目標網站,爬取盤後資訊
if __name__ == "__main__":
    # Step1 - 爬取今日日期===============================
    date = str(datetime.today().date())
    date = date.replace("-","")
    filename = "stock_date.csv"
    logname = "stock_date_log.txt"
    
    # Step2 - Fetch Data Form
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
#     # 2_3 write to csv
#     if filename in os.listdir(wcd_data_dir):
#         with open(wcd_data_dir + "\\" + filename, 'a') as f:
#             df.to_csv(f, header=False)
#     else:
#         with open(wcd_data_dir + "\\" + filename, 'w') as f:
#             df.to_csv(f)
#     print(date + " | Crawler Done")

    
    
#     # ====== write to log file =============
#     if logname in os.listdir(wcd):
#         with open(wcd + "\\" + logname, 'a') as f:
#             f.write(date + " | Crawler Done")
#     else:
#         with open(wcd + "\\" + logname, 'w') as f:
#             f.write(date + " | Crawler Done")
# -


