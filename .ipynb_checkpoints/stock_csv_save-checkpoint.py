# -*- coding: utf-8 -*-
# ### Stock csv Save function
# #### 因為不同的股票抓取程式用的save邏輯相似，所以寫一個function去處理。
# input : df, filename, logname

# +

import os 
def stock_csv_save(df, filename, logname, date):
    
    wcd = os. getcwd()
    wcd_dir = os.path.dirname(wcd)
    wcd_data_dir = wcd_dir+"\\STOCK_DATA"
    
    # 2_3 write to csv
    if filename in os.listdir(wcd_data_dir):
        with open(wcd_data_dir + "\\" + filename, 'a') as f:
            df.to_csv(f, header=False)
    else:
        with open(wcd_data_dir + "\\" + filename, 'w') as f:
            df.to_csv(f)
    print(date + " | Crawler Done")

    
    # ====== write to log file =============
    if logname in os.listdir(wcd):
        with open(wcd + "\\" + logname, 'a') as f:
            f.write(date + " | Crawler Done")
    else:
        with open(wcd + "\\" + logname, 'w') as f:
            f.write(date + " | Crawler Done")
