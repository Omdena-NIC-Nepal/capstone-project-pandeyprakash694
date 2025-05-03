import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import uuid
from datetime import datetime
import streamlit as st
import streamlit as st

def show_page():
    st.title("Climate Trends")
    st.write("This is the Climate Trends page.")



# Load and clean data
def load_and_clean_data(file_path):
    df = pd.read_csv(file_path)
    
    # Remove any rows with missing critical values
    df = df.dropna(subset=['date', 't2m', 'prectot', 'district', 'year', 'month'])
    
    # Convert data types
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['year'].astype(int)
    df['month'] = df['month'].astype(int)
    df['t2m'] = df['t2m'].astype(float)
    df['prectot'] = df['prectot'].astype(float)
    
    # Add season column
    def get_season(month):
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Monsoon'
        else:
            return 'Autumn'
    
    df['season'] = df['month'].apply(get_season)
    
    return df

# Create visualizations
def create_visualizations(df):
    # 1. Yearly Temperature Trend (unchanged)
    yearly_temp = df.groupby('year')['t2m'].mean().reset_index()
    fig1 = px.line(yearly_temp, x='year', y='t2m', 
                  title='Average Yearly Temperature Trend',
                  labels={'t2m': 'Temperature (°C)', 'year': 'Year'})

    # 2. Enhanced Seasonal Precipitation Comparison
    st.subheader("District Precipitation Comparison")
    
    # Create multiselect widget
    districts = df['district'].unique().tolist()
    selected_districts = st.multiselect(
        'Select Districts (max 10 for clear comparison):',
        options=districts,
        default=['Kathmandu', 'Kaski'],  # Example defaults
        max_selections=10
    )
    
    # Filter data for selected districts
    if len(selected_districts) > 0:
        district_data = df[df['district'].isin(selected_districts)]
        seasonal_precip = district_data.groupby(['district', 'season'])['prectot'].mean().reset_index()
        
        # Create comparison chart
        fig2 = px.bar(seasonal_precip, 
                     x='season', 
                     y='prectot', 
                     color='district',
                     barmode='group',
                     title=f'Seasonal Precipitation Comparison: {", ".join(selected_districts)}',
                     labels={'prectot': 'Precipitation (mm)', 'season': 'Season'},
                     category_orders={"season": ["Winter", "Spring", "Monsoon", "Autumn"]})
        
        fig2.update_layout(xaxis_tickangle=-45, 
                          hovermode='x unified',
                          legend_title='District')
    else:
        fig2 = px.bar()  # Empty figure if no selection

    # 3. Temperature vs Precipitation Scatter (unchanged)
    sampled_df = df.sample(frac=0.1, random_state=42)
    fig3 = px.scatter(sampled_df, x='t2m', y='prectot',
                     color='season', 
                     hover_data=['district', 'date'],
                     title='Temperature vs Precipitation')

    return fig1, fig2, fig3


# Find interesting fact
def find_interesting_fact(df):
    winter_data = df[df['season'] == 'Winter']
    high_precip_winter = winter_data.groupby('district')['prectot'].mean().sort_values(ascending=False).head(1)
    
    if not high_precip_winter.empty:
        district = high_precip_winter.index[0]
        precip_value = high_precip_winter.iloc[0]
        return f"{district} has an unusually high average precipitation of {precip_value:.2f} mm in Winter, a typically dry season!"
    return "No unusual precipitation trends found in Winter."

