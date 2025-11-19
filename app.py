import streamlit as st
import requests
import pandas as pd
import altair as alt

# --- Config ---
ACCESS_TOKEN = "66ff4fba9c2ad49a91fbcab7ed5029f001143b0c"
BASE_URL = "https://www.strava.com/api/v3"

# --- Fetch Data ---
@st.cache_data
def get_activities():
    activities = []
    page = 1
    while True:
        url = f"{BASE_URL}/athlete/activities"
        #params = {"per_page": 200, "page": page}
        params = {"per_page": 10, "page": 2}
        headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
        r = requests.get(url, headers=headers, params=params)
        data = r.json()
        if not data:
            break
        activities.extend(data)
        page += 1
        if len(filtered_activities) >= 10:
            break

    return pd.DataFrame(activities)

# --- UI ---
st.title("Strava Dashboard")
df = get_activities()

st.write("Total Activities:", len(df))
st.write(df.head())

# --- Charts ---
distance_chart = alt.Chart(df).mark_line().encode(
    x='start_date:T',
    y='distance:Q'
).properties(title="Distance Over Time")

st.altair_chart(distance_chart, use_container_width=True)

# --- Download ---
csv = df.to_csv(index=False)
st.download_button("Download CSV", csv, "strava_activities.csv", "text/csv")

