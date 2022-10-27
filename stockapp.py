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

Range = st.sidebar.radio(
    "Choose Range",
    ('1W', '1M', '3M','6M','YTD','1Y','2Y','5Y','10Y','ALL'))


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
      
if range = '1W':
     stockretrieve(dt.date.today() - timedelta(days = 7), dt.date.today())

elif range == '1M':
     stockretrieve(dt.date.today() - timedelta(days = 30), dt.date.today())
     
elif range == '3M':
     stockretrieve(dt.date.today() - timedelta(days = 90), dt.date.today())
     
elif range == '6M':
     stockretrieve(dt.date.today() - timedelta(days = 180), dt.date.today())
     
elif range == 'YTD':
     todaysdate = dt.date.today()
     startofyear = todaysdate.replace(month=1, day=1)
     stockretrieve(startofyear, dt.date.today())

elif range == '1Y':
     stockretrieve(dt.date.today() - timedelta(days = 365), dt.date.today())
     
elif range == '2Y':
     stockretrieve(dt.date.today() - timedelta(days = 730), dt.date.today())
     
elif range == '5Y':
     stockretrieve(dt.date.today() - timedelta(days = 1825), dt.date.today())

elif range == '10Y':
     stockretrieve(dt.date.today() - timedelta(days = 3650), dt.date.today())
     
elif range == 'ALL':
     stockretrieve(dt.date.today() - timedelta(days = 50000), dt.date.today())
     
else:
     stockretrieve(start_date, end_date)
