import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

def get_esg_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        esg_data = stock.sustainability
        if esg_data is not None:
            esg_data = esg_data.transpose()
            esg_data.insert(0, 'company_ticker', ticker)  # Move ticker to the first column
            if 'maxAge' in esg_data.columns:
                max_age = esg_data.pop('maxAge')
                esg_data['maxAge'] = max_age  # Move maxAge to the last column
            return esg_data
        else:
            st.warning(f"No ESG data found for {ticker}.")
            return None
    except Exception as e:
        st.error(f"Error retrieving data for {ticker}: {e}")
        return None

def get_esg_data_for_file(uploaded_file):
    if uploaded_file is not None:
        try:
            tickers_df = pd.read_csv(uploaded_file)
            tickers = tickers_df['ticker_code'].head(100)
            esg_data_list = []
            for ticker in tickers:
                stock = yf.Ticker(ticker)
                if stock.sustainability is not None:
                    temp = stock.sustainability.transpose()
                    temp.insert(0, 'company_ticker', ticker)
                    if 'maxAge' in temp.columns:
                        max_age = temp.pop('maxAge')
                        temp['maxAge'] = max_age  # Move maxAge to the last column
                    esg_data_list.append(temp)
            if esg_data_list:
                return pd.concat(esg_data_list, ignore_index=True)
            else:
                st.warning("No ESG data found for the provided tickers.")
                return None
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
            st.subheader(f"ESG Breakdown for {ticker}")
            
            # Get scores directly from columns
            total_esg = esg_data['totalEsg'].iloc[0]
            env_score = esg_data['environmentScore'].iloc[0]
            soc_score = esg_data['socialScore'].iloc[0]
            gov_score = esg_data['governanceScore'].iloc[0]
            # Radar Chart
            categories = ['Environment', 'Social', 'Governance']
            values = [env_score, soc_score, gov_score]
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(r=values + [values[0]],
                                          theta=categories + [categories[0]],
                                          fill='toself', name=ticker))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True)),
                              showlegend=True)
            st.plotly_chart(fig)

elif menu == "Compare ESG Scores":
    ticker1 = st.text_input("Enter first stock ticker")
    ticker2 = st.text_input("Enter second stock ticker")
    if st.button("Compare"):
        esg_data1 = get_esg_data(ticker1)
        esg_data2 = get_esg_data(ticker2)
        if esg_data1 is not None and esg_data2 is not None:
            comparison_df = pd.DataFrame({
                "Category": ['Environment', 'Social', 'Governance'],
                ticker1: [esg_data1.xs('environmentScore', level=1).iloc[0], esg_data1.xs('socialScore', level=1).iloc[0], esg_data1.xs('governanceScore', level=1).iloc[0]],
                ticker2: [esg_data2.xs('environmentScore', level=1).iloc[0], esg_data2.xs('socialScore', level=1).iloc[0], esg_data2.xs('governanceScore', level=1).iloc[0]]
            })
            st.write(comparison_df)

            # Visualization
            fig = px.bar(comparison_df, x="Category", y=[ticker1, ticker2], barmode='group', title=f"ESG Comparison: {ticker1} vs {ticker2}")
            st.plotly_chart(fig)

elif menu == "Upload File for ESG Data":
    uploaded_file = st.file_uploader("Upload a CSV file with ticker codes", type=["csv"])
    if uploaded_file is not None:
        if st.button("Get ESG Data"):
            esg_data = get_esg_data_for_file(uploaded_file)
            if esg_data is not None:
                st.write(esg_data)
