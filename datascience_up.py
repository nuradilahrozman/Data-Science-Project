import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io


st.set_page_config(page_title='Analyze Your Data', page_icon="📊",layout='wide')
st.title('📊 Analyze Your Data')
st.write('📁 Upload A ***CSV*** or an ***Excel*** File To Explore Your Data Interactively!')

uploaded_file = st.file_uploader(
    "Choose a CSV or Excel file",
    type=["csv", "xls", "xlsx"]
)

if uploaded_file is not None:
    try:
        # Get file extension
        file_extension = uploaded_file.name.split(".")[-1].lower()

        # Read file based on extension
        if file_extension == "csv":
            data = pd.read_csv(uploaded_file)
        elif file_extension in ["xls", "xlsx"]:
            data = pd.read_excel(uploaded_file)
        else:
            st.error("❌ Unsupported file format")
            data = None

        if data is not None:
            st.success("✨ File loaded successfully!")
            st.dataframe(data)

# converting bool columns as str
        non_numeric_cols = data.select_dtypes(include=['bool', 'object']).columns

        st.write('### Statistical Summary For Non-Numerical Features Of Dataset')

        if len(non_numeric_cols) > 0:
            st.dataframe(data[non_numeric_cols].describe())
        else:
            st.info("No non-numerical (categorical or boolean) features found in this dataset.")


    except Exception as e:
        st.error(f"Error reading file: {e}")

    st.write('### Data Overview')
    st.write('Number Of Rows ',data.shape[0])
    st.write('Number Of Columns ',data.shape[1])
    st.write('Number Of Missing Values ',data.isnull().sum().sum())
    st.write('Number Of Duplicates Records ',data.duplicated().sum())

    st.write("###Complete Summary Of Dataset")
    buffer = io.StringIO()
    data.info(buf=buffer)
    i = buffer.getvalue()
    st.text(i)

    
    st.write('### Statistical Summary For Non-Numerical Features Of Dataset')
    st.dataframe(data.describe(include=['bool','object']))

    st.write( '### Select The Desired Columns For Analysis')
    selected_columns = st.multiselect('Choose Columns', data.columns.tolist())

    if selected_columns:
        st.dataframe(data[selected_columns].head())
    else:
        st.info('No Columns Selected. Showing Full Dataset')
        st.dataframe(data.head())
    
    st.write(' ### Data Visualization')
    st.write('Select **Columns** For Data Visualization')
    columns = data.columns.tolist()
    x_axis = st.selectbox('Select Column For X-Axis',options = columns)
    y_axis = st.selectbox('Select Column For Y-Axis',options = columns)

    # Create Buttons For Diff Diff Charts
    col1 , col2 , col3 = st.columns(3)

    with col1:
        line_btn = st.button('Click Here To Generate The Line Graph')
    with col2:
        scatter_btn = st.button('Click Here To Generate The Scatter Graph')
    with col3:
        bar_btn = st.button('Click Here To Generate The Bar Graph')

    if line_btn:
        st.write('### Showing A Line Graph')
        fig,ax = plt.subplots()
        ax.plot(data[x_axis],data[y_axis])
        ax.set_xlabel(x_axis)
        ax.set_ylabel(y_axis)
        ax.set_title(f'Line Graph Of {x_axis} Vs {y_axis}')
        st.pyplot(fig) # show the graph

    if scatter_btn:
        st.write('### Showing A Scatter Graph')
        fig,ax = plt.subplots()
        ax.scatter(data[x_axis],data[y_axis])
        ax.set_xlabel(x_axis)
        ax.set_ylabel(y_axis)
        ax.set_title(f'Scatter Graph Of {x_axis} Vs {y_axis}')
        st.pyplot(fig) # show the graph

    if bar_btn:
        st.write('### Showing A Bar Graph')
        fig,ax = plt.subplots()
        ax.bar(data[x_axis],data[y_axis])
        ax.set_xlabel(x_axis)
        ax.set_ylabel(y_axis)
        ax.set_title(f'Bar Graph Of {x_axis} Vs {y_axis}')
        st.pyplot(fig) # show the graph

else:
    st.info('Please Upload A CSV or Excel File To Get Started')