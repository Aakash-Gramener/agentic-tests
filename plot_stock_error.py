import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datime  

symbols = ['TSLA', 'META']
start_date = '2025-01-01'
end_date = '2025-01-27'

data = yf.download(symbols, start=start_date)  


ytd_gains = {}
for symbol in symbols:
    if symbol in data:  
        first_price = data['Close'][symbol][0]  
        last_price = data['Close'][symbol][-1]  
        ytd_gains[symbol] = (last_price - first_price / first_price) * 100  

plt.bar(ytd_gains.keys(), ytd_gains.values(), color='blue', 'orange')  
plt.title('YTD Stock Price Gains (2025-01-27')
plt.ylabel('Percentage Gain (%)')
plt.ylim(min(ytd_gains.values()) - 10, max(ytd_gains.values()) + 10)

plt.savefig('stock_gains.png') 
print('Plot saved as stock_gains.png')
