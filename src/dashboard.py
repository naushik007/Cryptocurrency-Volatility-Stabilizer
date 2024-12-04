import os
import streamlit as st
import pandas as pd
import plotly.graph_objs as go

# Set the base directory for processed data
data_dir = os.path.abspath('data/processed')

# Ensure the working directory is correctly set
os.chdir(os.path.dirname(__file__))

# Check if the processed directory exists
if not os.path.exists(data_dir):
    st.error(f"Directory {data_dir} does not exist. Please run the preprocessing step or create the directory.")
else:
    # Get list of processed files
    symbol_files = [file for file in os.listdir(data_dir) if file.endswith('.csv')]

    # Handle cases where no files are found
    if not symbol_files:
        st.warning(f"No processed data files found in {data_dir}. Please run the preprocessing script to generate files.")
    else:
        # Create a dropdown menu for selecting a file
        selected_file = st.selectbox("Select a Cryptocurrency", symbol_files)

        if selected_file:
            # Load the selected file
            data = pd.read_csv(os.path.join(data_dir, selected_file), index_col=0, parse_dates=True)
            
            # Display the title
            st.write(f"### Historical Prices for {selected_file.split('_')[0]}")

            # Create and display a line chart for prices
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close'))
            fig.add_trace(go.Scatter(x=data.index, y=data['ma_10'], mode='lines', name='10-day MA'))
            fig.add_trace(go.Scatter(x=data.index, y=data['ma_50'], mode='lines', name='50-day MA'))
            st.plotly_chart(fig)

            # Display technical indicators
            st.write(f"### Technical Indicators")
            st.line_chart(data[['rsi', 'volatility']])
