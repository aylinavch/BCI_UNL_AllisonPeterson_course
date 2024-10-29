import streamlit as st
import time

def check_if_OpenBCI():
    return False

def check_best_time_to_get_up(current_time, time_before_to_wake_up):
    """
    """
    print('Not developed yet')

def start_countdown(countdown_placeholder):
    st.session_state.countdown_started = True
    for i in range(15, -1, -1):
        countdown_placeholder.write(f"Start to monitor your sleep in {i}")
        time.sleep(1)
    countdown_placeholder.write("")
    st.balloons()

    