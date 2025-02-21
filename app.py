import streamlit as st
import yfinance as yf
import pandas as pd
from streamlit_option_menu import option_menu
import os

def get_esg_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        esg_data = stock.sustainability.transpose()
        esg_data.insert(0, 'company_ticker', ticker)  # Move ticker to the first column
        return esg_data
    except Exception as e:
        st.error(f"Error retrieving data for {ticker}: {e}")
        return None

def get_esg_data_for_file(uploaded_file):
    if uploaded_file is not None:
        try:
            tickers_df = pd.read_csv(uploaded_file)
            tickers = tickers_df['ticker_code'].head(100)
            esg_data = pd.DataFrame()
            for ticker in tickers:
                stock = yf.Ticker(ticker)
                if stock.sustainability is not None:
                    temp = stock.sustainability.transpose()
                    temp.insert(0, 'company_ticker', ticker)
                    esg_data = esg_data.append(temp)
            return esg_data
        except Exception as e:
            st.error(f"Error processing file: {e}")
            return None
    else:
        st.warning("Please upload a valid file.")
        return None

st.title("ESG Dashboard")

menu = option_menu("Main Menu", ["View ESG Score", "Compare ESG Scores", "Upload File for ESG Data"],
                   icons=['eye', 'bar-chart', 'upload'], menu_icon="cast", default_index=0)

if menu == "View ESG Score":
    ticker = st.text_input("Enter a stock ticker (e.g., KO for Coca-Cola)")
    if st.button("Get ESG Score"):
        esg_data = get_esg_data(ticker)
        if esg_data is not None:
            st.write(esg_data)

elif menu == "Compare ESG Scores":
    ticker1 = st.text_input("Enter first stock ticker")
    ticker2 = st.text_input("Enter second stock ticker")
    if st.button("Compare"):
        esg_data1 = get_esg_data(ticker1)
        esg_data2 = get_esg_data(ticker2)
        if esg_data1 is not None and esg_data2 is not None:
            comparison = pd.concat([esg_data1, esg_data2])
            st.write(comparison)

elif menu == "Upload File for ESG Data":
    uploaded_file = st.file_uploader("Upload a CSV file with ticker codes", type=["csv"])
    if uploaded_file is not None:
        if st.button("Get ESG Data"):
            esg_data = get_esg_data_for_file(uploaded_file)
            if esg_data is not None:
                st.write(esg_data)
