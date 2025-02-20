import streamlit as st
import pandas as pd
import altair as alt


st.set_page_config(page_title="Exoplanet Data Explorer", page_icon="🪐", layout="wide")

st.title("🪐 Exoplanet Data Explorer")
st.write("Explore key parameters of confirmed exoplanets from NASA's Exoplanet Archive")


st.markdown(
    """
    This interactive tool allows you to explore exoplanets discovered beyond our Solar System.
    - Use the **filters** to adjust the mass range and distance from Earth.
    - The **visualization** displays exoplanet equlibrium temperature vs. mass (Earth masses), with color indicating distance from Earth.
    - The **data table** provides detailed information on filtered exoplanets.
    
    🚀 *Explore the universe with real astronomical data!*
    """
)

# load exoplanets.csv and clean data
@st.cache_data
def load_data():
    df = pd.read_csv("exoplanets.csv", sep=",", na_values=["NA", ""])
    
    #select relevant columns
    df = df[["pl_name", "pl_eqt", "pl_bmasse", "pl_orbsmax", "pl_rade", "st_teff", "sy_dist"]].copy()
    df = df.rename(columns={
        "pl_name": "Exoplanet", 
        "pl_eqt": "Equilibrium Temp (K)", 
        "pl_bmasse": "Mass (Earth Masses)",
        "pl_orbsmax": "Semi-Major Axis (AU)",
        "pl_rade": "Radius (Earth Radii)",
        "st_teff": "Host Star Temp (K)",
        "sy_dist": "Distance from Earth (pc)"
    })
    
    #remove rows with missing values
    df = df.dropna()
    
    return df

df = load_data()

# filters
min_mass, max_mass = st.slider("Select Exoplanet Mass Range (Earth Masses)", 0.1, 50.0, (0.5, 5.0))
min_distance, max_distance = st.slider("Select Distance Range (pc)", 0, 1000, (0, 500))
df_filtered = df[
    (df["Mass (Earth Masses)"] >= min_mass) & (df["Mass (Earth Masses)"] <= max_mass) &
    (df["Distance from Earth (pc)"] >= min_distance) & (df["Distance from Earth (pc)"] <= max_distance)
]

# data visualization
chart = alt.Chart(df_filtered).mark_circle(size=100).encode(
    x=alt.X("Mass (Earth Masses):Q", title="Exoplanet Mass (Earth Masses)"),
    y=alt.Y("Equilibrium Temp (K):Q", title="Equilibrium Temperature (K)"),
    color=alt.Color("Distance from Earth (pc):Q", scale=alt.Scale(scheme="viridis")),
    tooltip=["Exoplanet", "Mass (Earth Masses)", "Equilibrium Temp (K)", "Distance from Earth (pc)"]
).properties(width=800, height=500, title="Exoplanet Mass vs. Temperature")

st.altair_chart(chart, use_container_width=True)

#display filtered data
st.write("📊 **Filtered Exoplanet Data**")
st.dataframe(df_filtered)

st.write("🚀 Data Source: [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/) (Planetary Systems Composite Data)")
st.write("<p style='color:grey;'>A project by PY Heng</p>", unsafe_allow_html=True)