# app/visualization.py
import plotly.express as px
import altair as alt
import pandas as pd

def yield_trend_line(df, district=None, prediction_data=None):
    """Line chart of yield over years with prediction highlights"""
    if district:
        data = df[df['DISTRICT_NAME'] == district]
        title = f"Yield Trend for {district}"
    else:
        data = df
        title = "Yield Trend (All Districts)"
        
    fig = px.line(data, x='year', y='VG_Y', markers=True,
                 title=title, 
                 labels={"VG_Y": "Yield (tons/ha)", "year": "Year"})
    
    if prediction_data is not None:
        fig.add_scatter(
            x=prediction_data['year'],
            y=prediction_data['VG_Y'],
            mode='markers',
            marker=dict(color='red', size=12),
            name='Prediction'
        )
    
    return fig

def yield_comparison_bar(df, year):
    """Bar chart comparing yield across districts for a given year."""
    data = df[df['year'] == year]
    fig = px.bar(data, x='DISTRICT_NAME', y='VG_Y', color='VG_Y', 
                 title=f"District-wise Yield Comparison ({year})",
                 labels={"VG_Y": "Yield (tons/ha)", "DISTRICT_NAME": "District"})
    fig.update_layout(xaxis_tickangle=-45)
    return fig

def feature_importance_chart(importances, feature_names):
    """Bar chart for feature importances (for tree models)."""
    imp_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances})
    imp_df = imp_df.sort_values('Importance', ascending=False)
    fig = px.bar(imp_df, x='Feature', y='Importance', title='Feature Importances')
    return fig

def prediction_vs_actual(y_true, y_pred):
    """Scatter plot of predicted vs actual yields."""
    df = pd.DataFrame({'Actual': y_true, 'Predicted': y_pred})
    fig = px.scatter(df, x='Actual', y='Predicted', trendline='ols',
                     title='Predicted vs Actual Yield')
    return fig
