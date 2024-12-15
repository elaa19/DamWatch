import streamlit as st
import pandas as pd
import plotly.express as px

# Load the Excel data
def load_data():
    df = pd.read_excel('Data1.xlsx')
    df['Capacity ( millions m3 )'] = pd.to_numeric(df['Capacity ( millions m3 )'], errors='coerce')
    df['Year Built'] = pd.to_numeric(df['Year Built'], errors='coerce')
    return df

data = load_data()


# Dashboard title and layout
st.set_page_config(
    page_title="Tunisia Dams Dashboard", 
    layout="wide",
    page_icon='✅'
)

# Custom CSS for a professional look
def custom_css():
    st.markdown("""
        <style>
            body {
                background-color: #f4f6f9;
                color: #2c2c2c;
                font-family: Arial, sans-serif;
            }

            .header {
                font-size: 42px;
                font-weight: 600;
                text-align: center;
                color: #2c3e50;
                padding-bottom: 20px;
            }

            .box {
                background-color: #001f3f;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
                text-align: center;
                margin-bottom: 20px;
                color: white;
            }

            .chart-box {
                background-color: #f0f0f5;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
                margin-bottom: 20px;
                transition: transform 0.3s, box-shadow 0.3s;
            }

            .chart-box:hover {
                transform: scale(1.02);
                box-shadow: 0px 6px 16px rgba(0, 0, 0, 0.2);
            }

            .stSidebar .css-17eq0hr, .stSidebar label {
                color: black ;
                font-size: 18px ;
                font-weight: bold ;
            }

            /* Slider track and thumb */
            .stSlider .css-1wy6l3l {
                background-color: #007bff ;  
            }

            .stSlider .css-qrbaxs {
                background-color: #007bff t;  
            }

            .stSlider .css-1h9h7wh, .stSlider .css-1e5bymp {
                color: #000000 ;  
                font-size: 18px ;
                font-weight: bold ;
            }

            .stSlider .css-10trblm {
                color: #000000 ;  
            }

            /* Filter buttons and tags */
            .stMultiSelect span, .stSlider span {
                background-color: #000080 ;
                color: white ;
            }

            

            
        </style>
    """, unsafe_allow_html=True)



custom_css()

# Dashboard Header
st.markdown('<div class="header">Tunisia Dams Dashboard</div>', unsafe_allow_html=True)

# Sidebar: Filters
st.sidebar.title("Filters")
st.sidebar.markdown("""
    <style>
        .css-1d391kg {
            background-color: #001f3f ;
            color: white ;
        }
        .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3, .css-1d391kg h4 {
            color: white ;
        }
    </style>
""", unsafe_allow_html=True)

year_filter = st.sidebar.slider(
    "Select Year Range", 
    int(data['Year Built'].min()), 
    int(data['Year Built'].max()), 
    (int(data['Year Built'].min()), int(data['Year Built'].max()))
)

city_filter = st.sidebar.multiselect(
    "Select Cities", 
    options=data['City'].dropna().unique(), 
    default=data['City'].dropna().unique()
)

quality_filter = st.sidebar.multiselect(
    "Select Water Quality", 
    options=data['Water Quality'].dropna().unique(), 
    default=data['Water Quality'].dropna().unique()
)

# Apply filters
data_filtered = data[
    (data['Year Built'] >= year_filter[0]) & 
    (data['Year Built'] <= year_filter[1])
]
data_filtered = data_filtered[data_filtered['City'].isin(city_filter)]
data_filtered = data_filtered[data_filtered['Water Quality'].isin(quality_filter)]
data_filtered = data_filtered.dropna(subset=['Capacity ( millions m3 )', 'Year Built'])

# Main KPIs
# Main KPIs
st.markdown("## Key Metrics")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    total_dams = len(data_filtered)
    st.markdown(f'<div class="box"><h2 style="color:white;">Total Dams</h2><h1 style="color:white;">{total_dams}</h1></div>', unsafe_allow_html=True)

