# Geo-Spatial Delivery Route Optimizer (Advanced Version)

import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
import osmnx as ox
import networkx as nx
import geopandas as gpd
from shapely.geometry import Point
from geopy.distance import geodesic
from streamlit_folium import folium_static
from sklearn.linear_model import LinearRegression
import numpy as np
import datetime
import plotly.express as px
import base64
import io

# Page setup
st.set_page_config(layout="wide")
st.title("🚀 Advanced Geo-Spatial Delivery Route Optimizer")

# Sample delivery data
st.sidebar.header("📍 Upload Delivery Data")
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    data = pd.read_csv(uploaded_file)
else:
    data = pd.DataFrame({
        'Delivery Point': ['Warehouse', 'Location A', 'Location B', 'Location C', 'Location D'],
        'Latitude': [28.6139, 28.6296, 28.6353, 28.6202, 28.6400],
        'Longitude': [77.2090, 77.2182, 77.2026, 77.2304, 77.1985],
        'Traffic Level': [2, 3, 4, 2, 5],  # 1-5 scale (simulated)
        'Time of Day': [9, 10, 11, 12, 13]  # 24-hr format (simulated)
    })

# Display map and data
st.subheader("🗺 Delivery Locations")
st.dataframe(data)

# Build GeoDataFrame
gdf = gpd.GeoDataFrame(
    data,
    geometry=gpd.points_from_xy(data.Longitude, data.Latitude),
    crs='EPSG:4326'
)

origin = (gdf.iloc[0]['Latitude'], gdf.iloc[0]['Longitude'])
graph = ox.graph_from_point(origin, dist=3000, network_type='drive')

# Get nearest nodes
def get_nearest_node(lat, lon):
    return ox.nearest_nodes(graph, lon, lat)

# Distance Matrix
def compute_distance_matrix(coords):
    n = len(coords)
    dist_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                dist_matrix[i, j] = geodesic(coords[i], coords[j]).meters
    return dist_matrix

# TSP (Nearest Neighbour)
def tsp_nearest_neighbor(coords):
    n = len(coords)
    visited = [False]*n
    path = [0]
    visited[0] = True
    for _ in range(n - 1):
        last = path[-1]
        next_city = np.argmin([
            geodesic(coords[last], coords[j]).meters if not visited[j] else float('inf')
            for j in range(n)
        ])
        path.append(next_city)
        visited[next_city] = True
    return path

coords = list(zip(gdf['Latitude'], gdf['Longitude']))
opt_order = tsp_nearest_neighbor(coords)
route_nodes = [get_nearest_node(*coords[i]) for i in opt_order]

# Draw map
m = folium.Map(location=origin, zoom_start=13)
marker_cluster = MarkerCluster().add_to(m)

for i in opt_order:
    row = gdf.iloc[i]
    folium.Marker(
        location=(row['Latitude'], row['Longitude']),
        popup=row['Delivery Point'],
        icon=folium.Icon(color='blue' if i == 0 else 'green')
    ).add_to(marker_cluster)

# Draw route
route_path = []
for i in range(len(route_nodes) - 1):
    path = nx.shortest_path(graph, route_nodes[i], route_nodes[i+1], weight='length')
    coords_path = [(graph.nodes[n]['y'], graph.nodes[n]['x']) for n in path]
    route_path.extend(coords_path)

folium.PolyLine(route_path, color='red', weight=5).add_to(m)
folium_static(m, height=600)

# Predict ETA using Linear Regression (sample ML integration)
X = gdf[['Traffic Level', 'Time of Day']].values
y = [10, 12, 20, 15, 25]  # simulated delivery time in mins
model = LinearRegression().fit(X, y)
predicted_eta = model.predict(gdf[['Traffic Level', 'Time of Day']])
total_eta = sum(predicted_eta)

# Fuel Estimate
total_distance_km = sum(
    geodesic(coords[opt_order[i]], coords[opt_order[i+1]]).km
    for i in range(len(opt_order)-1)
)
fuel_efficiency_kmpl = 15
fuel_used = total_distance_km / fuel_efficiency_kmpl

# Show Stats
st.subheader("📊 Route Summary")
st.markdown(f"*Total Distance:* {total_distance_km:.2f} km")
st.markdown(f"*Predicted ETA:* {total_eta:.1f} minutes")
st.markdown(f"*Estimated Fuel Usage:* {fuel_used:.2f} liters")

# Route Order Table
ordered_df = gdf.iloc[opt_order].reset_index(drop=True)
ordered_df['Visit Order'] = range(1, len(ordered_df)+1)
st.subheader("📋 Delivery Order")
st.dataframe(ordered_df[['Visit Order', 'Delivery Point', 'Latitude', 'Longitude']])

# Export CSV
csv = ordered_df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download Route CSV", csv, file_name='optimized_route.csv', mime='text/csv')

# Analytics
st.subheader("📈 Delivery Traffic Analysis")
fig = px.scatter(data, x='Time of Day', y='Traffic Level', size=[10]*len(data), color='Delivery Point')
st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("Developed by Mayank!")
