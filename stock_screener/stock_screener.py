import streamlit as st
import requests
import pandas as pd



header=st.container()
inputc=st.container()
ratios=st.container()
sel_col, disp_col =st.columns(2)

with inputc:
        input_feature=st.text_input("Enter the stock to find ratios :", value="aetherindustries")
        input_feature=input_feature.lower().strip().replace(" ","")


with header:
    st.title("Fundamental Analysis Ratios of  NIFTY 500 Stocks")



with ratios:
    data=requests.get(f"http://stock_api_1:80/stock_data?s_name={input_feature}")
    json_data=data.json()
    df=pd.DataFrame(json_data, index=["Year1", "Year2","Year3", "Year4", "Year5"])
    df=df.apply(pd.to_numeric, errors='coerce')
    st.header("Fundamental Ratios")
    st.write(df)

    st.subheader("Return on Capital Employed (%)")
    chart_data = df['Return on Capital Employed (%)']
    st.line_chart(chart_data)

    st.subheader("Current Ratio (X)")
    chart_data = df['Current Ratio (X)']
    st.line_chart(chart_data)

    st.subheader("Retention Ratios (%)")
    chart_data = df['Return on Capital Employed (%)']
    st.line_chart(chart_data)

    st.subheader("MarketCap/Net Operating Revenue (X)")
    chart_data = df['Current Ratio (X)']
    st.line_chart(chart_data)



#aetherindustries
