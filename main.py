import streamlit as st
import json

# Load existing data from JSON file (if available)
try:
    with open("localities.json", "r") as f:
        distance_data = json.load(f)
except FileNotFoundError:
    distance_data = {}

# Streamlit app
st.title("Locality Information Tracker")

# Sidebar navigation
page = st.sidebar.radio("Navigation", ["Admin Page", "User Page"])

if page == "Admin Page":
    st.header("Admin Page")
    
    # Input fields for admin page
    with st.form(key='admin_form'):
        start_locality = st.text_input("Starting Locality")
        end_locality = st.text_input("Destination Locality")
        distance = st.number_input("Distance (km)", min_value=0.0, format="%.2f", step=0.01)
        time_travel = st.number_input("Time Travel (hrs)", min_value=0.0, format="%.2f", step=0.01)
        num_stops = st.number_input("Number of Stops", min_value=0, format="%d")
        fuel_consumption = st.number_input("Fuel Consumption (L/km)", min_value=0.0, format="%.2f", step=0.01)

        submitted = st.form_submit_button("Add Route")

        if submitted:
            # Update distance data dictionary with new route information
            if start_locality not in distance_data:
                distance_data[start_locality] = {}
            distance_data[start_locality][end_locality] = {
                "Distance (km)": distance,
                "Time Travel (hrs)": time_travel,
                "Number of Stops": num_stops,
                "Fuel Consumption (L/km)": fuel_consumption
            }
            
            # Update distance data dictionary with return route information
            if end_locality not in distance_data:
                distance_data[end_locality] = {}
            distance_data[end_locality][start_locality] = {
                "Distance (km)": distance,
                "Time Travel (hrs)": time_travel,
                "Number of Stops": num_stops,
                "Fuel Consumption (L/km)": fuel_consumption
            }

            st.success("Route added successfully!")

    # Save data to JSON file
    with open("localities.json", "w") as f:
        json.dump(distance_data, f)

elif page == "User Page":
    st.header("User Page")
    
    
    # Load localities for user page
    localities = list(distance_data.keys())

    # Input fields for route calculation
    start_locality = st.selectbox("Select starting locality:", localities)
    end_locality = st.selectbox("Select destination locality:", localities)

    # Check if start and end localities are in the distance data
    if start_locality in distance_data and end_locality in distance_data[start_locality]:
        route_info = distance_data[start_locality][end_locality]
        st.write(f"### Route Information from {start_locality} to {end_locality}:")
        st.write(f"Distance: {route_info['Distance (km)']:.2f} km")
        st.write(f"Time Travel: {route_info['Time Travel (hrs)']:.2f} hrs")
        st.write(f"Number of Stops: {route_info['Number of Stops']}")
        st.write(f"Fuel Consumption: {route_info['Fuel Consumption (L/km)']:.2f} L/km")
    elif start_locality == end_locality:
        st.error("You want to pay for not moving? Get on baby!", icon="🚨")
    else:
        st.warning("The selected origin or destination is not available right now.", icon="⚠️")