# Main function to generate report
def generate_climate_report(file_path, output_html='climate_trend_report.html'):
    # Load and clean data
    df = load_and_clean_data(file_path)
    
    # Create visualizations
    fig1, fig2, fig3 = create_visualizations(df)
    
    # Find interesting fact
    interesting_fact = find_interesting_fact(df)
    
    # Generate HTML report
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Climate Trends in Nepal</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    </head>
    <body class="bg-gray-100 font-sans">
        <div class="container mx-auto p-6">
            <h1 class="text-4xl font-bold text-center text-blue-800 mb-8">Climate Trends in Nepal (1981-2019)</h1>
            
            <!-- Summary -->
            <section class="bg-white p-6 rounded-lg shadow-md mb-8">
                <h2 class="text-2xl font-semibold text-gray-800 mb-4">Summary</h2>
                <p class="text-gray-600">
                    This report analyzes temperature and precipitation trends across various districts in Nepal from 1981 to 2019. 
                    The data reveals seasonal patterns, with Monsoon seasons showing significantly higher precipitation and temperatures peaking in Spring and Monsoon.
                </p>
            </section>
            
            <!-- Yearly Temperature Trend -->
            <section class="bg-white p-6 rounded-lg shadow-md mb-8">
                <h2 class="text-2xl font-semibold text-gray-800 mb-4">Yearly Temperature Trend</h2>
                <div id="temp-trend"></div>
                <p class="text-gray-600 mt-4">
                    The line chart shows the average annual temperature across all districts, indicating a gradual warming trend.
                </p>
            </section>
            
            <!-- Seasonal Precipitation -->
            <section class="bg-white p-6 rounded-lg shadow-md mb-8">
                <h2 class="text-2xl font-semibold text-gray-800 mb-4">Seasonal Precipitation by District</h2>
                <div id="precip-bar"></div>
                <p class="text-gray-600 mt-4">
                    The bar chart illustrates average precipitation by season across districts, highlighting the dominance of the Monsoon season.
                </p>
            </section>
            
            <!-- Temperature vs Precipitation -->
            <section class="bg-white p-6 rounded-lg shadow-md mb-8">
                <h2 class="text-2xl font-semibold text-gray-800 mb-4">Temperature vs Precipitation</h2>
                <div id="temp-precip-scatter"></div>
                <p class="text-gray-600 mt-4">
                    The scatter plot explores the relationship between temperature and precipitation, with distinct seasonal patterns.
                </p>
            </section>
            
            <!-- Interesting Fact -->
            <section class="bg-white p-6 rounded-lg shadow-md mb-8">
                <h2 class="text-2xl font-semibold text-gray-800 mb-4">Interesting Fact</h2>
                <p class="text-gray-600">{interesting_fact}</p>
            </section>
            
            <!-- Conclusion -->
            <section class="bg-white p-6 rounded-lg shadow-md">
                <h2 class="text-2xl font-semibold text-gray-800 mb-4">Conclusion</h2>
                <p class="text-gray-600">
                    The analysis highlights a warming trend in Nepal, with significant precipitation during the Monsoon season. 
                    These insights can inform agricultural planning and disaster preparedness.
                </p>
            </section>
        </div>
        
        <script>
            Plotly.newPlot('temp-trend', {fig1.to_json()}, {{responsive: true}});
            Plotly.newPlot('precip-bar', {fig2.to_json()}, {{responsive: true}});
            Plotly.newPlot('temp-precip-scatter', {fig3.to_json()}, {{responsive: true}});
        </script>
    </body>
    </html>
    """
    
    # Save HTML report
    with open(output_html, 'w') as f:
        f.write(html_content)
    
    return fig1, fig2, fig3, interesting_fact

# Example usage
if __name__ == "__main__":
    file_path = "data/processed_temp_precipitation.csv"
    fig1, fig2, fig3, fact = generate_climate_report(file_path)
    print("Report generated: climate_trend_report.html")
    print("Interesting Fact:", fact)


import streamlit as st

#file_path = "../../data/processed_temp_precipitation.csv"
#fig1, fig2, fig3, fact = generate_climate_report(file_path)

st.title("Climate Trends in Nepal (1981-2019)")

st.header("Summary")
st.write("""
This report analyzes temperature and precipitation trends across various districts in Nepal from 1981 to 2019.
The data reveals seasonal patterns, with Monsoon seasons showing significantly higher precipitation and temperatures peaking in Spring and Monsoon.
""")

st.header("Yearly Temperature Trend")
st.plotly_chart(fig1, use_container_width=True)

st.header("Seasonal Precipitation by District")
st.plotly_chart(fig2, use_container_width=True)

st.header("Temperature vs Precipitation")
st.plotly_chart(fig3, use_container_width=True)

st.header("Interesting Fact")
st.info(fact)

st.header("Conclusion")
st.write("""
The analysis highlights a warming trend in Nepal, with significant precipitation during the Monsoon season.
These insights can inform agricultural planning and disaster preparedness.
""")
