import os  # Import the os module to interact with the file system
import streamlit as st
import pandas as pd
import plotly.graph_objs as go

st.title("Cryptocurrency Volatility Stabilizer")

# Specify the directory containing processed data
data_dir = r'C:\Users\Naushik\Downloads\csc582-asg1-master\Cryptocurrency-Volatility-Stabilizer\data\processed'

# List all CSV files in the directory
symbol_files = [file for file in os.listdir(data_dir) if file.endswith('.csv')]
selected_file = st.selectbox("Select a Cryptocurrency", symbol_files)

# Display the selected file's data
if selected_file:
    data = pd.read_csv(os.path.join(data_dir, selected_file), index_col=0, parse_dates=True)
    st.write(f"### Historical Prices for {selected_file.split('_')[0]}")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close'))
    fig.add_trace(go.Scatter(x=data.index, y=data['ma_10'], mode='lines', name='10-day MA'))
    fig.add_trace(go.Scatter(x=data.index, y=data['ma_50'], mode='lines', name='50-day MA'))
    st.plotly_chart(fig)

    st.write(f"### Technical Indicators")
    st.line_chart(data[['rsi', 'volatility']])
   
