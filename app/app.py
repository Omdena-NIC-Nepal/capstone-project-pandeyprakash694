import streamlit as st
from datetime import date

# Set page configuration
st.set_page_config(
    page_title="Climate-Aware Agricultural Dashboard",
    layout="wide",
    page_icon="🌾",
    initial_sidebar_state="expanded"
)

# Sidebar for navigation and branding
with st.sidebar:
    st.title("🌱 Agri-Dashboard")
    st.image(
        "https://images.unsplash.com/photo-1506744038136-46273834b3fb?fit=crop&w=400&q=80",
        caption="Nepalese Agriculture",
        use_container_width=True
    )
    st.markdown("---")
    st.caption(f"📅 {date.today().strftime('%B %d, %Y')}")
    
    # Navigation menu in the sidebar
    page = st.selectbox(
        "Navigate to:",
        ["Home", "Climate Trends", "Extreme Events", "Crop Yield Modeling", "Map View"],
        index=0
    )

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
    </style>
""", unsafe_allow_html=True)

# Main content
if page == "Home":
    st.title("🌾 Climate-Aware Agricultural Dashboard")
    st.markdown("""
        ### Project Information
        Welcome to the **Climate-Aware Agricultural Dashboard**, a tool designed to provide data-driven insights for sustainable farming practices. This project aims to support farmers and agricultural stakeholders by offering actionable information on climate patterns and crop productivity.

        #### Key Features:
        - **Climate Trends**: Monitor historical and projected temperature and rainfall patterns to understand long-term changes. 📈
        - **Extreme Events**: Analyze the frequency and impact of droughts, floods, and heatwaves on agriculture. 🌪
        - **Crop Yield Modeling**: Use machine learning models to predict crop yields based on environmental factors. 🌱
        - **Synthetic Data**: Visualize district-level extreme events in synthetic data. 🗺

        #### Objective:
        The goal of this dashboard is to empower farmers with the knowledge to adapt to changing climate conditions, optimize crop production, and mitigate risks from extreme weather events.

        #### Get Started:
        Use the sidebar to navigate to different sections and explore the insights available!
    """)
elif page == "Climate Trends":
    try:
        import pages.climate_trends as climate_trends
        climate_trends.show_page()
    except ImportError:
        st.error("Error: Could not load Climate Trends page. Ensure 'pages/climate_trends.py' exists and contains a 'show_page()' function.")
    except AttributeError:
        st.error("Error: 'climate_trends.py' does not have a 'show_page()' function.")
elif page == "Extreme Events":
    try:
        import pages.extreme_events as extreme_events
        extreme_events.show_page()
    except ImportError:
        st.error("Error: Could not load Extreme Events page. Ensure 'pages/extreme_events.py' exists and contains a 'show_page()' function.")
    except AttributeError:
        st.error("Error: 'extreme_events.py' does not have a 'show_page()' function.")
elif page == "Crop Yield Modeling":
    try:
        import pages.crop_yields as crop_yields
        crop_yields.show_page()
    except ImportError:
        st.error("Error: Could not load Crop Yield Modeling page. Ensure 'pages/crop_yields.py' exists and contains a 'show_page()' function.")
    except AttributeError:
        st.error("Error: 'crop_yields.py' does not have a 'show_page()' function.")
elif page == "Map View":
    try:
        import pages.map_view as map_view
        map_view.show_page()
    except ImportError:
        st.error("Error: Could not load Map View page. Ensure 'pages/map_view.py' exists and contains a 'show_page()' function.")
    except AttributeError:
        st.error("Error: 'map_view.py' does not have a 'show_page()' function.")