with kpi2:
    total_capacity = data_filtered['Capacity ( millions m3 )'].sum()
    st.markdown(f'<div class="box"><h2 style="color:white;">Total Capacity (Million m³)</h2><h1 style="color:white;">{total_capacity:,.2f}</h1></div>', unsafe_allow_html=True)

with kpi3:
    avg_capacity = data_filtered['Capacity ( millions m3 )'].mean()
    st.markdown(f'<div class="box"><h2 style="color:white;">Average Capacity (Million m³)</h2><h1 style="color:white;">{avg_capacity:,.2f}</h1></div>', unsafe_allow_html=True)

with kpi4:
    total_cities = data_filtered['City'].nunique()
    st.markdown(f'<div class="box"><h2 style="color:white;">Total Covered Cities</h2><h1 style="color:white;">{total_cities}</h1></div>', unsafe_allow_html=True)

# Chart Layout
st.markdown("## Visualizations")

chart1, chart2 = st.columns(2)

# Bar Chart
with chart1:
    st.markdown('<div class="chart-box"><h3>Total Capacity by Year</h3>', unsafe_allow_html=True)
    if not data_filtered.empty:
        grouped_data = data_filtered.groupby('Year Built', as_index=False)['Capacity ( millions m3 )'].sum()
        fig1 = px.bar(grouped_data, x='Year Built', y='Capacity ( millions m3 )', template='plotly_dark')
        st.plotly_chart(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Bubble Chart
with chart2:
    st.markdown('<div class="chart-box"><h3>Capacity vs. Year</h3>', unsafe_allow_html=True)
    if not data_filtered.empty:
        valid_bubble_data = data_filtered[data_filtered['Capacity ( millions m3 )'] > 0]
        fig2 = px.scatter(valid_bubble_data, x='Year Built', y='Capacity ( millions m3 )', size='Capacity ( millions m3 )', template='plotly_dark')
        st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

chart3, chart4 = st.columns(2)

# Funnel Chart
with chart3:
    st.markdown('<div class="chart-box"><h3>Cumulative Capacity</h3>', unsafe_allow_html=True)
    if not data_filtered.empty:
        funnel_data = data_filtered.groupby('Year Built', as_index=False)['Capacity ( millions m3 )'].sum()
        funnel_data['Cumulative Capacity'] = funnel_data['Capacity ( millions m3 )'].cumsum()
        fig3 = px.funnel(funnel_data, x='Cumulative Capacity', y='Year Built', template='plotly_dark')
        st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Line Chart
with chart4:
    st.markdown('<div class="chart-box"><h3>Capacity Trends</h3>', unsafe_allow_html=True)
    if not data_filtered.empty:
        line_data = data_filtered.groupby('Year Built', as_index=False)['Capacity ( millions m3 )'].mean()
        fig4 = px.line(line_data, x='Year Built', y='Capacity ( millions m3 )', template='plotly_dark')
        st.plotly_chart(fig4, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

chart5, chart6 = st.columns(2)

# Donut Chart
with chart5:
    st.markdown('<div class="chart-box"><h3>Capacity by City</h3>', unsafe_allow_html=True)
    if not data_filtered.empty:
        city_data = data_filtered.groupby('City', as_index=False)['Capacity ( millions m3 )'].sum()
        fig5 = px.pie(
            city_data, 
            values='Capacity ( millions m3 )', 
            names='City', 
            hole=0.4, 
            template='plotly_dark',
            color_discrete_sequence=['#ADD8E6', '#001F3F', '#D8BFD8']  # Light blue, navy blue, light purple
        )
        st.plotly_chart(fig5, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Scatter Plot
with chart6:
    st.markdown('<div class="chart-box"><h3>Year vs. Capacity</h3>', unsafe_allow_html=True)
    if not data_filtered.empty:
        fig6 = px.scatter(data_filtered, x='Year Built', y='Capacity ( millions m3 )', color='City', template='plotly_dark')
        st.plotly_chart(fig6, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
