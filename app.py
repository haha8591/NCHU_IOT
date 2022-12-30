from flask import Flask, render_template, request, jsonify,url_for,redirect
import requests
import pandas as pd
from datetime import date, timedelta
import os
import yfinance as yf
import matplotlib.pyplot as plt
import datetime as dt
import datetime
import matplotlib
import matplotlib.ticker as ticker
from stocker import Stocker  #記得放在stocker下

#創建Flask物件app并初始化
app = Flask(__name__)

#通過python裝飾器的方法定義路由地址
@app.route("/index")
def root():
    #製作當日台股加權指數圖
    today=datetime.date.today()
    today=today.strftime("%Y-%m-%d")#當天的變數轉成str
    url = "https://api.finmindtrade.com/api/v4/data"
    parameter = {
        "dataset": "TaiwanVariousIndicators5Seconds",
        "start_date": "2022-12-30",#新的dataset太大,不好畫圖,之後修正
        "token": "", # 參考登入，獲取金鑰
    }
    
    data = requests.get(url, params=parameter)
    data = data.json()
    data = pd.DataFrame(data['data'])

    # 畫圖
    len(data['date'])
    data['date']=pd.to_datetime(data['date'])
    data['time']=data['date'].dt.time
    data["time"]=data["time"].astype(str)

    plt.plot(data["time"], data["TAIEX"],"r")  
    plt.title('TaiwanVariousIndicators'+'('+today+')', {"fontsize":15})

    plt.xticks(range(0,len(data['time']),810))#三千多筆/4hr
    plt.savefig('D:\\Desktop\\NCHU_IOT-main\\Stock_final\\static\img\\TAIEX.png')    

    return render_template("index.html")

@app.route('/table')#url地址
def table():
    return render_template("tables.html")   

@app.route('/login')
def login():
    return render_template("login.html")

@app.route("/chart", methods=["POST", "GET"])
def fetchdata_to_js():
    if request.method == 'POST':
        #從tables.html拿股票代號
        stockNo=request.values['stockNo']

        #用股票代號抓預測資料
        start_date = '2012-01-01'
        df = yf.download(stockNo, start=start_date)#(stockNo, start=start_date)
        df = df.reset_index()
        stock = Stocker(stockNo, df)
        
        #未來10天股價  預測同時並生成圖片
        stock.create_prophet_model(days = 10, chart_name=stockNo)
        
        ########我的電腦跑這兩個有問題但先把圖片改好了,幫我測一下######
        #短中長期趨勢
        #stock.changepoint_prior_analysis(changepoint_priors=[0.001, 0.05, 0.1, 0.2], chart_name=stockNo)
        #回測
        #stock.evaluate_prediction(chart_name=stockNo)
        ##########################

        #轉換日期型態(當天)
        #stock.max_date=stock.max_date.to_pydatetime()
        
        #data load to database
        #sel_toDB[["ds", "trend"]].to_sql(i[0:4], engine, chunksize=10000,index=None)
        return render_template("charts.html", chart_name=stockNo)
    
    return render_template("charts.html")


if __name__ == '__main__':
    #定義app在8080埠運行
    app.run(host="localhost",port=8000,debug=True)
