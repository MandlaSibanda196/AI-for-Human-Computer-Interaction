import streamlit as st
import datetime
import pytz
import random

st.subheader("Hello, world!", anchor=False)

# List of timezones
timezones = pytz.all_timezones

if st.button("Show Current Time in a Random City"):
    # Select a random timezone
    random_timezone_str = random.choice(timezones)
    random_timezone = pytz.timezone(random_timezone_str)

    # Get the current time in that timezone
    current_time = datetime.datetime.now(random_timezone)
    
    # Display the city and time
    city = random_timezone_str.split('/')[-1].replace('_', ' ')
    st.write(f"The current time in {city} ({random_timezone_str}) is: {current_time.strftime('%Y-%m-%d %H:%M:%S')}") 