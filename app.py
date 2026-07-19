import streamlit as st
import yesg
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
# Page config
st.set_page_config(page_title="ESGeniusIQ", page_icon="🌱", layout="wide")
st.image("logo.png", width=100)


REQUIRED_ESG_COLS = ['totalEsg', 'environmentScore', 'socialScore', 'governanceScore', 'highestControversy']

# yesg's get_esg_full() column names -> the names the rest of this app expects
_ESG_COLUMN_MAP = {
    'Ticker': 'company_ticker',
    'Total-Score': 'totalEsg',
    'E-Score': 'environmentScore',
    'S-Score': 'socialScore',
    'G-Score': 'governanceScore',
    'Highest Controversy': 'highestControversy',
}


def _fetch_esg(ticker):
    """Fetch and normalize ESG data for one ticker. Returns None on any failure, silently."""
    try:
        esg_data = yesg.get_esg_full(ticker)
        if esg_data is None or esg_data.empty:
            return None
        esg_data = esg_data.rename(columns=_ESG_COLUMN_MAP)
        if not all(c in esg_data.columns for c in REQUIRED_ESG_COLS):
            return None
        return esg_data
    except Exception:
        return None


def get_esg_data(ticker):
    esg_data = _fetch_esg(ticker)
    if esg_data is None:
        st.warning(f"No ESG data found for {ticker}. It may not be covered by Sustainalytics/Yahoo's ESG dataset.")
        return None
    return esg_data

def get_esg_data_for_file(uploaded_file):
    if uploaded_file is not None:
        try:
            tickers_df = pd.read_csv(uploaded_file)
            tickers = tickers_df['ticker_code'].head(100)
            esg_data_list = []
            for ticker in tickers:
                temp = _fetch_esg(ticker)  # skip tickers with no/incomplete ESG data instead of crashing
                if temp is not None:
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

st.title("ESGeniusIQ - ESG Analytics Dashboard")
st.subheader("Strategic ESG Analysis & Sustainability Metrics")

# Main navigation
menu = option_menu("Main Menu", 
                  ["Welcome", "View ESG Score", "Compare ESG Scores", "Bulk ESG Analysis"],
                  icons=['house', 'eye', 'bar-chart', 'upload'], 
                  menu_icon="cast", 
                  default_index=0)

if menu == "Welcome":
    st.markdown("""
    Access comprehensive ESG metrics and sustainability analytics for informed investment decisions 📈
    """)
    
    # Main Features in Three Columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### Single Company Analysis 🔍")
        st.markdown("""
        Detailed ESG breakdown:
        - 📊 Total ESG risk score
        - 🌱 Environmental metrics
        - 👥 Social responsibility
        - ⚖️ Governance standards
        - ⚠️ Controversy tracking
        """)
        
            
    with col2:
        st.markdown("### Peer Comparison 🔄")
        st.markdown("""
        Compare sustainability metrics:
        - 📈 Side-by-side ESG analysis
        - 📊 Component breakdown
        - 📉 Visual comparisons
        - 🎯 Industry benchmarking
        - ⚡ Risk level assessment
        """)
        
            
    with col3:
        st.markdown("### Portfolio Analysis 📝")
        st.markdown("""
        Bulk ESG assessment:
        - 📂 Multiple company analysis
        - 🔍 Portfolio screening
        - 📊 ESG risk overview
        - ⚡ Batch processing
        - 💾 Data export options
        """)
        

    # Analysis Features
    st.markdown("### Analysis Tools 🛠️")
    
    tab1, tab2, tab3 = st.tabs(["Risk Assessment 📊", "Sustainability Metrics 🌱", "Reporting Tools 📑"])
    
    with tab1:
        st.markdown("""
        **ESG Risk Analysis**
        - 📊 Comprehensive risk scoring
        - ⚠️ Controversy level assessment
        - 📈 Industry comparison
        - 📅 Historical tracking
        - 🎯 Risk categorization
        """)
        
    with tab2:
        st.markdown("""
        **Sustainability Performance**
        - 🌍 Environmental impact metrics
        - 👥 Social responsibility indicators
        - ⚖️ Governance standards
        - 🔍 Controversy monitoring
        - 📈 Trend analysis
        """)
        
    with tab3:
        st.markdown("""
        **Reporting & Visualization**
        - 📊 Interactive charts
        - 🔄 Comparative analysis
        - 📉 Risk breakdowns
        - 💾 Data export
        - 📑 Custom reporting
        """)

    # Quick Start Guide
    st.markdown("### Getting Started 🚀")
    with st.expander("Usage Guide"):
        st.markdown("""
        **Single Company Analysis:**
        - 🔍 Enter company ticker symbol
        - 📊 View comprehensive ESG breakdown
        - 📈 Analyze risk components
        - ⚠️ Track controversy levels
        
        **Company Comparison:**
        - 🔄 Select two companies
        - 📊 Compare ESG metrics
        - 👥 View side-by-side analysis
        - 📈 Identify key differences
        
        **Portfolio Assessment:**
        - 📂 Upload CSV with ticker codes
        - ⚡ Process multiple companies
        - 📊 View aggregated results
        - 💾 Export analysis data
        """)

    # Best Practices
    st.markdown("### Analysis Best Practices 💡")
    with st.expander("Tips for Better Analysis"):
        st.markdown("""
        **Effective Analysis:**
        - 🎯 Compare within industry groups
        - ⚠️ Consider controversy levels
        - 📈 Monitor trends over time
        - 🔄 Check data recency
        
        **Risk Assessment:**
        - 📊 Review all ESG components
        - ⚖️ Evaluate controversy impact
        - 🌍 Consider industry context
        - 📈 Track significant changes
        """)

    # Footer with disclaimer
    st.markdown("""
    ---
    *ESG data sourced from Yahoo Finance. Scores and assessments should be considered alongside fundamental analysis.* 📚
    """)

