from datetime import datetime
import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_datareader.data as web
import capm_fuctions

st.set_page_config(
    page_title="CAPM",
    page_icon="chart_with_upwards_trend",
    layout="wide"
)

st.title("Capital Asset Pricing Model")

# Getting input from the user

col1, col2 = st.columns([1, 1])
with col1:
    stocks_list = st.multiselect("Choose 4 stocks", ('TSLA', 'AAPL', 'NFLX', 'MSFT', 'MGM', 'AMZN', 'NVDA', 'GOOGL'), ['TSLA', 'AAPL', 'AMZN', 'GOOGL'])
with col2:
    year = st.number_input("Number of years", 1, 10)

# Downloading data for S&P 500

try:
  end = datetime.now().date()
  start = datetime.date(datetime.now() - pd.DateOffset(years=year))
  
  SP500 = web.DataReader(['sp500'], 'fred', start, end)
  
  stocks_df = pd.DataFrame()
  
  for stock in stocks_list:
      data = yf.download(stock, period=f'{year}y')
      stocks_df[f'{stock}'] = data['Close']
  
  stocks_df.reset_index(inplace=True)
  SP500.reset_index(inplace=True)
  
  SP500.columns = ['Date', 'sp500']
  stocks_df['Date'] = stocks_df['Date'].astype('datetime64[ns]')
  stocks_df = pd.merge(stocks_df, SP500, on='Date', how='inner')
  
  col1, col2 = st.columns([1, 1])
  with col1:
      st.markdown("### Dataframe head")
      st.dataframe(stocks_df.head(), use_container_width=True)
  
  with col2:
      st.markdown("### Dataframe tail")
      st.dataframe(stocks_df.tail(), use_container_width=True)
  
  col1, col2 = st.columns([1, 1])
  with col1:
      st.markdown("### Price of all the Stocks")
      st.plotly_chart(capm_fuctions.interactive_plot(stocks_df))
  
  with col2:
      st.markdown("### Price of all the Stocks (After Normalizing)")
      st.plotly_chart(capm_fuctions.interactive_plot(capm_fuctions.normalize(stocks_df)))
  
  stock_daily_return = capm_fuctions.daily_return(stocks_df)
  print(stock_daily_return.head())
  
  beta = {}
  alpha = {}
  
  for i in stock_daily_return.columns:
      if i != 'Date' and i != 'sp500':
          b, a = capm_fuctions.calculate_beta(stock_daily_return, i)  # Use stock_daily_return here
          beta[i] = b
          alpha[i] = a
  
  print(beta, alpha)
  
  
  beta_df=pd.DataFrame(columns=['Stock','Beta Value'])
  beta_df['Stock']=beta.keys()
  beta_df['Beta Value'] = [str(round(1,2))for i in beta.values()]
  
  
  with col1:
      st.markdown('### Calculated Beta Values')
      st.dataframe(beta_df,use_container_width=True)
  
  rf=0;
  rm=stock_daily_return['sp500'].mean()*252
  
  return_df = pd.DataFrame()
  return_value=[]
  for stock,value in beta.items():
      return_value.append(str(round(rf+(value*(rm-rf)),2)))
  
  return_df['Stock'] = stocks_list
  
  return_df['Return Value'] = return_value
  
  with col2:
      st.markdown('### Calculated Return using CAPM')
  
      st.dataframe(return_df,use_container_width=True)
  
except:
    st.write("Please select valid inputs")


try:
    import yfinance as yf
except ModuleNotFoundError as e:
    print("Error importing yfinance:", e)
















