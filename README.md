# Routegenie



# 🚀 Advanced Geo-Spatial Delivery Route Optimizer

This project is an interactive **geo-spatial route optimization tool** built using **Streamlit** and **Folium**, with intelligent routing based on delivery location data. It helps users visualize delivery points on a map and generates an **optimized delivery path** using a basic Traveling Salesman Problem (TSP) approach.

---

## 🧩 Features

- 📍 Upload or simulate delivery locations.
- 🌍 Visualize delivery points on an interactive Folium map.
- 🔄 Automatically compute an optimized delivery route (Nearest Neighbour heuristic).
- 🚦 Consider traffic levels and time of day.
- 📊 View data and routing order interactively.

---

## 🧰 Tech Stack

- **Frontend/UI**: Streamlit
- **Mapping & Geo-processing**: Folium, OSMnx, GeoPandas
- **Distance Calculations**: geopy
- **Data Handling**: Pandas, NumPy
- **Modeling/ML-ready**: Scikit-learn
- **Map Embedding**: streamlit-folium
- **Graph Routing**: NetworkX (via OSMnx)

---

## 📂 File Structure

```
├── app.py                # Main Streamlit app
├── sample_data.csv       # Example CSV file for testing
├── README.md             # This documentation file
```

---

## 📝 How It Works

### 1. 📤 Upload or Use Sample Data

The sidebar allows you to upload a CSV file with columns:

- `Delivery Point`: Name or label of the location
- `Latitude` & `Longitude`: Coordinates of each delivery location
- `Traffic Level`: (1-5 scale) Simulated traffic impact
- `Time of Day`: Time in 24-hour format

If no file is uploaded, sample data will be used.

---

### 2. 📌 Display Delivery Locations

- A Pandas DataFrame is displayed showing all delivery points.
- A GeoDataFrame (`GeoPandas`) is built from this data for spatial operations.
- An interactive **Folium map** displays all delivery points using marker clusters.

---

### 3. 🧭 Optimize the Delivery Route

- The app builds a graph of drivable roads around the warehouse using **OSMnx**.
- Each delivery location is converted to its **nearest graph node**.
- A **Distance Matrix** is computed using `geodesic` distance.
- A **Nearest Neighbour heuristic** solves a simplified **TSP (Traveling Salesman Problem)** to compute an efficient route.
- The route returns to the warehouse.

---

### 4. 🗺 Visualize Route on Map

- Markers show each delivery location.
- Popups and tooltips display route order and point names.
- A red polyline connects points in optimized order.

---

## 📈 Example CSV Format

```csv
Delivery Point,Latitude,Longitude,Traffic Level,Time of Day
Warehouse,28.6139,77.2090,2,9
Location A,28.6296,77.2182,3,10
Location B,28.6353,77.2026,4,11
Location C,28.6202,77.2304,2,12
Location D,28.6400,77.1985,5,13
```

---

## ⚙️ Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/geo-spatial-route-optimizer.git
   cd geo-spatial-route-optimizer
   ```

2. **Create and activate a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**:
   ```bash
   streamlit run app.py
   ```

---

## 📦 Dependencies

You can add this to a `requirements.txt` file:

```txt
streamlit
pandas
folium
osmnx
networkx
geopandas
shapely
geopy
streamlit-folium
scikit-learn
numpy
plotly
```

---

## 🧠 Future Improvements

- ✅ Incorporate real-time traffic APIs.
- 🧭 Use Dijkstra/A* algorithms for more accurate routing.
- 📍 Let users manually adjust delivery points.
- 🛰 Add map layers (heatmaps, traffic zones).
- 💾 Save optimized routes as GeoJSON or CSV.
- 🧠 Add predictive modeling for delivery times.

---

## 📬 Contact

**Developer:** Mayank Gaurav

---

## 🏁 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

---
