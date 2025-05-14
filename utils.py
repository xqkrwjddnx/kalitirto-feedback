import pandas as pd
import streamlit as st
import pytz
import plotly.express as px

def process_feedback_history(data):
    df = pd.DataFrame(data)

    jakarta_tz = pytz.timezone('Asia/Jakarta')
    df['date'] = pd.to_datetime(df['created_at']).dt.tz_convert(jakarta_tz).dt.strftime('%Y-%m-%d %H:%M:%S')

    df.drop(columns=['created_at'], inplace=True)
    df.insert(0, 'no', range(1, len(df) + 1))
    return df

def set_markdown():
    return st.markdown("""
    <style>
        .stMetricValue-positif {
            background-color: green;
            color: white;
            border-radius: 10px;
            padding: 5px;
            text-align: center;
            font-size: 20px;
        }
        .stMetricValue-negatif {
            background-color: red;
            color: white;
            border-radius: 10px;
            padding: 5px;
            text-align: center;
            font-size: 20px;
        }
        .stMetricValue-netral {
            background-color: yellow;
            color: white;
            border-radius: 10px;
            padding: 5px;
            text-align: center;
            font-size: 20px;
        }
        .stMetricLabel {
            font-size: 16px;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)

def create_chart(positive, neutral, negative):
    labels = ['Positif', 'Netral', 'Negatif']
    values = [positive, neutral, negative]

    fig = px.pie(
        names=labels,
        values=values,
        color=['Positif', 'Netral', 'Negatif'],
        color_discrete_map={
            'Positif': 'green',
            'Netral': 'yellow',
            'Negatif': 'red'
        }
    )

    fig.update_traces(
        textinfo='label+percent',
        insidetextorientation='auto',
        hoverinfo='skip', hovertemplate=None
    )
    st.plotly_chart(fig, use_container_width=True)
