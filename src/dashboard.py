import streamlit as st
import pandas as pd
import plotly.graph_objs as go

st.title("Cryptocurrency Volatility Stabilizer")

data = pd.read_csv('data/processed/btc_data_processed.csv', index_col=0, parse_dates=True)

st.write("### Historical Prices")
fig = go.Figure()
fig.add_trace(go.Scatter(x=data.index, y=data['close'], mode='lines', name='Close'))
st.plotly_chart(fig)

st.write("### Optimized Portfolio Weights")
weights = [0.3, 0.5, 0.2]  # Example weights
st.bar_chart(weights)
