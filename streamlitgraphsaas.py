import streamlit as st 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
import io

st.set_page_config(
    page_title="Simplest Graph Creator",
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
        st.error(f"Error loading file: please select correct format")
else:
    st.info("Please upload a file to proceed.")

if dataframe is not None:
    st.dataframe(dataframe.head(5))
    x_options = ['None'] + list(dataframe.columns)
    x = st.selectbox("x axis", x_options)
    y_options = ['None'] + list(dataframe.columns)
    y = st.selectbox("y axis", y_options)
    plot_type = st.selectbox("plot type", ['line plot', 'scatter plot', 'box plot'])
    st.dataframe(dataframe.head(5))
    st.text(plot_type)
    x_axis_label = st.text_input('X label')
    y_axis_label = st.text_input('Y label')

if (dataframe is not None) and x:
    #st.line_chart(dataframe, x = x, y = y)
    fig, ax = plt.subplots()
    if plot_type == "line plot":
        try:
            sns.lineplot(data=dataframe, x= None if x == 'None' else x, y= None if y == 'None' else y, ax=ax)
        except Exception as e:
            st.error(f"Error loading file: line plot needs both x and y not just one")
    elif plot_type == "scatter plot":
        sns.scatterplot(data=dataframe, x= None if x == 'None' else x, y= None if y == 'None' else y, ax=ax)
    elif plot_type == 'box plot':
        sns.boxplot(data=dataframe, x= None if x == 'None' else x, y= None if y == 'None' else y, ax=ax)

    plt.xlabel(x_axis_label)
    plt.ylabel(y_axis_label)
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