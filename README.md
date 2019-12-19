## 台股爬蟲程式 (TWSE台灣證券交易所)
### 須於下載後另外建立STOCK_DATA目錄於上一層目錄下
ex: D:/STOCK → 須建立 D:/STOCK_DATA
### 各項程式功能如下
1. stok_price_by_date.py ：抓取歷史資料
- 設定以下變數資訊
  1. date = '20150422' (從當點時間往前一天開始抓取股票資料)
  2. filename = "stock_date.csv" (檔案名稱設定，每日股價資訊-所有上市股票)
  3. logname = "stock_date_log.txt" (檔案名稱設定，紀錄是否完成爬取)

- 抓取結果
  1. 存於STOCK目錄下
logname :紀錄是否完成爬取
  2. 存於此資料夾上一層目錄的STOCK_DATA目錄(須自行創建)
filename :每日股價資訊-所有上市股票
----
2. stok_price_update.py：抓取最新資料
- 設定以下變數資訊
  1. filename = "stock_date.csv" (檔案名稱設定，每日股價資訊-所有上市股票)
  2. logname = "stock_date_log.txt" (檔案名稱設定，紀錄是否完成爬取)

- 抓取結果
  1. 存於STOCK目錄下
logname :紀錄是否完成爬取
  2. 存於此資料夾上一層目錄的STOCK_DATA目錄(須自行創建)
filename :每日股價資訊-所有上市股票
----
3. stok_value_by_date.py ：抓取歷史資料
- 設定以下變數資訊
  1. date = '20150422' (從當點時間往前一天開始抓取股票價值)
  2. filename = "stock_value.csv" (檔案名稱設定，每日股票價值-所有上市股票)
  3. logname = "stock_value_log.txt" (檔案名稱設定，紀錄是否完成爬取)

- 抓取結果
  1. 存於STOCK目錄下
logname :紀錄是否完成爬取
  2. 存於此資料夾上一層目錄的STOCK_DATA目錄(須自行創建)
filename :每日股價資訊-所有上市股票
----
4. stok_value_update.py：抓取最新資料
- 設定以下變數資訊
  1. filename = "stock_value.csv" (檔案名稱設定，每日股票價值-所有上市股票)
  2. logname = "stock_value_log.txt" (檔案名稱設定，紀錄是否完成爬取)

- 抓取結果
  1. 存於STOCK目錄下
logname :紀錄是否完成爬取
  2. 存於此資料夾上一層目錄的STOCK_DATA目錄(須自行創建)
filename :每日股價資訊-所有上市股票