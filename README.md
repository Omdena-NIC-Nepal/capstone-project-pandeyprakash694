# 🌾 Climate-Aware Agricultural Dashboard

A Streamlit-based data science dashboard that combines climate, weather, and agricultural data to help analyze trends, predict yields, and assess the impact of extreme weather on food systems.

---

## 🚀 Features

- 📊 **Climate Trends**: Visualize temperature and precipitation across districts
- 🌪 **Extreme Weather Analysis**: Understand historical droughts, floods, heatwaves
- 🌾 **Crop Yield Modeling**: Predict yield using ML models (Linear, RF, XGBoost)
- 🗺 **Interactive Mapping**: Explore spatial insights using GeoPandas + Streamlit

---

## 🏗 Project Structure

climate_agri_dashboard/
├── data/ # datasets
├── notebooks/ # EDA notebooks
├── source/ # Backend logic (data loading, ML, geo utils)
├── app/ # Streamlit dashboard (main & pages)
├── .streamlit/ # Streamlit config
├── requirements.txt # Dependencies
└── README.md



---

## 🛠️ Setup Instructions

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app/main.py


🧠 ML Models Used

    Linear Regression

    Random Forest Regressor

    XGBoost Regressor

🌍 Spatial Analysis

    District-level GeoJSON overlays

    Climate/agriculture data joined using GeoPandas

📌 Future Enhancements

    Time-series forecasting (LSTM)

    Upload-your-own-dataset feature

    Real-time API integration (weather or satellite)