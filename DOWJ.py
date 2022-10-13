
import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import yfinance as yf
st.title('Dow Jones Industrial App')


st.markdown("""
Welcome
""")

st.sidebar.header('User Input Features')


@st.cache
def load_data():
    url = 'https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average#Components'
    html = pd.read_html(url, header=0)
    df = html[1]
    return df


df = load_data()

sector = df.groupby('Industry')

sorted_sector_unique = sorted(df['Industry'].unique())
selected_sector = st.sidebar.multiselect(
    'Industry', sorted_sector_unique, sorted_sector_unique)

# Filtering data
df_selected_sector = df[(df['Industry'].isin(selected_sector))]

st.header('Display Companies in Selected Sector')
st.write('Data Dimension: ' + str(df_selected_sector.shape[0]) + ' rows and ' + str(
    df_selected_sector.shape[1]) + ' columns.')
st.dataframe(df_selected_sector)

# def filedownload(df):
#     csv = df.to_csv(index=False)
#     b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
#     href = f'<a href="data:file/csv;base64,{b64}" download="SP500.csv">Download CSV File</a>'
#     return href

# st.markdown(filedownload(df_selected_sector), unsafe_allow_html=True)



# len(sorted_sector_unique)

data = yf.download(
    # tickers = list(df.Symbol),
    tickers=list(df_selected_sector[:10].Symbol),
    period="ytd",
    interval="1d",
    group_by='ticker',
    auto_adjust=True,
    prepost=True,
    threads=True,
    proxy=None
)


# # def price_plot(symbol):
# df = pd.DataFrame(data['AAPL'].Close)
# df['Date'] = df.index
st.set_option('deprecation.showPyplotGlobalUse', False)
def price_plot(symbol):
    df = pd.DataFrame(data[symbol].Close)
    df['Date'] = df.index    
    plt.fill_between(df.Date, df.Close, color='darkgreen', alpha=0.3)
    plt.plot(df.Date, df.Close, color='blue', alpha=0.8)
    plt.xticks(rotation=90)
    plt.title(symbol, fontweight='bold')
    plt.xlabel('Date', fontweight='bold')
    plt.ylabel('Closing Price', fontweight='bold')
    return st.pyplot()


num_company = st.sidebar.slider('Number of Companies', 1, 5)

if st.button('Show Plots'):
    st.header('Stock Closing Price')
    for i in list(df_selected_sector.Symbol)[:num_company]:
        price_plot(i)
