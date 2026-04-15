import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px
from math import radians, cos, sin, asin, sqrt

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Smart City Explorer Pro", layout="wide")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}
.card {
    padding: 20px;
    border-radius: 15px;
    background: rgba(255,255,255,0.1);
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("🌆 Smart City Explorer PRO")
page = st.sidebar.radio("Navigation", [
    "🏠 Dashboard",
    "🗺️ Smart Map",
    "📊 Analytics",
    "📍 Nearby",
    "🤖 AI Insights",
    "📂 Upload Data"
])

# ---------------- SAMPLE DATA ----------------
np.random.seed(1)
data = pd.DataFrame({
    "lat": np.random.uniform(21.10, 21.20, 150),
    "lon": np.random.uniform(79.05, 79.15, 150),
    "type": np.random.choice(["Hospital", "Restaurant", "School", "Police"], 150),
    "name": [f"Location {i}" for i in range(150)]
})

# ---------------- COLOR MAP ----------------
color_map = {
    "Hospital": [255, 0, 0],
    "Restaurant": [0, 255, 0],
    "School": [0, 0, 255],
    "Police": [255, 255, 0]
}

data["color"] = data["type"].map(color_map)

# ---------------- DISTANCE ----------------
def distance(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    return 6371 * 2 * asin(sqrt(
        sin((lat2 - lat1)/2)**2 +
        cos(lat1)*cos(lat2)*sin((lon2 - lon1)/2)**2
    ))

# ---------------- DASHBOARD ----------------
if page == "🏠 Dashboard":
    st.title("🚀 Smart City Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("🏥 Hospitals", len(data[data["type"]=="Hospital"]))
    col2.metric("🍽️ Restaurants", len(data[data["type"]=="Restaurant"]))
    col3.metric("🏫 Schools", len(data[data["type"]=="School"]))
    col4.metric("🚓 Police", len(data[data["type"]=="Police"]))

    st.markdown("### 📈 Live Distribution")
    fig = px.histogram(data, x="type", color="type", animation_frame=None)
    st.plotly_chart(fig, use_container_width=True)

# ---------------- MAP ----------------
elif page == "🗺️ Smart Map":
    st.title("🗺️ Smart Interactive Map")

    category = st.multiselect(
        "Select Categories",
        options=data["type"].unique(),
        default=data["type"].unique()
    )

    filtered = data[data["type"].isin(category)]

    st.pydeck_chart(pdk.Deck(
        initial_view_state=pdk.ViewState(
            latitude=21.1458,
            longitude=79.0882,
            zoom=11,
            pitch=45,
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=filtered,
                get_position='[lon, lat]',
                get_color="color",
                get_radius=300,
                pickable=True,
            ),
        ],
        tooltip={"text": "{name}\nType: {type}"}
    ))

# ---------------- ANALYTICS ----------------
elif page == "📊 Analytics":
    st.title("📊 Advanced Analytics")

    df = pd.DataFrame({
        "Area": ["A","B","C","D"],
        "Population": np.random.randint(50000, 100000, 4),
        "Pollution": np.random.randint(100, 200, 4),
        "Traffic": np.random.randint(50, 100, 4)
    })

    tab1, tab2, tab3 = st.tabs(["Population", "Pollution", "Traffic"])

    with tab1:
        st.plotly_chart(px.bar(df, x="Area", y="Population", color="Area"))

    with tab2:
        st.plotly_chart(px.pie(df, names="Area", values="Pollution"))

    with tab3:
        st.plotly_chart(px.line(df, x="Area", y="Traffic", markers=True))

# ---------------- NEARBY ----------------
elif page == "📍 Nearby":
    st.title("📍 Nearby Smart Finder")

    user_lat = st.slider("Latitude", 21.10, 21.20, 21.1458)
    user_lon = st.slider("Longitude", 79.05, 79.15, 79.0882)

    data["dist"] = data.apply(
        lambda x: distance(user_lat, user_lon, x["lat"], x["lon"]), axis=1
    )

    nearest = data.sort_values("dist").head(10)

    st.dataframe(nearest)

# ---------------- AI ----------------
elif page == "🤖 AI Insights":
    st.title("🤖 AI Urban Intelligence")

    city = st.text_input("Enter City")

    if st.button("Generate Insights"):
        if city:
            st.success(f"Analysis for {city}")

            score = np.random.randint(60, 95)

            st.progress(score/100)
            st.metric("Safety Score", score)

            st.info("✔️ Best Area: Central Zone")
            st.warning("⚠️ Traffic: Moderate")
            st.success("🌿 Air Quality: Good")

# ---------------- UPLOAD ----------------
elif page == "📂 Upload Data":
    st.title("📂 Smart Data Analyzer")

    file = st.file_uploader("Upload CSV")

    if file:
        df = pd.read_csv(file)

        st.dataframe(df)

        col = st.selectbox("Select Column", df.columns)

        st.plotly_chart(px.histogram(df, x=col, color_discrete_sequence=["cyan"]))
