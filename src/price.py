import os
from datetime import datetime, timedelta

import pandas as pd
import requests

data_folder = os.path.join(os.path.dirname(__file__), '..', 'data')

stock_num = '0752.HK'
from_date = str(int((datetime.now() - timedelta(days=1)).timestamp()))
to_date = str(int(datetime.now().timestamp()))

url = "https://query1.finance.yahoo.com/v7/finance/download/{stock_num}?period1={from_date}&period2={to_date}&interval=1d&events=history&includeAdjustedClose=true"
# url = "https://query1.finance.yahoo.com/v7/finance/download/0752.HK?period1=1714026926&period2=1721889195&interval=1d&events=history&includeAdjustedClose=true"
# print(url)
headers = {
    "user-agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
}

print(url.format(stock_num=stock_num, from_date=from_date, to_date=to_date))
session = requests.Session()
response = session.get(url.format(stock_num=stock_num, from_date=from_date, to_date=to_date), headers=headers)
session.close()

# Check if the request was successful
if response.status_code == 200:
  print("Request successful")
  # Process the response content here
  print(response.content)

  df = pd.DataFrame([row.split(',') for row in response.text.split('\n')])
  df.to_csv(os.path.join(data_folder, f'{stock_num}.csv'), index=False, header=False)
else:
  print(f"Request failed with status code: {response.status_code}")
  print(response.content)
