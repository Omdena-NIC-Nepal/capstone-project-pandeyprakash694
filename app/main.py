import streamlit as st
from datetime import date

# Set page configuration
st.set_page_config(
    page_title="Climate-Aware Agricultural Dashboard",
    layout="wide",
    page_icon="🌾",
    initial_sidebar_state="expanded"
)

# Navigation using tabs at the top
pages = ["Home", "Climate Trends", "Extreme Events", "Crop Yield Modeling", "Map View"]
tabs = st.tabs(pages)

# Sidebar (branding/info only)
with st.sidebar:
    st.title("🌱 Agri-Dashboard")
    st.image(
        "https://images.unsplash.com/photo-1506744038136-46273834b3fb?fit=crop&w=400&q=80",
        caption="Nepalese Agriculture",
        use_container_width=True
    )
    st.markdown("---")
    st.caption(f"📅 {date.today().strftime('%B %d, %Y')}")

# Custom CSS for styling
st.markdown("""
    <style>
    .main {background-color: #f5f5f5;}
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
    }
    .stSelectbox, .stRadio {background-color: #ffffff; border-radius: 8px; padding: 10px;}
    .sidebar .sidebar-content {background-color: #e8f5e9;}
    h1, h2, h3 {color: #2e7d32;}
    /* Style for tabs */
    .stTabs [role="tablist"] {
        background-color: #4CAF50;
        padding: 10px;
        border-radius: 8px;
    }
    .stTabs [role="tab"] {
        color: white;
        font-size: 18px;
        padding: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2e7d32;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Main content using tabs
with tabs[0]:
    st.title("🌾 Climate-Aware Agricultural Dashboard")
    st.markdown("""
        Welcome to your **Climate-Aware Agricultural Dashboard**! Explore data-driven insights for sustainable farming:
        - **Climate Trends**: Monitor temperature and rainfall patterns 📈
        - **Extreme Events**: Analyze droughts, floods, and heatwaves 🌪
        - **Crop Yield Modeling**: Predict yields with ML models 🌱
        - **Extreme Synthetic**: Visualize district-level data with synthetic data 🗺
    """)

with tabs[1]:
    try:
        import pages.climate_trends as climate_trends
        climate_trends.show_page()
    except ImportError:
        st.error("Error: Could not load Climate Trends page. Ensure 'pages/climate_trends.py' exists and contains a 'show_page()' function.")
    except AttributeError:
        st.error("Error: 'climate_trends.py' does not have a 'show_page()' function.")

with tabs[2]:
    try:
        import pages.extreme_events as extreme_events
        extreme_events.show_page()
    except ImportError:
        st.error("Error: Could not load Extreme Events page. Ensure 'pages/extreme_events.py' exists and contains a 'show_page()' function.")
    except AttributeError:
        st.error("Error: 'extreme_events.py' does not have a 'show_page()' function.")

with tabs[3]:
    try:
        import pages.crop_yields as crop_yields
        crop_yields.show_page()
    except ImportError:
        st.error("Error: Could not load Crop Yield Modeling page. Ensure 'pages/crop_yields.py' exists and contains a 'show_page()' function.")
    except AttributeError:
        st.error("Error: 'crop_yields.py' does not have a 'show_page()' function.")

with tabs[4]:
    try:
        import pages.map_view as map_view
        map_view.show_page()
    except ImportError:
        st.error("Error: Could not load Map View page. Ensure 'pages/map_view.py' exists and contains a 'show_page()' function.")
    except AttributeError:
        st.error("Error: 'map_view.py' does not have a 'show_page()' function.")