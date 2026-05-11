import streamlit as st
import pickle
from PIL import Image
import pandas as pd

# load artifacts
model = pickle.load(open('./model/model.pkl','rb'))
scaler = pickle.load(open('./model/scaler.pkl','rb'))
features = pickle.load(open('./model/features.pkl','rb'))

scale_cols = [
    'Delivery_person_Age',
    'Delivery_person_Ratings',
    'Distance'
]

# Tittle
st.markdown("""
    <h1 style='text-align: center; color: white; background-color: red; padding: 20px; border-radius: 10px;'>
        Food Delivery Time Prediction
    </h1>
    """, unsafe_allow_html=True)


# Image
image = Image.open(r"C:\Users\babus\Data_Spark\Project\Zomato\Deployment\image.png")
st.image(image,width=800)


# INPUTS

# Delivery Person Age
st.subheader("Delivery Person Age")
age = st.number_input("Age", 18, 60, 30,label_visibility="collapsed")

# Delivery Person Rating
st.subheader("Delivery Person Rating")
selected = st.feedback("stars")
if selected == 0:
    rating = 1
elif selected == 1:
    rating = 2
elif selected == 2:
    rating = 3
elif selected == 3:
    rating = 4
elif selected == 4:
    rating = 5
else:
     rating = 0


# Distance
st.subheader("Distance (Km)")
distance = st.number_input("Rating", 0.1, 30.0, 5.0,label_visibility="collapsed")

# Multiple Deliveries
st.subheader("Multiple Deliveries")
multi_delivery = st.number_input("Multiple",0,3,0,label_visibility="collapsed")


# Road Traffic Density
traffic_map = {
    "Low": 0,
    "Medium": 1,
    "High": 2,
    "Jam": 3
}
st.subheader("Road Traffic Density")
traffic_choice = st.selectbox("Traffic", list(traffic_map.keys()),label_visibility="collapsed")
traffic_value = traffic_map[traffic_choice]

# City
st.subheader("City")
city_map = {
    "Semi-Urban" : 0,
    "Urban" : 1,
    "Metropolitan" : 2 
}
city_choice = st.selectbox("City",list(city_map.keys()),label_visibility="collapsed")
city_value = city_map[city_choice]

# Festival
st.subheader("Festival")
festival_map = {
    "No" : 0,
    "Yes" : 1
}
festival_choice = st.selectbox("Festival",list(festival_map.keys()),label_visibility="collapsed")
festival_value = festival_map[festival_choice]

# Time_slot
st.subheader("Time Slot")
time_map = {
    "Morning":0,
    "Afternoon":1,
    "Evening":2,
    "Night": 3
}
time_choice = st.selectbox("Time",list(time_map.keys()),label_visibility="collapsed")
time_value = time_map[time_choice]

# Prepration_minute
st.subheader("Preparation Time")
prep_options = [
    "Below 5 minutes", 
    "5 - 10 minutes", 
    "10 - 15 minutes", 
    "Above 15 minutes"
]
prep_choice = st.selectbox("Preparation", prep_options,label_visibility="collapsed")

if prep_choice == "Below 5 minutes":
    prep_time = 5
elif prep_choice == "5 - 10 minutes":
    prep_time = 10
elif prep_choice == "10 - 15 minutes":
    prep_time = 15
else:  # Above 15 minutes
    prep_time = 15 


# Is_Weekend
st.subheader("Day of the Week")
day_map =  {"Monday":0, "Tuesday":0, "Wednesday":0, "Thursday":0, "Friday":0, "Saturday":1, "Sunday":1}
day =   st.selectbox("Week", list(day_map.keys()),label_visibility="collapsed")
weekend = day_map[day]

# Peak_hour
st.subheader("Peak Hour Status")
hour_labels = [f"{h:02d}:00" for h in range(24)]
selected_hour = st.selectbox("Hour", range(24), format_func=lambda x: hour_labels[x],label_visibility="collapsed")
lunch_hour = ( selected_hour >= 11 ) & ( selected_hour <= 14 )
dinner_hour = ( selected_hour >= 18 ) & ( selected_hour <= 21 )
if lunch_hour or dinner_hour:
    peak_status = "Peak Hour"
    st.warning(f"🕒 This is a **{peak_status}**! Deliveries might be slower.")
else:
    peak_status = "Non-Peak Hour"
    st.success(f"✅ This is a **{peak_status}**.")
if peak_status == "Peak Hour":
    hour = 1
else:
    hour = 0


# Weather_conditions_
st.subheader("Weather Conditions")
options = ['Sandstorms', 'Stormy', 'Fog' ,'Windy', 'Cloudy', 'Sunny']
weather = st.selectbox("Weather", options,label_visibility="collapsed")

weather_fog = 0
weather_sandstorms = 0
weather_stormy = 0
weather_sunny = 0
weather_windy = 0
weather_cloudy = 0

if weather == 'Fog':
    weather_fog = 1
elif weather == 'Sandstorms':
    weather_sandstorms = 1
elif weather == 'Stormy':
    weather_stormy = 1
elif weather == 'Sunny':
    weather_sunny = 1
elif weather == 'Windy':
    weather_windy = 1
else:
    weather_cloudy = 1


# Type_of_vehicle
st.subheader("Type Of Vehicle")
v_list =  ['Scooter','Motorcycle','Electric scooter']
Vehicle = st.radio("Vehicle",['Scooter','Motorcycle','Electric scooter'],label_visibility="collapsed")
# Vehicle = st.selectbox("Type Of Vehicle",v_list)

vechcle_scooter = int(Vehicle == 'Scooter')
vechcle_motorcycle = int(Vehicle == 'Motorcycle')
vechcle_electric_scooter = int(Vehicle == 'Electric scooter')




# build input dictionary
input_data = {
    'Delivery_person_Age': age,
    'Delivery_person_Ratings': rating,
    'Distance': distance,
    'Road_traffic_density': traffic_value,
    'City': city_value,
    'Festival': festival_value,
    'Multiple_deliveries':multi_delivery,
    "Time_slot":time_value,
    "Prepration_minute":prep_time,
    "Is_Weekend" : weekend,
    "Peak_hour":hour,
    "Weather_conditions_Fog": weather_fog,
    "Weather_conditions_Sandstorms": weather_sandstorms,
    "Weather_conditions_Stormy": weather_stormy,
    "Weather_conditions_Sunny": weather_sunny,
    "Weather_conditions_Windy": weather_windy,
    "Type_of_vehicle_motorcycle": vechcle_motorcycle,
    "Type_of_vehicle_scooter":vechcle_scooter
}

st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #4CAF50;
        color: white;
        height: 3em;
        width: 100%;
        border-radius: 10px;
        border: none;
        font-weight: bold;
    }
    /* Change color on hover */
    div.stButton > button:first-child:hover {
        background-color: #45a049;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)


if st.button("Predict Delivery Time"):

    df = pd.DataFrame([input_data])

    # enforce column order
    df = df[features]

    # scaling
    df[scale_cols] = scaler.transform(df[scale_cols])

    prediction = model.predict(df)[0]

    st.success(f"Predicted Delivery Time : {round(prediction)} Minutes")