if menu == "View ESG Score":
    ticker = st.text_input("Enter a stock ticker (e.g., KO for Coca-Cola)")
    if st.button("Get ESG Score"):
        esg_data = get_esg_data(ticker)
        if esg_data is not None:
            st.subheader(f"ESG Breakdown for {ticker}")
            
            # Extract ESG Scores
            total_esg = esg_data['totalEsg'].iloc[0]
            env_score = esg_data['environmentScore'].iloc[0]
            soc_score = esg_data['socialScore'].iloc[0]
            gov_score = esg_data['governanceScore'].iloc[0]
            controversy_level = esg_data['highestControversy'].iloc[0]  # Fixed column name

            # Assign qualitative labels
            def classify_esg(score):
                if score < 20:
                    return "Low Risk"
                elif score < 40:
                    return "Medium Risk"
                else:
                    return "High Risk"
            
            def classify_controversy(level):
                labels = ["None", "Low", "Moderate", "High", "Severe"]
                return labels[min(int(level), 4)]  # Ensure index is within range

            esg_label = classify_esg(total_esg)
            controversy_label = classify_controversy(controversy_level)

            # Display Overall ESG Risk Score
            st.markdown(f"### **Overall ESG Risk Score:** {total_esg} ({esg_label})")

            # Display Individual ESG Scores
            col1, col2, col3 = st.columns(3)
            col1.metric("🌱 Environmental", env_score)
            col2.metric("🤝 Social", soc_score)
            col3.metric("🏛 Governance", gov_score)

            # Display Controversy Level
            st.markdown(f"### **Controversy Level:** {controversy_level} ({controversy_label})")
            st.progress(int(controversy_level) / 5)  # Scale 0 to 5

            # Radar Chart Visualization
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
                ticker1: [esg_data1['environmentScore'].values[0], esg_data1['socialScore'].values[0], esg_data1['governanceScore'].values[0]],
                ticker2: [esg_data2['environmentScore'].values[0], esg_data2['socialScore'].values[0], esg_data2['governanceScore'].values[0]]

            })
            st.write(comparison_df)

            # Visualization
            fig = px.bar(comparison_df, x="Category", y=[ticker1, ticker2], barmode='group', title=f"ESG Comparison: {ticker1} vs {ticker2}")
            st.plotly_chart(fig)

elif menu == "Bulk ESG Analysis":
    uploaded_file = st.file_uploader("Upload a CSV file with ticker codes", type=["csv"])
    if uploaded_file is not None:
        if st.button("Get ESG Data"):
            esg_data = get_esg_data_for_file(uploaded_file)
            if esg_data is not None:
                st.write(esg_data)
