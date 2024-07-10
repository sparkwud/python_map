import streamlit as st
import folium
import pandas as pd
import json
from folium.plugins import Fullscreen

# Load and prepare data
@st.cache_data
def load_data():
    india_covid_data = pd.read_csv("india/covid_cases_india.csv")
    with open("india/india.geojson") as f:
        geojson = json.load(f)
    return india_covid_data, geojson

india_covid_data, geojson = load_data()

# Streamlit UI
st.title("COVID-19 Cases in India")

# Sidebar for controls
st.sidebar.header("Map Controls")
choice = st.sidebar.selectbox("Select Data to Display", 
                              ['Confirmed Cases', 'Active Cases', 'Cured/Discharged', 'Death'])
zoom_level = st.sidebar.slider("Zoom Level", 3, 8, 5)

# Data preparation
india_covid_data[choice] = pd.to_numeric(india_covid_data[choice], errors='coerce')
india_covid_data = india_covid_data.dropna(subset=[choice, 'state_code'])

# Create map
m = folium.Map(location=[20.5937, 78.9629], zoom_start=zoom_level)

# Add GeoJSON layer
folium.GeoJson(
    geojson,
    name="India",
    style_function=lambda x: {
        'fillColor': 'lightblue',
        'color': 'black',
        'weight': 2,
        'fillOpacity': 0.1
    }
).add_to(m)

# Add Choropleth layer
choropleth = folium.Choropleth(
    geo_data=geojson,
    name="COVID-19 Data",
    data=india_covid_data,
    columns=["state_code", choice],
    key_on="feature.properties.state_code",
    fill_color="YlOrRd",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name=f"{choice}",
    highlight=True
).add_to(m)

# Add hover functionality
folium.LayerControl().add_to(m)
choropleth.geojson.add_child(
    folium.features.GeoJsonTooltip(['st_nm'], labels=False)
)

# Add fullscreen option
Fullscreen().add_to(m)

# Display the map in Streamlit
st_map = st.components.v1.html(m._repr_html_(), height=600)

# Save the map
m.save('india/india_covid_map.html')
st.success("Map saved as 'india_covid_map.html'")

# Display statistics
st.subheader("COVID-19 Statistics")
total_cases = india_covid_data[choice].sum()
st.metric(f"Total {choice}", f"{total_cases:,}")

# Display data table
st.subheader("State-wise Data")
st.dataframe(india_covid_data[['st_nm', choice]].sort_values(by=choice, ascending=False))