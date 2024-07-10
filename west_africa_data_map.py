import streamlit as st
import folium
import pandas as pd
import json

# Load and prepare data
@st.cache_data
def load_data():
    data = pd.read_csv("west_africa_data_usage.csv")
    with open("west_africa_map.geojson") as f:
        geojson = json.load(f)
    return data, geojson

data, geojson = load_data()

# Streamlit UI
st.title("West Africa Data Visualization")

# Sidebar for controls
st.sidebar.header("Map Controls")
choice = st.sidebar.selectbox("Select Data to Display", ['Voice', 'Data/MB'])
zoom_level = st.sidebar.slider("Zoom Level", 3, 8, 5)

# Data preparation
data[choice] = pd.to_numeric(data[choice], errors='coerce')
data = data.dropna(subset=[choice, 'country_code'])

# Create map
m = folium.Map(location=[-0.3515602939922709, 0.703125], zoom_start=zoom_level)

# Add GeoJSON layer
folium.GeoJson(
    geojson,
    name="West_Africa",
    style_function=lambda x: {
        'fillColor': 'blue',
        'color': 'black',
        'weight': 2,
        'fillOpacity': 0.1
    }
).add_to(m)

# Add Choropleth layer
choropleth = folium.Choropleth(
    geo_data=geojson,
    name="choropleth",
    data=data,
    columns=["country_code", choice],
    key_on="feature.properties.country_code",
    fill_color="YlOrRd",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name=f"{choice} (%)",
).add_to(m)

# Add hover functionality
folium.LayerControl().add_to(m)
choropleth.geojson.add_child(
    folium.features.GeoJsonTooltip(['name'], labels=False)
)

# Display the map in Streamlit
st.components.v1.html(m._repr_html_(), height=600)

# Save the map
m.save('data_usage_map.html')
# st.success("Map saved as 'data_usage_map.html'")


# Display data table
st.subheader("State-wise Data")
st.dataframe(data[['country', choice]].sort_values(by=choice, ascending=False))