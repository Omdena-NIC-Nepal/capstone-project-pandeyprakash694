# app/pages/extreme_events.py

import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
import plotly.express as px
from datetime import datetime, timedelta
from shapely.geometry import Point
import random
import streamlit as st

def show_page():
    st.title("Extreme Events Atlas")
    st.write("This is the Extreme Events page.")
    #st.write("This is the Crop Yield Modeling page.")


# Custom disaster types with appropriate colors
DISASTER_TYPES = {
    'Flood': '#1E88E5',
    'Earthquake': '#D81B60',
    'Mass movement (wet)': '#8E24AA',
    'Mass movement (dry)': '#5E35B1',
    'Epidemic': '#43A047',
    'Drought': '#FFC107',
    'Wildfire': '#FF5722',
    'Extreme temperature': '#E91E63',
    'Glacial lake outburst flood': '#00ACC1'
}

# Nepal boundaries for data generation
NEPAL_BOUNDS = {
    'min_lat': 26.3478, 'max_lat': 30.4478,
    'min_lon': 80.0586, 'max_lon': 88.2010
}

def update_month_safely(date_obj, new_month):
    year = date_obj.year
    days_in_month = [31, 29 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 28,
                     31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    day = min(date_obj.day, days_in_month[new_month - 1])
    return date_obj.replace(month=new_month, day=day)

@st.cache_data
def generate_synthetic_data(num_events=2000):
    np.random.seed(42)  # For reproducibility
    start_date = datetime(2010, 1, 1)
    end_date = datetime(2024, 12, 31)
    date_range = (end_date - start_date).days

    data = []
    for i in range(num_events):
        random_days = np.random.randint(0, date_range)
        event_date = start_date + timedelta(days=random_days)

        # Strategic location distribution across Nepal's regions
        if i % 5 == 0:  # Western Nepal
            lat = np.random.uniform(26.8, 29.5)
            lon = np.random.uniform(80.1, 82.5)
        elif i % 5 == 1:  # Central Nepal
            lat = np.random.uniform(27.0, 28.5)
            lon = np.random.uniform(83.5, 85.5)
        elif i % 5 == 2:  # Eastern Nepal
            lat = np.random.uniform(26.5, 28.0)
            lon = np.random.uniform(86.0, 88.0)
        elif i % 5 == 3:  # Northern Nepal
            lat = np.random.uniform(28.5, 30.4)
            lon = np.random.uniform(81.0, 88.0)
        else:  # Southern Nepal
            lat = np.random.uniform(26.4, 27.5)
            lon = np.random.uniform(80.1, 88.0)

        # Realistic disaster distribution based on geography
        if lat > 29.0:  # High mountains
            disaster_weights = [0.1, 0.3, 0.2, 0.2, 0.0, 0.0, 0.1, 0.2, 0.1]
        elif lon < 82.0:  # Far-western
            disaster_weights = [0.3, 0.1, 0.2, 0.1, 0.1, 0.1, 0.1, 0.0, 0.0]
        elif lon > 86.0:  # Eastern
            disaster_weights = [0.3, 0.1, 0.1, 0.1, 0.2, 0.1, 0.1, 0.0, 0.0]
        elif lat < 27.0:  # Terai region
            disaster_weights = [0.4, 0.0, 0.0, 0.0, 0.3, 0.1, 0.1, 0.1, 0.0]
        else:  # Hills
            disaster_weights = [0.2, 0.2, 0.3, 0.1, 0.1, 0.0, 0.1, 0.0, 0.0]

        # Normalize weights to sum to 1
        weights_array = np.array(disaster_weights, dtype=np.float64)
        normalized_weights = weights_array / weights_array.sum()

        disaster_type = np.random.choice(list(DISASTER_TYPES.keys()), p=normalized_weights)

        # Apply seasonal patterns using the safe month update
        if disaster_type == 'Flood' and event_date.month not in [6, 7, 8, 9]:
            event_date = update_month_safely(event_date, random.choice([6, 7, 8, 9]))
        if disaster_type == 'Drought' and event_date.month not in [3, 4, 5]:
            event_date = update_month_safely(event_date, random.choice([3, 4, 5]))
        if disaster_type == 'Wildfire' and event_date.month not in [2, 3, 4]:
            event_date = update_month_safely(event_date, random.choice([2, 3, 4]))

        event_id = f"NDRM-{event_date.year}-{i:04d}"

        data.append({
            'disno': event_id,
            'disaster_type': disaster_type,
            'latitude': lat,
            'longitude': lon,
            'start_date': event_date.strftime('%Y-%m-%d'),
            'year': event_date.year,
            'month': event_date.month
        })

    return pd.DataFrame(data)

@st.cache_data
def load_and_enhance_data():
    events_df = generate_synthetic_data(2000)
    nepal_gdf = gpd.read_file("data/nepal-districts.geojson")
    district_col = 'DISTRICT'
    nepal_gdf = nepal_gdf[[district_col, 'geometry']].rename(columns={district_col: 'district'})
    events_gdf = gpd.GeoDataFrame(
        events_df,
        geometry=events_df.apply(lambda row: Point(row['longitude'], row['latitude']), axis=1),
        crs=nepal_gdf.crs
    )
    enhanced_gdf = gpd.sjoin(events_gdf, nepal_gdf, how='left', predicate='within')
    enhanced_gdf['start_date'] = pd.to_datetime(enhanced_gdf['start_date'])
    return enhanced_gdf, nepal_gdf

def create_interactive_dashboard(enhanced_gdf, nepal_gdf, year_range=None, disaster_types=None):
    filtered_df = enhanced_gdf.copy()
    if year_range:
        filtered_df = filtered_df[(filtered_df['year'] >= year_range[0]) & (filtered_df['year'] <= year_range[1])]
    if disaster_types:
        filtered_df = filtered_df[filtered_df['disaster_type'].isin(disaster_types)]
    district_stats = filtered_df.groupby('district').agg(
        total_events=('disno', 'count'),
        common_disaster=('disaster_type', lambda x: x.mode()[0] if not x.mode().empty else None),
        last_event=('start_date', 'max')
    ).reset_index()
    district_map = nepal_gdf.merge(district_stats, on='district', how='left')
    district_map['total_events'] = district_map['total_events'].fillna(0)
    fig = px.choropleth_mapbox(
        district_map,
        geojson=district_map.geometry.__geo_interface__,
        locations=district_map.index,
        color='total_events',
        hover_name='district',
        hover_data=['total_events', 'common_disaster'],
        color_continuous_scale='Reds',
        mapbox_style="carto-positron",
        center={"lat": 28.3949, "lon": 84.1240},
        zoom=5.8,
        opacity=0.7,
        labels={'total_events': 'Events'},
        height=650
    )
    marker_layer = px.scatter_mapbox(
        filtered_df,
        lat='latitude',
        lon='longitude',
        color='disaster_type',
        color_discrete_map=DISASTER_TYPES,
        hover_name='disaster_type',
        hover_data=['start_date', 'district'],
        size_max=10
    ).data[0]
    fig.add_trace(marker_layer)
    fig.update_layout(
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        legend_title_text="Disaster Type",
        mapbox=dict(
            center={"lat": 28.3949, "lon": 84.1240},
            zoom=5.8
        ),
        coloraxis_colorbar=dict(
            title="Event Count",
            thicknessmode="pixels",
            thickness=20,
            len=0.6
        )
    )
    return fig

def show_page():
    st.title("🌏 Nepal Extreme Events Atlas")
    enhanced_gdf, nepal_gdf = load_and_enhance_data()
    with st.sidebar:
        st.header("Filter Options")
        year_min = int(enhanced_gdf['year'].min())
        year_max = int(enhanced_gdf['year'].max())
        year_range = st.slider(
            "Select Year Range",
            min_value=year_min,
            max_value=year_max,
            value=(year_min, year_max)
        )
        disaster_types = st.multiselect(
            "Select Disaster Types",
            options=enhanced_gdf['disaster_type'].unique(),
            default=list(enhanced_gdf['disaster_type'].unique())[:5]
        )
        st.header("Display Options")
        show_markers = st.checkbox("Show Event Markers", value=True)
        show_choropleth = st.checkbox("Show District Heatmap", value=True)
    st.header("Spatial-Temporal Event Analysis")
    fig = create_interactive_dashboard(enhanced_gdf, nepal_gdf, year_range, disaster_types)
    st.plotly_chart(fig, use_container_width=True)
    filtered_df = enhanced_gdf[
        (enhanced_gdf['year'] >= year_range[0]) & (enhanced_gdf['year'] <= year_range[1])
    ]
    if disaster_types:
        filtered_df = filtered_df[filtered_df['disaster_type'].isin(disaster_types)]
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Events", f"{len(filtered_df):,}")
    with col2:
        top_disaster = filtered_df['disaster_type'].value_counts().idxmax() if not filtered_df.empty else "N/A"
        st.metric("Most Common Disaster", top_disaster)
    with col3:
        affected_districts = filtered_df['district'].nunique()
        st.metric("Affected Districts", f"{affected_districts} of {nepal_gdf.shape[0]}")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Annual Trend")
        yearly_counts = filtered_df.groupby(['year', 'disaster_type']).size().reset_index(name='count')
        fig_yearly = px.line(
            yearly_counts,
            x='year',
            y='count',
            color='disaster_type',
            color_discrete_map=DISASTER_TYPES,
            markers=True,
            title="Events by Year"
        )
        st.plotly_chart(fig_yearly, use_container_width=True)
    with col2:
        st.subheader("Seasonal Distribution")
        filtered_df['month_name'] = pd.to_datetime(filtered_df['start_date']).dt.strftime('%b')
        monthly_counts = filtered_df.groupby(['month', 'disaster_type']).size().reset_index(name='count')
        monthly_counts['month_name'] = pd.to_datetime(monthly_counts['month'], format='%m').dt.strftime('%b')
        fig_monthly = px.bar(
            monthly_counts,
            x='month_name',
            y='count',
            color='disaster_type',
            color_discrete_map=DISASTER_TYPES,
            title="Events by Month",
            category_orders={"month_name": ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                                            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']}
        )
        st.plotly_chart(fig_monthly, use_container_width=True)
    st.subheader("Most Affected Districts")
    district_counts = filtered_df['district'].value_counts().reset_index()
    district_counts.columns = ['district', 'count']
    district_counts = district_counts.sort_values('count', ascending=False).head(10)
    fig_district = px.bar(
        district_counts,
        x='district',
        y='count',
        color='count',
        color_continuous_scale='Reds',
        title="Top 10 Districts by Event Count"
    )
    fig_district.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_district, use_container_width=True)

if __name__ == "__main__":
    show_page()
