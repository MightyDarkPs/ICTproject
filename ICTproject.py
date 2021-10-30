import streamlit as st
from PIL import Image
import pandas as pd
import base64
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests

st.set_page_config(layout="wide")

image = Image.open('kzt.png')

st.image(image, width=500)

st.title('KZT against other currencies')
st.markdown("""
The main purpose of that webb app is get actual information about currencies
""")
# ---------------------------------#
# About
expander_bar = st.beta_expander("About")
expander_bar.markdown("""
This project was made by Toktaganov Turlykhan, Shaimuran Alisher and Zhardembek Nurmukhammed
""")

# ---------------------------------#

col1 = st.sidebar
col2, col3 = st.beta_columns((2, 1))


# ---------------------------------#
def load_data():
    url = 'https://nationalbank.kz/ru/exchangerates/ezhednevnye-oficialnye-rynochnye-kursy-valyut'
    page = requests.get(url)
    print(page.status_code)

    information = []
    currency = []

    soup = BeautifulSoup(page.text, "html.parser")

    information = soup.findAll('tr')

    res = []
    for tr in information:
        td = tr.find_all('td')
        row = [tr.text.strip() for tr in td if tr.text.strip()]
        if row:
            res.append(row)

    df = pd.DataFrame(res, columns=["Currency", "Symbol", "Price"])
    df['Price'] = pd.to_numeric(df['Price'])
    return df


def load_data_two():
    url = 'http://tng.kz/?city=2'
    page = requests.get(url)
    page.encoding = 'utf-8'
    print(page.status_code)

    information = []
    soup = BeautifulSoup(page.text, "html.parser")

    information = soup.findAll('tr', class_='cours_tr')

    res = []
    for tr in information:
        td = tr.find_all('td')
        row = [tr.text.strip() for tr in td if tr.text.strip()]
        if row:
            res.append(row)

    # print(res)
    dftwo = pd.DataFrame(res, columns=["Name", "Buy Dollar", "Sell Dollar", "Buy Euro", "Sell Euro", "Buy Rub", "Sell Rub",
                                       "Date"])
    return dftwo


def filedownload(df):
    csv = df.to_csv(index=True, encoding='utf-8-sig')
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="KZTcurrency.csv">Download CSV File about KZT currency</a>'
    return href


def filedownloadtwo(dftwo):
    csv = dftwo.to_csv(index=True, encoding='utf-8-sig')
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="ExchangeOffices.csv">Download CSV File about exchange offices</a>'
    return href


# ---------------------------------#
df = load_data()
dftwo = load_data_two()

# ---------------------------------#
col1.header('Input Options')

sort_values = col1.selectbox('Sort values?', ['No', 'Yes'])

col1.subheader('Converter')

selected_currency = col1.selectbox('Currency', df['Symbol'])

number = col1.number_input('Insert a number')
count = 0
for i in range(38):
    if df.loc[i, 'Symbol'] == selected_currency:
        break
    else:
        count = count + 1

col1.write('The current number is ', number * df.loc[count, 'Price'])
number2 = col1.number_input('Insert a tenge')
col1.write('The current number is ', number2 / df.loc[count, 'Price'])

# ---------------------------------#

if sort_values == 'Yes':
    df = df.sort_values(by=['Price'])

col2.subheader('Here information about KZT/other currencies')

col2.dataframe(df)

col2.markdown(filedownload(df), unsafe_allow_html=True)

col2.subheader('Here information about all exchange offices from Nur-Sultan')

col2.table(dftwo)

col2.markdown(filedownloadtwo(dftwo), unsafe_allow_html=True)

# ---------------------------------#
col3.subheader('Bar plot of all currency/KZT')

fig, ax = plt.subplots(figsize=(5, 25))

ax.barh(df['Symbol'], df['Price'], color="red")
plt.subplots_adjust(top=1, bottom=0)
ax.set_xlabel("Price")

for x, y in zip(ax.patches, df['Price']):
    ax.text(10, x.get_y() + x.get_height() / 2, y, color='black', ha='left', va='center')

col3.pyplot(fig)

