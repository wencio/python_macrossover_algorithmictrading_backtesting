import yfinance as yf
import pandas as pd
from backtesting import Backtest, Strategy
import streamlit as st


st.title('Finance Dashboard')
tickers = ('TSLA','AAPL','MSFT','BTC-USD','ETH-USD','SPY')
dropdown = st.multiselect('Pick your assets',tickers)

st.title('Short MA')
short_ma = ('7','10','20','50','100','200')
short_dropdown = st.multiselect('Pick your Short MA',short_ma)


st.title('Long MA')
long_ma = ('7','10','20','50','100','200')
long_dropdown = st.multiselect('Pick your Long MA ',long_ma)


start = st.date_input('Start',value=pd.to_datetime('2019-01-01'))
end = st.date_input('End',value=pd.to_datetime('today'))

if (len(dropdown) > 0) and (len(short_dropdown)> 0 )and (len(long_dropdown) >0):
    symbol  = yf.Ticker(dropdown[0])
    price_data = symbol.history(interval="1d",start = start, end = end)
    print (price_data)


    def MovingAverage(price,period):
         return pd.Series(price).rolling(period).mean()

    class SMACross(Strategy):
        n_short = int(short_dropdown[0])
        n_long =  int(long_dropdown[0])

        def init(self):
         close = self.data.Close
         self.ma_short = self.I(MovingAverage,close,self.n_short)
         self.ma_long = self.I(MovingAverage,close,self.n_long)

        def next(self):
         if self.ma_short[-2] < self.ma_long[-2]:
            if self.ma_short[-1] > self.ma_long[-1]:
               self.buy()
            elif self.ma_short[-2] > self.ma_long[-2]:
              if self.ma_short[-1]  < self.ma_long[-1]:
               if self.position:
                 self.position.close()

    bt = Backtest(price_data,SMACross,cash = 10000,commission= 0,exclusive_orders = True)
    output = bt.run()
    print (output)
    bt.plot()
