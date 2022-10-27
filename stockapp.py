# Importing Libraries
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
import datetime as dt
from datetime import timedelta

with open("style.css") as f:
      st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True) 

# App Title
st.markdown('''
# Stock Price App
##### Georges Elkassouf

''')

st.write('---')

# Sidebar
st.sidebar.subheader("Parameters")
ticker_list = pd.read_csv("https://raw.githubusercontent.com/georgeselkassouf/Stock-App/main/stocktickers.txt")
tickerSymbol = st.sidebar.selectbox("Stock Ticker", ticker_list)
start_date = st.sidebar.date_input("Start date", dt.date(2019,1,1))
end_date = st.sidebar.date_input("End date", dt.date.today())

# Define Sidebar Columns
side_1, side_2, side_3, side_4, side_5 = st.sidebar.columns(5)

# Define Buttons
with side_1:
    b1 = st.button('1W')

with side_1:
    b6 = st.button('1Y')
      
with side_2:
    b2 = st.button('1M')

with side_2:
    b7 = st.button('2Y')

with side_3:
    b3 = st.button('3M')

with side_3:
    b8 = st.button('5Y')

with side_4:
    b4 = st.button('6M')

with side_4:
    b9 = st.button('10Y')
      
with side_5:
    b5 = st.button('YTD')

with side_5:
    b10 = st.button('ALL')

# Define Main Function
def stockretrieve(start_date, end_date):
     tickerData = yf.Ticker(tickerSymbol)
     tickerDf = pd.DataFrame(tickerData.history(period="1d", start = start_date, end = end_date))
     tickerDf = tickerDf[['Open', 'High', 'Low', 'Close', 'Volume']]

     # Adjusting the Date Column
     tickerDf.reset_index(inplace=True)
     tickerDf['Date'] = tickerDf['Date'].dt.date

     # Ticker Information
     string_logo = '<img src=%s>' % tickerData.info['logo_url']
     st.markdown(string_logo, unsafe_allow_html=True)

     string_name =tickerData.info['longName']
     st.header('**%s**' % string_name)

     st.markdown('#### Summary')
     string_summary = tickerData.info['longBusinessSummary']
     st.info(string_summary)

     st.markdown('#### Industry')
     string_industry = tickerData.info['industry']
     st.info(string_industry)

     st.markdown('#### Country')
     string_country = tickerData.info['country']
     st.info(string_country)

     # Ticker Data
     st.header('**Data**')
     st.write(tickerDf)     
     
     # Define Download to csv Button
     csv = tickerDf.to_csv(index=False).encode('utf-8')
     
     st.download_button(
     label="Download Data ",
     data = csv,
     file_name = "data.csv",
     mime = "text/csv",
     key='download-csv',
     on_click=None
     )

     # Chart
     st.header('**Candlestick Chart**')
      
     fig = go.Figure()

     config = {

      'toImageButtonOptions': {

         'filename': 'Candlestick Chart'
      }

     }
      
     fig.add_trace(go.Candlestick(x=tickerDf['Date'],
          open=tickerDf['Open'],
          high=tickerDf['High'],
          low=tickerDf['Low'],
          close=tickerDf['Close'], name = 'market data'))

     fig.update_layout(
     xaxis_rangeslider_visible=False,
     xaxis_title = 'Date',
     )
      
     st.plotly_chart(fig, config=config)
      
if b1:
     stockretrieve(dt.date.today() - timedelta(days = 7), dt.date.today())

elif b2:
     stockretrieve(dt.date.today() - timedelta(days = 30), dt.date.today())
     
elif b3:
     stockretrieve(dt.date.today() - timedelta(days = 90), dt.date.today())
     
elif b4:
     stockretrieve(dt.date.today() - timedelta(days = 180), dt.date.today())
     
elif b5:
     todaysdate = dt.date.today()
     startofyear = todaysdate.replace(month=1, day=1)
     stockretrieve(startofyear, dt.date.today())

elif b6:
     stockretrieve(dt.date.today() - timedelta(days = 365), dt.date.today())
     
elif b7:
     stockretrieve(dt.date.today() - timedelta(days = 730), dt.date.today())
     
elif b8:
     stockretrieve(dt.date.today() - timedelta(days = 1825), dt.date.today())

elif b9:
     stockretrieve(dt.date.today() - timedelta(days = 3650), dt.date.today())
     
elif b10:
     stockretrieve(dt.date.today() - timedelta(days = 50000), dt.date.today())
     
elif start_date:
     stockretrieve(start_date, end_date)
