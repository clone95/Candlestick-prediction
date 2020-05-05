import yfinance as yf

msft = yf.Ticker("MSFT")

for el in msft.info:
    print(el, msft.info[el])