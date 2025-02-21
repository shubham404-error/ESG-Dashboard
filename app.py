import streamlit as st
import yfinance as yf
import pandas as pd
from streamlit_option_menu import option_menu

def get_esg_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        esg_data = stock.sustainability.transpose()
        esg_data['company_ticker'] = ticker
        return esg_data
    except Exception as e:
        st.error(f"Error retrieving data for {ticker}: {e}")
        return None

st.title("ESG Dashboard")

menu = option_menu("Main Menu", ["View ESG Score", "Compare ESG Scores"],
                   icons=['eye', 'bar-chart'], menu_icon="cast", default_index=0)

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
