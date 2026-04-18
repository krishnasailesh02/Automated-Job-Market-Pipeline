import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from sqlalchemy import create_engine
import os

# Set page config to hide sidebar and use full width
st.set_page_config(page_title="Job Market Live", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS to mimic the "Epic BI" Premium Dashboard (Dark Teal, Glowing effects, Rounded Corners)
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #071620, #0a2f35);
        color: #e0f2f1;
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide top header and main menu for a clean app look */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    
    /* Custom KPI Cards */
    div[data-testid="metric-container"] {
        background-color: rgba(16, 55, 65, 0.7);
        border: 1px solid rgba(44, 116, 126, 0.5);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(4px);
    }
    
    div[data-testid="metric-container"] > div:nth-child(1) {
        color: #88c0d0; /* Label color */
        font-size: 1.1rem;
    }
    
    div[data-testid="metric-container"] > div:nth-child(2) {
        color: #64ffda; /* Value neon cyan text */
        font-weight: 700;
        font-size: 2.5rem;
    }
    
    /* Style headers */
    h1, h2, h3 {
        color: #ffffff;
        font-weight: 600;
        letter-spacing: 1px;
    }
    
    /* Adjust block container padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

st.title("✨ Live Job Market Intelligence")
st.markdown("<p style='color: #88c0d0; margin-bottom: 40px; font-size: 1.2rem;'>Automated Real-Time Pipeline Feed</p>", unsafe_allow_html=True)

@st.cache_data(ttl=30) # Refresh every 30 seconds for "Live" feel
def load_data():
    try:
        db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'job_market.db'))
        engine = create_engine(f'sqlite:///{db_path}')
        df = pd.read_sql('SELECT * FROM stg_jobs', engine)
        return df
    except Exception as e:
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.warning("Waiting for automated data pipeline to complete...")
else:
    # 1. Top KPIs (Like the Epic BI dashboard)
    total_jobs = len(df)
    avg_salary = df['avg_salary'].mean()
    max_salary = df['salary_max'].max()
    remote_jobs = df[df['remote_allowed'] == 'Yes'].shape[0]
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Total Active Jobs", f"{total_jobs:,}")
    with col2: st.metric("Market Avg Salary", f"${avg_salary/1000:,.0f}K")
    with col3: st.metric("Peak Salary Offer", f"${max_salary/1000:,.0f}K")
    with col4: st.metric("Remote Opportunities", f"{remote_jobs:,}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Common chart styling to make backgrounds transparent and fonts match the theme
    chart_layout = dict(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#88c0d0', family="Inter"),
        margin=dict(l=10, r=10, t=30, b=10)
    )
    
    row1_col1, row1_col2 = st.columns([1.5, 2])
    
    with row1_col1:
        st.markdown("### Experience Demographics")
        exp_df = df['experience_level'].value_counts().reset_index()
        exp_df.columns = ['experience_level', 'count']
        
        # Sleek Donut Chart
        fig_donut = go.Figure(data=[go.Pie(
            labels=exp_df['experience_level'], 
            values=exp_df['count'], 
            hole=.7,
            marker_colors=['#64ffda', '#1de9b6', '#00bfa5', '#00897b'],
            textinfo='label+percent',
            textposition='outside'
        )])
        fig_donut.update_layout(**chart_layout, showlegend=False)
        st.plotly_chart(fig_donut, use_container_width=True)

    with row1_col2:
        st.markdown("### Salary Trends by Industry")
        ind_df = df.groupby('industry')['avg_salary'].mean().reset_index()
        
        # Glowing Line Chart with filled area (Mimicking the Epic BI middle chart)
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=ind_df['industry'], 
            y=ind_df['avg_salary'],
            mode='lines+markers',
            line=dict(color='#64ffda', width=4, shape='spline'),
            marker=dict(size=12, color='#0a2f35', line=dict(color='#64ffda', width=3)),
            fill='tozeroy',
            fillcolor='rgba(100, 255, 218, 0.15)'
        ))
        fig_line.update_layout(
            **chart_layout,
            xaxis=dict(showgrid=False, color='#88c0d0', title=None),
            yaxis=dict(showgrid=True, gridcolor='rgba(44, 116, 126, 0.2)', color='#88c0d0', title=None, tickprefix="$")
        )
        st.plotly_chart(fig_line, use_container_width=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Bottom Row
    st.markdown("### Top Hiring Locations")
    city_df = df[df['city'] != 'Unknown']['city'].value_counts().head(5).reset_index()
    city_df.columns = ['city', 'count']
    
    # Sleek Horizontal Bar Chart
    fig_bar = go.Figure(go.Bar(
        x=city_df['count'],
        y=city_df['city'],
        orientation='h',
        marker_color='#64ffda',
        text=city_df['count'],
        textposition='auto',
        textfont=dict(color='#071620', weight='bold')
    ))
    fig_bar.update_layout(
        **chart_layout,
        height=250,
        xaxis=dict(showgrid=False, visible=False),
        yaxis=dict(showgrid=False, color='#ffffff', autorange="reversed", title=None)
    )
    st.plotly_chart(fig_bar, use_container_width=True)
