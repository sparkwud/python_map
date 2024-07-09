import streamlit as st
import folium
import pandas as pd
mapobj=folium.Map(location=[
     -0.3515602939922709,
     0.703125
],zoom_start=5)
geojson = f"subregion_Western_Africa_subunits.geojson"
bordersStyle={
    'color':'black',
    'weight':2,
    'fillColor':'blue',
    'fillOpacity': 0.1
}

# define variables
geojson = f"subregion_Western_Africa_subunits.geojson"
folium.GeoJson("subregion_Western_Africa_subunits.geojson",name="West_Africa",
            style_function=lambda x:bordersStyle).add_to(mapobj)
westy = f"ooooo.csv"
westy_data = pd.read_csv(westy)
choice = ['sovereignt','Voice','SMS','Data.per MB']
choice_selected = st.selectbox("Select Choice ", choice)

folium.Choropleth(
    geo_data=geojson,
    name="choropleth",
    data=westy_data,
    columns=["sov_a3", choice_selected],
    key_on="feature.properties.sovereignt",
    fill_color="Blues",
    fill_opacity=0.7,
    line_opacity=.1,
    legend_name=choice_selected+"(%)",
).add_to(mapobj)




   # display the code in html 
mapobj.save('West_Africa.html')
#add points
#folium.Circle(radius=5000,location=[9.0244164,7.3674663],
             #   color='red',
            #  weight=5,
            # fill=True,
             #fill_color='blue',
             #fill_opacity=0.7,
             #stroke=True
            # tooltip="this is a circle ",
            # popup=folium.Popup("This is a <b>popup</b>",max_width=500)
             
            # ).add_to(mapobj)





# choropleth map
