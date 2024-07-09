import streamlit as st
import folium
import pandas as pd
mapobj=folium.Map(location=[
     -0.3515602939922709,
     0.703125
],zoom_start=5)
json1 = f"states_india.geojson"
bordersStyle={
    'color':'black',
    'weight':2,
    'fillColor':'blue',
    'fillOpacity': 0.1
}

# define variables
geojson = f"states_india.geojson"
folium.GeoJson("states_india.geojson",name="Ghana ",
               style_function=lambda x:bordersStyle).add_to(mapobj)
india_covid = f"covid_cases_india.csv"
india_covid_data = pd.read_csv(india_covid)
choice = ['Confirmed Cases','Active Cases', 'Cured/Discharged', 'Death']
choice_selected = st.selectbox("Select Choice ", choice)

folium.Choropleth(
    geo_data=json1,
    name="choropleth",
    data=india_covid_data,
    columns=["state_code", choice_selected],
    key_on="feature.properties.state_code",
    fill_color="Blues",
    fill_opacity=0.7,
    line_opacity=.1,
    legend_name=choice_selected+"(%)",
).add_to(mapobj)

mapobj.save('Gina.html')