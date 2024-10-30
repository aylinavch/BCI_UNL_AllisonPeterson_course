import streamlit as st
import utils
from frontend import header, footer
from backend import simulation
import matplotlib.pyplot as plt
import datetime


# Header
st.title(header.app_name_emoji)
st.subheader(header.header, divider='blue')

# Footer
st.markdown(footer.footer, unsafe_allow_html=True)

# Sleep option
t_alpha = st.time_input("Set an alarm from", value=None)
t_omega = st.time_input("...until", value=None)
st.write("Alarm is set between", t_alpha, "and",t_omega)

# Start button
if 'button' not in st.session_state:
    st.session_state.button = False

def click_button():
    st.session_state.button = not st.session_state.button

start_button = st.button("START", 
          key="start_monitoring",
          icon="💤", 
          help='Click to start monitoring your sleep',
          on_click=click_button,
          disabled=st.session_state.button)

# Count down + Signal plot + Stage + Hypnogram
if start_button:
    countdown_placeholder = st.empty()
    #utils.start_countdown(countdown_placeholder)

    if utils.check_if_OpenBCI():
        print('Not ready yet')
    else:
        data, raw_info = simulation.load_psg()
        fs, ch_names = raw_info['sfreq'], raw_info['ch_names']
        st.title('Monitoring your sleep ...')
        col1, col2 = st.columns(2)
        with col1:
            stage_placeholder = st.empty()
        with col2:
            prevstage_placeholder = st.empty()
        hypno_placeholder = st.empty()
        plot_placeholder = st.empty()
        simulation.plotter(data, fs, raw_info, plot_placeholder, stage_placeholder, hypno_placeholder, prevstage_placeholder,t_alpha,t_omega)


else:
    st.write("*Please select how many hours you want to sleep.*")