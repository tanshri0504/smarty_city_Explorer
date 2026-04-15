import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px
from math import radians, cos, sin, asin, sqrt

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Smart City Explorer", layout="wide")

# ---------------- SIDEBAR ----------------
st.sidebar.title("🌆 Smart City Explorer")
page = st.sidebar.radio("Navigate", [
    "🏠 Home",
    "🗺️ Map",
    "📊 Analytics",
    "🚨 Emergency",
    "🤖 AI Insights",
    "📍 Nearby Services",
    "📅 Booking",
    "📂 Upload Data"
])

# ---------------- SAMPLE DATA ----------------
np.random.seed(42)

data = pd.DataFrame({
    "lat": np.random.uniform(21.10, 21.20, 100),
    "lon": np.random.uniform(79.05, 79.15, 100),
    "type": np.random.choice(["Hospital", "Restaurant", "School", "Police"], 100),
    "name": [f"Place {i}" for i in range(100)]
})

# ---------------- HOME ----------------
if page == "🏠 Home":
    st.title("🚀 Smart City Explorer")
    st.markdown("### All-in-One Urban Intelligence Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("🏥 Hospitals", 25)
    col2.metric("🍽️ Restaurants", 40)
    col3.metric("🚓 Police Stations", 15)

    st.success("✔️ Real-time city insights at your fingertips!")

# ---------------- MAP ----------------
elif page == "🗺️ Map":
    st.title("🗺️ Interactive City Map")

    category = st.selectbox("Filter by Category", ["All"] + list(data["type"].unique()))

    if category != "All":
        filtered = data[data["type"] == category]
    else:
        filtered = data

    st.pydeck_chart(pdk.Deck(
        initial_view_state=pdk.ViewState(
            latitude=21.1458,
            longitude=79.0882,
            zoom=11,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=filtered,
                get_position='[lon, lat]',
                get_color='[200, 30, 0, 160]',
                get_radius=200,
                pickable=True,
            ),
        ],
        tooltip={"text": "{name}\nType: {type}"}
    ))

# ---------------- ANALYTICS ----------------
elif page == "📊 Analytics":
    st.title("📊 City Analytics Dashboard")

    df = pd.DataFrame({
        "Area": ["A", "B", "C", "D"],
        "Population": [50000, 70000, 65000, 80000],
        "Pollution": [120, 140, 110, 160],
        "Traffic": [60, 80, 75, 90]
    })

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(df, x="Area", y="Population", title="Population")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.line(df, x="Area", y="Traffic", title="Traffic")
        st.plotly_chart(fig, use_container_width=True)

    fig = px.pie(df, names="Area", values="Pollution", title="Pollution Levels")
    st.plotly_chart(fig, use_container_width=True)

# ---------------- EMERGENCY ----------------
elif page == "🚨 Emergency":
    st.title("🚨 Emergency Dashboard")

    st.error("🚑 Emergency Contacts")

    st.write("""
    - Police: 100
    - Ambulance: 102
    - Fire: 101
    """)

    if st.button("🚨 Send Emergency Alert"):
        st.success("Alert Sent Successfully!")

# ---------------- AI INSIGHTS ----------------
elif page == "🤖 AI Insights":
    st.title("🤖 AI City Insights")

    city = st.text_input("Enter City Name")

    if st.button("Analyze"):
        if city:
            score = np.random.randint(60, 95)

            st.subheader(f"🏙️ {city} Analysis")

            st.write(f"✔️ Safety Score: {score}/100")
            st.write("✔️ Best Area: Central Zone")
            st.write("✔️ Traffic: Moderate")
        else:
            st.warning("Enter city name")

# ---------------- DISTANCE FUNCTION ----------------
def calculate_distance(lat1, lon1, lat2, lon2):
    # Haversine Formula
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))

    return 6371 * c

# ---------------- NEARBY ----------------
elif page == "📍 Nearby Services":
    st.title("📍 Nearby Services")

    user_lat = st.number_input("Your Latitude", value=21.1458)
    user_lon = st.number_input("Your Longitude", value=79.0882)

    data["distance"] = data.apply(
        lambda x: calculate_distance(user_lat, user_lon, x["lat"], x["lon"]), axis=1
    )

    nearest = data.sort_values("distance").head(5)

    st.write("### Closest Locations")
    st.dataframe(nearest[["name", "type", "distance"]])

# ---------------- BOOKING ----------------
elif page == "📅 Booking":
    st.title("📅 Booking System")

    service = st.selectbox("Select Service", ["Hospital", "Restaurant"])

    name = st.text_input("Your Name")
    date = st.date_input("Select Date")

    if st.button("Book Now"):
        st.success(f"{service} booked successfully for {name} on {date}")

# ---------------- UPLOAD ----------------
elif page == "📂 Upload Data":
    st.title("📂 Upload & Analyze Data")

    file = st.file_uploader("Upload CSV", type=["csv"])

    if file:
        df = pd.read_csv(file)
        st.dataframe(df)

        st.subheader("📊 Auto Visualization")
        fig = px.histogram(df, x=df.columns[0])
        st.plotly_chart(fig, use_container_width=True)
