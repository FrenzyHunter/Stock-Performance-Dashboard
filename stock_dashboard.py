import streamlit as st     #MADE THIS USING PYTHON AND CHATGPT
import pandas as pd 
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Making An Interactive Stock Dashboard

st.set_page_config(page_title="Stock Dashboard", layout="wide")
st.title("Stock Dashboard")
st.markdown("This dashboard allows you to visualize stock data interactively.")

# Sidebar for user inputs
ticker_input = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL, MSFT):", "AAPL")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2024-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

st.sidebar.button("Fetch Data")
# The above code sets up a sidebar where users can input the stock ticker and date range for fetching stock data.

#To get a calendar type of date input, we do pd.to_datetime("today") to set the default end date to today

# Fetching stock data

data = yf.download(ticker_input, start=start_date, end=end_date)  
# The above code uses yfinance to download stock data for the specified ticker and date range.


# To get this data on the dashboard, we use yfinance library to download stock data
if data.empty:
    st.error("No data found for the given ticker and date range.")
else:
    st.success(f"Data fetched for {ticker_input} from {start_date} to {end_date}.")  

# Getting data of stock on streamlit dashboard
st.subheader("Stock Closing Price")
st.line_chart(data['Close'], use_container_width=True)

#integrating matplotlib to create a good line chart 
st.subheader("Adjusted Close Price")
plt.figure(figsize=(10, 5))
plt.plot(data, linewidth=2, color='blue')
plt.xlabel("Date")
plt.ylabel("Adjusted Close Price")
plt.tight_layout()
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.4)
plt.show()
st.pyplot(plt)

# Moving on to the next part of the code, we will create a bar chart to visualize the stock's volume.

st.subheader("Stock Volume")


# Creating a histogram for stock volume
plt.figure(figsize=(10, 5))
plt.hist(data['Volume'], bins=25, color='orange', edgecolor='black')
plt.xlabel("Date")
plt.ylabel("Volume")
plt.tight_layout()
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.4)
st.pyplot(plt)

#Creating different tabs for different visualizations

Information_slide, pricing_data, fundamentals_data, news, Chat_assitant =  st.tabs(["Information slide", "Pricing Data", "Fundamentals Data","News", "Your personal chat assistant."])
 
with Information_slide:
    st.subheader("Stock Information")
    st.markdown("Here is some basic information about the stock you selected:).")

with pricing_data:
    st.subheader("Stock Pricing Data")
    data2 = data
    data2['%age change'] = data['Close']/ data['Close'].shift(1) - 1
    data2.fillna(0, inplace=True)  # Filling NaN values with 0
    st.write(data2)
    annual_return = data2['%age change'].mean() * 252 * 100  # Assuming 252 trading days in a year
    st.success(f"Annual Return: {annual_return:.2f}%")
    # Standard deviation of returns
    std_dev = data2['%age change'].std() * np.sqrt(252)  # Annualized standard deviation
    st.success(f"Annualized Standard Deviation: {std_dev:.2f}%")


with fundamentals_data:
    if ticker_input:
        ticker_data = yf.Ticker(ticker_input.upper())

        st.subheader("Balance Sheet")
        st.write(ticker_data.balance_sheet)

        st.subheader("Income Statement")
        st.write(ticker_data.financials)

        st.subheader("Cash Flow Statement")
        st.write(ticker_data.cashflow)

from stocknews import StockNews
with news:
    st.header(f'Latest News for {ticker_input}')
    sn = StockNews(ticker_input, save_news=False)
    news_data = sn.read_rss()
    for i in range(10):
        st.subheader(news_data['title'][i])
        st.write(news_data['published'][i])
        st.write(news_data['summary'][i])
        st.write("---")     

    
with Chat_assitant:
    st.title("You can ask all your doubts regarding to the current stock in the chatbox.")

import streamlit as st
import cohere

co = cohere.Client("mi5t5RKsyXZ1p5vmLCix8CCTAa9c6ULDRG4iU3bG")

st.title("Cohere Chat assistant")

prompt = st.text_input("Ask something...")

if prompt:
    response = co.generate(
        model='command',
        prompt=prompt,
        max_tokens=10000000,
        temperature=0.8
    )
    st.write(response.generations[0].text)

