import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import folium
from streamlit_folium import st_folium
import requests
from sklearn.linear_model import LinearRegression

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Smart City Ultimate", layout="wide")

# ---------------- SIDEBAR ----------------
st.sidebar.title("🌆 Smart City Ultimate")
page = st.sidebar.radio("Navigation", [
    "🏠 Dashboard",
    "🗺️ Live Map",
    "📊 Analytics",
    "🌦️ Weather",
    "🤖 AI Prediction",
    "💬 Chatbot"
])

# ---------------- SAMPLE DATA ----------------
np.random.seed(10)
data = pd.DataFrame({
    "lat": np.random.uniform(21.10, 21.20, 50),
    "lon": np.random.uniform(79.05, 79.15, 50),
    "type": np.random.choice(["Hospital","Restaurant","School","Police"],50),
    "name": [f"Place {i}" for i in range(50)]
})

# ---------------- DASHBOARD ----------------
if page == "🏠 Dashboard":
    st.title("🚀 Smart City Ultimate Dashboard")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Hospitals", len(data[data["type"]=="Hospital"]))
    col2.metric("Restaurants", len(data[data["type"]=="Restaurant"]))
    col3.metric("Schools", len(data[data["type"]=="School"]))
    col4.metric("Police", len(data[data["type"]=="Police"]))

    st.plotly_chart(px.histogram(data, x="type", color="type"))

# ---------------- MAP ----------------
elif page == "🗺️ Live Map":
    st.title("🗺️ Live Smart Map")

    m = folium.Map(location=[21.1458, 79.0882], zoom_start=12)

    for i in range(len(data)):
        folium.Marker(
            [data.iloc[i]["lat"], data.iloc[i]["lon"]],
            popup=f"{data.iloc[i]['name']} ({data.iloc[i]['type']})"
        ).add_to(m)

    st_folium(m, width=700, height=500)

# ---------------- ANALYTICS ----------------
elif page == "📊 Analytics":
    st.title("📊 City Analytics")

    df = pd.DataFrame({
        "Area": ["A","B","C","D"],
        "Population": np.random.randint(50000,100000,4),
        "Pollution": np.random.randint(100,200,4)
    })

    st.plotly_chart(px.bar(df, x="Area", y="Population"))
    st.plotly_chart(px.pie(df, names="Area", values="Pollution"))

# ---------------- WEATHER ----------------
elif page == "🌦️ Weather":
    st.title("🌦️ Live Weather")

    city = st.text_input("Enter City")

    if st.button("Get Weather"):
        api_key = "YOUR_API_KEY"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        res = requests.get(url)
        data_api = res.json()

        if res.status_code == 200:
            st.success(f"Temperature: {data_api['main']['temp']} °C")
            st.info(f"Weather: {data_api['weather'][0]['description']}")
        else:
            st.error("City not found")

# ---------------- AI PREDICTION ----------------
elif page == "🤖 AI Prediction":
    st.title("🤖 Traffic Prediction")

    X = np.array([[1],[2],[3],[4],[5]])
    y = np.array([50,60,65,80,90])

    model = LinearRegression()
    model.fit(X,y)

    day = st.slider("Select Day",1,10)

    pred = model.predict([[day]])
    st.success(f"Predicted Traffic: {int(pred[0])}")

# ---------------- CHATBOT ----------------
elif page == "💬 Chatbot":
    st.title("💬 Smart City Chatbot")

    user_input = st.text_input("Ask something")

    if user_input:
        if "hospital" in user_input.lower():
            st.write("🏥 Nearest hospital is 2 km away")
        elif "traffic" in user_input.lower():
            st.write("🚗 Traffic is moderate today")
        else:
            st.write("🤖 I'm your smart assistant!")
