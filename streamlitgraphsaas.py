import streamlit as st 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 

if 'file_csv_key' not in st.session_state:
    st.session_state['file_csv_key'] = False

if 'file_other_excel_key' not in st.session_state:
    st.session_state['file_other_excel_key'] = False

st.header('''🚀 _Data To Graph Generator_ 🚀 ''')

st.subheader(''' ➡️:rainbow[Upload your Data]⬅️ ''')

uploaded_file = st.file_uploader("Upload your datasheet here! ")

st.subheader(''' Type of Data ''')

col1, col2, col3 = st.columns(3)
the_file_csv = col1.button(".CSV ")
the_file_xlsx = col2.button(".XLSX")
the_file_xls = col3.button(".XLS")


if the_file_csv:
    st.session_state['file_csv_key'] = True
    st.session_state['file_other_excel_key'] = False
elif the_file_xlsx or the_file_xlsx:
    st.session_state['file_other_excel_key'] = True
    st.session_state['file_csv_key'] = False

if uploaded_file:
    if st.session_state['file_csv_key']:
        dataframe = pd.read_csv(uploaded_file)
    elif st.session_state['file_other_excel_key']:
        dataframe = pd.read_excel(uploaded_file)
    else:
        dataframe = False
        st.info("Please select a file format.")
else:
    st.info("Please upload a file to proceed.")

if uploaded_file:
    x = st.selectbox("x axis", dataframe.columns[:])
    y = st.selectbox("y axis", dataframe.columns[:])

if uploaded_file and x and y:
    st.line_chart(dataframe, x = x, y = y)
    fig, ax = plt.subplots()
    sns.lineplot(data=dataframe, x=x, y=y, ax=ax)
    st.pyplot(fig)

    if st.button("download"):
        plt.savefig("matplotfigures.png")