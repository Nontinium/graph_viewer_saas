import streamlit as st 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
import io

st.set_page_config(
    page_title="Hello world",
    page_icon="chart_with_upwards_trend",
    layout="centered",
)

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

dataframe = None
if uploaded_file:
    try:
        if st.session_state['file_csv_key']:
            dataframe = pd.read_csv(uploaded_file)
        elif st.session_state['file_other_excel_key']:
            dataframe = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Error loading file: {e}")
else:
    st.info("Please upload a file to proceed.")

if dataframe is not None:
    x = st.selectbox("x axis", dataframe.columns[:])
    y = st.selectbox("y axis", dataframe.columns[:])
    plot_type = st.selectbox("plot type", ['line plot', 'scatter plot'])
    st.text(plot_type)

if uploaded_file and x and y:
    #st.line_chart(dataframe, x = x, y = y)
    fig, ax = plt.subplots()
    if plot_type == "line plot":
        sns.lineplot(data=dataframe, x=x, y=y, ax=ax)
    elif plot_type == "scatter plot":
        sns.scatterplot(data=dataframe, x=x, y=y, ax=ax)
    else:
        sns.boxplot(data=dataframe, x=x, y=y, ax=ax)
    st.pyplot(fig)

    image_download_name = st.text_input("imagename", "image_name.png")

    if image_download_name:
        file_extension = image_download_name.split('.')[-1]
        
        img = io.BytesIO()
        
        if file_extension == 'png':
            plt.savefig(img, format='png')
        elif file_extension == 'svg':
            plt.savefig(img, format='svg')
        img.seek(0)
        st.download_button(
            label="Download image",
            data=img,
            file_name=image_download_name,
            mime="image/png"
        )