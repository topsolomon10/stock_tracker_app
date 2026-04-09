import streamlit as st
import yfinance as yf
import pandas as pd
from difflib import get_close_matches
from streamlit_autorefresh import st_autorefresh

# ------------------ CONFIGURATION ------------------
st.set_page_config(page_title="Stock Market Price Tracker", page_icon="📈")
st.title("Stock Market Price Tracker")
st.write("Real-Time Market Tracker")

st_autorefresh(interval=30000, key="datarefresh")

# ------------------ CACHE FUNCTION ------------------
@st.cache_data(ttl=60, show_spinner=False)
def get_stock_data(symbol):
    stock = yf.Ticker(stock_symbol)
    return stock.history(period="1mo")

# ------------------ SIDEBAR ------------------
st.sidebar.header("Settings")

valid_symbols = ["AAPL", "TSLA", "MSFT", "GOOGL", "AMZN", "NFLX", "META", "NVDA", "JPM", "V"]
stock_symbol = st.text_input("Enter stock symbol").upper()
target_price = st.sidebar.number_input("Target Price", value=0.0, min_value=0.0)

alert_type = st.sidebar.selectbox("Alert Type", ["Above", "Below"])

# ------------------ MAIN ------------------
if stock_symbol:
    data = get_stock_data(stock_symbol)

    if data.empty:
        st.error(f"Invalid stock symbol")
        suggestions = get_close_matches(stock_symbol, valid_symbols, n=3, cutoff=0.5)
        if suggestions:
            st.info(f"Did you mean: {','.join(suggestions)}?")
    else:
        # -------- PRICE CALCULATIONS --------
        price = data["Close"].iloc[-1]
        prev_price = data["Close"].iloc[-2]
        change = price - prev_price
        percent = (change / prev_price) * 100
        
        # -------- METRICS --------
        col1, col2, col3 = st.columns(3)

        col1.metric("Current Price", f"${price:.2f}", f"{change:.2f}")
        col2.metric("Change %", f"{percent:.2f}%")
        col3.metric("Volume", int(data["Volume"].iloc[-1]))

        st.markdown("---")

         # -------- CHART --------
        st.subheader("📈 Price Chart (1 Month)")
        st.line_chart(data["Close"])

        # -------- ALERTS --------
        if target_price > 0:
            if alert_type == "Above" and price >= target_price:
                st.error(f"Target reached! Price is ABOVE your target (${target_price})")
            elif alert_type == "Below" and price <= target_price:
                st.warning(f"Price has dropped BELOW your target (${target_price})")
            else:
                st.info("Waiting for target...")
else:   
    st.info("Please enter a stock symbol to continue")