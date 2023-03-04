import streamlit as st
import plotly.express as px
from backend import get_data


st.title("Weather Forecast")

location = st.text_input("Location: ")
days = st.slider("Forecasted Days", min_value=1, max_value=5,
                 help="Select the number of forecasted days")
option = st.selectbox("Select data to view", ("Temperature", 'Sky'))

st.subheader(f"{option} for the next {days} days in {location}")

if location:
    try:
        filtered_data = get_data(location, days)

        if option == "Temperature":
            temperatures = [dict["main"]["temp"] for dict in filtered_data]
            temperatures = [temp/10 for temp in temperatures]
            dates = [dict["dt_txt"] for dict in filtered_data]
            figure = px.line(x=dates, y=temperatures, labels={"x": "Date", "y": "Temperature (C)"})
            st.plotly_chart(figure)

        elif option == "Sky":
            images = {"Clear": "images/clear.png", "Clouds": "images/clouds.png",
                      "Rain": "images/rain.png", "Snow": "images/snow.png"}
            sky_conditions = [dict["weather"][0]["main"] for dict in filtered_data]
            image_paths = [images[conditions] for conditions in sky_conditions]
            st.image(image=image_paths, width=115)
    except KeyError:
        st.code("You input a non-existent location, please check your spelling and try again")
