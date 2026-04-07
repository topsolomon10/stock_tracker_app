from symtable import Symbol
import streamlit as st
import yfinance as yf
import pandas as pd
from difflib import get_close_matches
from streamlit_autorefresh import st_autorefresh


st.title("Stock Market Price Tracker")
st.write("Welcome! Enter a stock symbol to get started")

st_autorefresh(interval=5000, key="datarefresh")


valid_symbols = ["AAPL", "TSLA", "MSFT", "GOOGL", "AMZN", "NFLX", "META", "NVDA", "JPM", "V"]
stock_symbol = st.text_input("Enter stock symbol")


if stock_symbol:
    target_price = st.number_input("Set Target Price (optional)", value = 0.0, min_value = 0.0, step = 1.0)
    alert_type =st.selectbox("Alert Type", ["Above", "Below"])

    stock = yf.Ticker(stock_symbol)
    data = stock.history(period="1d")

    if data.empty:
        st.error(f"Inavlid stock symbol")
        suggestions = get_close_matches(stock_symbol, valid_symbols, n=3, cutoff=0.5)
        if suggestions:
            st.info(f"Did you mean: {','.join(suggestions)}?")
    else:
        price = data["Close"].iloc[-1]
        st.success(f"Current Price of {stock_symbol}: ${price:.2f}")

    if target_price > 0:
        if alert_type == "Above" and price >= target_price:
            st.error(f"Target reached! Price is ABOVE your target (${target_price})")
        elif alert_type == "Below" and price <= target_price:
            st.warning(f"Price has dropped BELOW your target (${target_price})")

    data = stock.history(period="1mo")
    st.subheader("Price Chart (1 Month)")
    st.line_chart(data["Close"])

else:   
    st.info("Please type a stock symbol to continue.")