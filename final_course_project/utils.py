import streamlit as st
import datetime
import time

def check_if_OpenBCI():
    return False

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
    
    # Return the rounded datetime object
    return dt + datetime.timedelta(0, rounding - seconds, -dt.microsecond)

def set_alpha_omega_max_min(sleep_option):
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

    return min_time.time(), max_time.time()


def set_deadline(deadline_placeholder, sleep_option):
    min_time, max_time = set_alpha_omega_max_min(sleep_option)
    
    t_alpha = st.time_input("You can wake up FROM", value=min_time, step=15 * 60)
    t_omega = st.time_input("... UNTIL", value=max_time, step=15 * 60)
    
    # Enforce the time range
    if t_omega < t_alpha:
        st.warning(f"Please select an UNTIL time later than FROM ({t_alpha.strftime('%H:%M')})")
    elif t_alpha < min_time:
        st.warning(f"WARNING: You should select a time between {min_time.strftime('%H:%M')} and {max_time.strftime('%H:%M')} to ensure enough sleep time.")
        #@TODO Change this message to be better :)
    else:
        deadline_placeholder.subheader(f":rainbow[MIMIR will wake you up between {t_alpha.strftime('%H:%M')} and {t_omega.strftime('%H:%M')}]")
    
    return t_alpha, t_omega


def start_countdown(countdown_placeholder):
    st.session_state.countdown_started = True
    for i in range(15, -1, -1):
        countdown_placeholder.write(f"Start to monitor your sleep in {i}")
        time.sleep(1)
    countdown_placeholder.write("")
    st.balloons()

    