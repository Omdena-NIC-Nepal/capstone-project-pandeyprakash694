# app/pages/extreme_events.py
import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
import streamlit as st

def show_page():
    st.title("Extreme Events")
    st.write("This is the Extreme Events page.")


@st.cache_data
def load_data():
    # Load extreme weather data
    df = pd.read_csv("data/processed_extreme_weather_events.csv")
    
    # Load Nepal districts GeoJSON
    nepal_gdf = gpd.read_file("data/nepal-districts.geojson")
    
    return df, nepal_gdf

def clean_data(df, nepal_gdf):
    """Handle missing values and duplicates"""
    # Drop exact duplicates
    df = df.drop_duplicates(subset=['disno'])
    
    # Remove rows with default coordinates
    df = df[~((df['latitude'] == 28.348895238095242) & 
              (df['longitude'] == 83.59854761904762))]
    
    # Convert date column
    df['start_date'] = pd.to_datetime(df['start_date'])
    df['year'] = df['start_date'].dt.year
    df['month'] = df['start_date'].dt.month
    
    return df

def prepare_features(df):
    """Feature engineering for ML model"""
    # Encode disaster types
    le = LabelEncoder()
    df['disaster_encoded'] = le.fit_transform(df['disaster_type'])
    
    features = ['latitude', 'longitude', 'year', 'month']
    target = 'disaster_encoded'
    
    return df[features], df[target], le

def train_model(X, y):
    """Train Random Forest classifier"""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    model = RandomForestClassifier(n_estimators=100, class_weight='balanced')
    model.fit(X_train, y_train)
    
    return model, X_test, y_test

def show_page():
    st.title("🇳🇵 Extreme Weather Events Analysis")
    
    # Load data
    df, nepal_gdf = load_data()
    
    # Data cleaning section
    st.header("🧹 Data Cleaning")
    with st.expander("Raw Data Summary"):
        st.write(f"Original records: {len(df)}")
        st.write("Missing values:", df.isnull().sum())
    
    df_clean = clean_data(df, nepal_gdf)
    
    with st.expander("Cleaned Data Summary"):
        st.write(f"Cleaned records: {len(df_clean)}")
        st.write("Common disaster types:", df_clean['disaster_type'].value_counts())
    
    # Visualization section
    st.header("🗺️ Event Visualization")
    
    # Disaster type selector
    disaster_types = st.multiselect(
        "Select Disaster Types to Visualize",
        options=df_clean['disaster_type'].unique(),
        default=['Flood', 'Earthquake', 'Mass movement (wet)']
    )
    
    # Filter data based on selection
    filtered_df = df_clean[df_clean['disaster_type'].isin(disaster_types)] if disaster_types else df_clean
    
    # Create interactive map with animation
    fig = px.scatter_mapbox(
        filtered_df,
        lat="latitude",
        lon="longitude",
        color="disaster_type",
        hover_name="disaster_type",
        hover_data=["start_date", "year"],
        animation_frame="year",
        zoom=5,
        height=600,
        title="Extreme Events Timeline",
        labels={"disaster_type": "Event Type"}
    )
    
    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_center={"lat": 28.3949, "lon": 84.1240},
        margin={"r":0,"t":40,"l":0,"b":0}
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Temporal distribution chart
    st.subheader("📅 Temporal Distribution")
    year_counts = filtered_df['year'].value_counts().reset_index()
    fig2 = px.bar(
        year_counts,
        x='year',
        y='count',
        color='year',
        title="Events per Year"
    )
    st.plotly_chart(fig2, use_container_width=True)
    
    # # ML Prediction Section
    # st.header("🤖 Disaster Type Prediction")
    
    # # Prepare features and target
    # X, y, le = prepare_features(df_clean)
    
    # # Train model
    # model, X_test, y_test = train_model(X, y)
    
    # # Prediction interface
    # col1, col2, col3 = st.columns(3)
    # with col1:
    #     lat = st.number_input("Latitude", value=27.7172)
    # with col2:
    #     lon = st.number_input("Longitude", value=85.3240)
    # with col3:
    #     year = st.number_input("Year", min_value=1980, max_value=2030, value=2024)
    
    # month = st.selectbox("Month", options=range(1,13), format_func=lambda x: pd.to_datetime(x, format='%m').strftime('%B'))
    
    # if st.button("Predict Disaster Risk"):
    #     input_data = pd.DataFrame([[lat, lon, year, month]], 
    #                             columns=['latitude', 'longitude', 'year', 'month'])
    #     prediction = model.predict(input_data)
    #     disaster_type = le.inverse_transform(prediction)
        
    #     st.success(f"Predicted High Risk for: {disaster_type[0]}")
    
    # # Model evaluation
    # st.subheader("Model Performance")
    # y_pred = model.predict(X_test)
    # report = classification_report(y_test, y_pred, target_names=le.classes_, output_dict=True)
    # report_df = pd.DataFrame(report).transpose()
    # st.dataframe(report_df.style.highlight_max(axis=0))

if __name__ == "__main__":
    show_page()
