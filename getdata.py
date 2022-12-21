import requests
import pandas as pd
from datetime import date, timedelta
import mysql.connector
import pymysql
from sqlalchemy import create_engine
import os


stock_list=[2330,2317,2454,2412,6505,2308,2881,1303,1301,2882,
2303,2002,2886,2891,3711,1326,1216,5880,2892,5871,
2603,2884,3045,2207,2880,3008,2912,2885,2382,2395,
"0050",1101,2609,2615,4904,5876,2883,2357,6488,2327,
2890,8069,1590,2801,3034,2887,9910,1605,3037,4938]

dataset_list=["TaiwanStockPriceTick", "TaiwanStockDividend"]#台灣股價歷史逐筆資料表, 股利政策表

#connect db
#engine = create_engine('mysql+pymysql://root:fdhg4322@localhost:3306/test')
#'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'

url = "https://api.finmindtrade.com/api/v4/data"

for i in dataset_list:

    for j in stock_list:   #台股代碼會跳號可能要列個sequence來跑loop
        parameter = {
            "dataset": i,
            "data_id": j,
            "start_date": "2020-01-02",
            "token": "", # 參考登入，獲取金鑰
        }
        resp = requests.get(url, params=parameter)
        data = resp.json()
        data = pd.DataFrame(data["data"])
        data.to_csv("D:/Desktop/stock_proj/" + i + ".csv", mode='a') #mode='a' 小心有舊資料


#data.to_sql('2330',engine,chunksize=100000,index=None)#to database


