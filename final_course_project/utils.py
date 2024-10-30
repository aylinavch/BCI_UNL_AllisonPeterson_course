import streamlit as st
import time
import datetime

def check_if_OpenBCI():
    return False

def start_countdown(countdown_placeholder):
    st.session_state.countdown_started = True
    for i in range(15, -1, -1):
        countdown_placeholder.write(f"Start to monitor your sleep in {i}")
        time.sleep(1)
    countdown_placeholder.write("")
    st.balloons()

def roundTime(dt, roundTo=15*60):
    """
    Round a datetime object to the nearest time interval.
    
    dt : datetime.datetime object, default is the current time.
    roundTo : Closest number of seconds to round to, default is 15 minutes.
    """    
    # Calculate total seconds of the day for the given datetime
    seconds = (dt.replace(tzinfo=None) - dt.min).seconds
    # Round to the nearest interval
    rounding = (seconds + roundTo // 2) // roundTo * roundTo
    return dt + datetime.timedelta(0, rounding - seconds, -dt.microsecond)

def set_deadline(deadline_placeholder, sleep_option):
    
    # Round current time
    current_time = roundTime(datetime.datetime.now())

    # Define the time range depending on sleep_option   
    if sleep_option == "Short nap (less than 1 hour)":
        min_time = current_time + datetime.timedelta(minutes=30)
        max_time = current_time + datetime.timedelta(minutes=60)
    elif sleep_option == "Long nap (60 to 90 minutes)":
        min_time = current_time + datetime.timedelta(minutes=60)
        max_time = current_time + datetime.timedelta(minutes=90)
    else: # Sleep night
        min_time = current_time + datetime.timedelta(hours=7)
        max_time = current_time + datetime.timedelta(hours=9)

    # Set up a time input widget
    selected_time = deadline_placeholder.time_input(
        f"Select a time between {min_time.strftime('%H:%M')} and {max_time.strftime('%H:%M')} to wake you up:",
        value=min_time,
        step=15*60)

    # Enforce the time range
    if selected_time.hour < min_time.hour or selected_time.hour > max_time.hour:
        st.warning(f"Please select a time between {min_time.strftime('%H:%M')} and {max_time.strftime('%H:%M')}!")
    else:
        st.write(f":rainbow[MIMIR is going to wake you up before {selected_time.strftime('%H:%M')}hs]")
    return

# def set_alarm(alarm_set_for_placeholder, sleep_option):
#     current_time = datetime.datetime.now()
#     if sleep_option == "Short nap (less than 1 hour)":
#         start_monitoring = current_time + datetime.timedelta(minutes=10)
#     elif sleep_option == "Long nap (60 to 90 minutes)":
#         start_monitoring = current_time + datetime.timedelta(minutes=10)
#     else: # Sleep night
#         start_monitoring = current_time + datetime.timedelta(hours=6)

#     alarm_set_for_placeholder.write(f"MIMIR is going to wake you up from {start_monitoring.strftime('%H:%M')} to deadline")



    