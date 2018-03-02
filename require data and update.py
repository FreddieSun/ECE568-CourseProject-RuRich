import sys
import pymysql
import requests
import json
import pprint
def requireintradailydata(interval,symbol):
  url = "https://www.alphavantage.co/query"
  function = "TIME_SERIES_INTRADAY"
#  symbol = [ "FB",  "AMZN", "MSFT", "GOOG",  "IBM", "INTC", "AMD","BAC","MS","GS" ]
  api_key = "C8QMHROQL5ID2AYU"    
  csv="csv"
#  interval="1min"
  data = { "function": function, 
         "symbol": symbol, 
         "apikey": api_key,
         "datatype":csv,
         "interval":interval} 
  page = requests.get(url, params = data)
  outFile = "D:\mysql\mysql-5.7.21-winx64\data\INTRADAILY\\"+interval+symbol+".csv"
  with open(outFile, 'w') as oF:
      oF.write(page.text.replace('\r\n','\n'))
a=str(input("Please Input Stock Name: "))
b=str(input("(1min, 5min, 15min, 30min, 60min)\n Please Input Time Interval: "))
requireintradailydata(b,a)


def requirehistorydata(function,symbol):
  url = "https://www.alphavantage.co/query"
  if function=="DAILY":
      functioninpu="TIME_SERIES_DAILY"
  elif function=="WEEKLY":
      functioninpu="TIME_SERIES_WEEKLY"
  elif function=="MONTHLY":
      functioninpu="TIME_SERIES_MONTHLY"
  else: 
      print("The word is wrong")
      sys.exit(1)      
#  symbol = [ "FB",  "AMZN", "MSFT", "GOOG",  "IBM", "INTC", "AMD","BAC","MS","GS" ]
  api_key = "C8QMHROQL5ID2AYU"    
  csv="csv"
#  interval="1min"
  data = { "function": functioninpu, 
         "symbol": symbol, 
         "apikey": api_key,
         "datatype":csv
         } 
  page = requests.get(url, params = data)
  if function=="DAILY":
     outFile = "D:\mysql\mysql-5.7.21-winx64\data\DAILY\\"+function+symbol+".csv"
  elif function=="WEEKLY":
     outFile = "D:\mysql\mysql-5.7.21-winx64\data\WEEKLY\\"+function+symbol+".csv"
  elif function=="MONTHLY":
     outFile = "D:\mysql\mysql-5.7.21-winx64\data\MONTHLY\\"+function+symbol+".csv"
  with open(outFile, 'w') as oF:
      oF.write(page.text.replace('\r\n','\n'))
c=str(input("Please Input Stock Name: "))
d=str(input("(DAILY,WEEKLY,MONTHLY)\n Please Input Time Interval: "))
requirehistorydata(d,c)

# 打开数据库连接
db = pymysql.connect("127.0.0.1","root","password","ece568" ,charset='utf8')

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# SQL 查询语句
#sql="load data infile"+"'D:\DAILY\DAILYGOOG.csv'"
sql = """load data infile 'D:\\mysql\\mysql-5.7.21-winx64\\data\\MSFT.csv'
into table MSFTTable
fields terminated by ',' optionally enclosed by '"' escaped by '"'
lines terminated by '\r\n';"""
#sqlo = "SELECT * FROM AAPL"
try:
    # 执行SQL语句
    cursor.execute(sql)
#    cursor.execute(sqlo)
    # 获取所有记录列表
    results = cursor.fetchall()
#    print(results)
    print(len(results[0]))
    for row in results:
        stock = "MSFT"
        timestamp = row[0]
        opencost=row[1]
        high=row[2]
        low = row[3]
        close = row[4]
        volume=row[5]
        # 打印结果
        print(" ")
        print("stock:%s,timestamp:%s,open:%s,high:%s,low:%s,close:%s,volume:%s" %(stock, timestamp,opencost,high,low,close,volume ))
    # print(results)
except:
    print("Error: unable to fetch data")
# 关闭数据库连接
db.close()
