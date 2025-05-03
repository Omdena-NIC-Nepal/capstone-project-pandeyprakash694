import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.model_selection import train_test_split
from visualization import yield_trend_line, prediction_vs_actual
import plotly.express as px
import streamlit as st

def show_page():
    st.title("Crop Yield Modeling")
    st.write("This is the Crop Yield Modeling page.")


@st.cache_data
def load_data():
    df = pd.read_csv("data/processed_agriculture_data.csv")
    melted = df.melt(id_vars=['DISTRICT_NAME'], var_name='metric_year', value_name='value')
    melted[['metric', 'year']] = melted['metric_year'].str.rsplit('_', n=1, expand=True)
    melted['year'] = melted['year'].str[:4]
    melted['year'] = pd.to_numeric(melted['year'], errors='coerce').astype('Int64')
    return melted.pivot_table(index=['DISTRICT_NAME', 'year'], columns='metric', values='value').reset_index()

def train_models(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
        "XGBoost": XGBRegressor(random_state=42)
    }

    results = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        rmse = mean_squared_error(y_test, preds) ** 0.5
        r2 = r2_score(y_test, preds)
        results[name] = {"model": model, "rmse": rmse, "r2": r2}
    return results, X_test, y_test

def show_page():
    st.title("🌾 Crop Yield Prediction")
    st.header("Here we will Predict and Compare Crop Yields Across Districts")

    # Load and preprocess data
    df = load_data()
    features = df[['DISTRICT_NAME', 'year', 'VG_A']].dropna()
    target = df.loc[features.index, 'VG_Y']

    X_encoded = pd.get_dummies(features)
    training_columns = X_encoded.columns.tolist()
    model_results, X_test, y_test = train_models(X_encoded, target)

    # Section 1: Yield trend comparison
    st.subheader("📊 Yield Comparison Over Time")
    selected_districts = st.multiselect(
        "Select Districts for Comparison",
        options=df['DISTRICT_NAME'].unique().tolist(),
        default=["Kathmandu", "Kaski"]
    )

    if selected_districts:
        comparison_df = df[df['DISTRICT_NAME'].isin(selected_districts)]
        fig = px.line(comparison_df, x='year', y='VG_Y', color='DISTRICT_NAME', markers=True,
                      labels={'VG_Y': 'Yield (tons/ha)', 'year': 'Year'},
                      title='District-wise Yield Trends')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Please select at least one district to compare.")

    # Section 2: Yield prediction input
    st.subheader("📌 Predict Future Crop Yield")
    col1, col2 = st.columns(2)
    with col1:
        district = st.selectbox("Select District", df['DISTRICT_NAME'].unique())
    with col2:
        year = st.number_input("Year", min_value=2023, max_value=2035, value=2024)

    area = st.number_input("Cultivation Area (hectares)", min_value=0.1, value=10.0)
    model_choice = st.radio("Choose Prediction Model", list(model_results.keys()))

    if st.button("Predict Yield"):
        input_data = pd.DataFrame([{
            'DISTRICT_NAME': district,
            'year': year,
            'VG_A': area
        }])
        input_encoded = pd.get_dummies(input_data)
        input_encoded = input_encoded.reindex(columns=training_columns, fill_value=0)

        model = model_results[model_choice]['model']
        prediction = model.predict(input_encoded)[0]

        st.success(f"🌱 Predicted Yield: {prediction:.2f} tons/hectare")
        st.write("### 🧾 Prediction Summary")
        st.write(f"**District:** {district}")
        st.write(f"**Year:** {year}")
        st.write(f"**Cultivation Area:** {area} ha")
        st.write(f"**Model Used:** {model_choice}")
        st.write(f"**Model R²:** {model_results[model_choice]['r2']:.2f}")
        st.write(f"**Model RMSE:** {model_results[model_choice]['rmse']:.2f}")
        st.balloons()

        # Yield trend for selected district
        st.subheader("📈 Yield Trend for Selected District")
        st.plotly_chart(yield_trend_line(df, district=district), use_container_width=True)

    # Section 3: Model evaluation (optional)
    st.subheader("📉 Evaluate Model Performance")
    if st.checkbox("Show Prediction vs Actual on Test Set"):
        y_pred = model_results[model_choice]['model'].predict(X_test)
        st.plotly_chart(prediction_vs_actual(y_test, y_pred), use_container_width=True)

if __name__ == "__main__":
    show_page()
