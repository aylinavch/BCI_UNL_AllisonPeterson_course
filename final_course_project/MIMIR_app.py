import streamlit as st
import numpy as np
import pandas as pd

from playsound import playsound

import configuration
import tempfile
import mne
import yasa
import time
import os

# Title of the app
st.title("MIMIR :sleeping:")
st.header("More Intelligent Method to Initiate your Routine", divider='gray')

# Load EEG data from an uploaded file
@st.cache_data
def load_eeg_data(file):
    #with tempfile.NamedTemporaryFile(delete=False, suffix=".edf") as tmp_file:
    #    tmp_file.write(file.read())
    #    tmp_file_path = tmp_file.name
    tmp_file_path = file
    raw = mne.io.read_raw_edf(tmp_file_path, preload=True)
    #os.remove(tmp_file_path)
    return raw

#eeg_file = st.file_uploader("Upload EEG data file (only EDF format)", type=['edf'])
eeg_file = configuration.EDF_PATH
scoring_file = configuration.SCORING_PATH

if eeg_file is not None:
    # Get EDF necessary data
    raw = load_eeg_data(eeg_file)
    data = raw.get_data()
    fs = raw.info['sfreq']
    window_size = int(fs * 30 * 2)

    option = st.selectbox(
    "How many hours do you want to sleep?",
    ("Short nap (less than 1 hour)", "Long nap (60 to 90 minutes)", "Sleep night (7 to 9 hours)"))

    # # Visualize the first epoch of first two EEG channels
    # data = raw.get_data()  # Get all EEG data
    # first_channel = data[0][:int(30*fs)]  # First 1000 samples from the first channel
    # second_channel = data[1][:int(30*fs)]  # First 1000 samples from the second channel
    # df = pd.DataFrame({
    #     raw.info['ch_names'][0]: first_channel,
    #     raw.info['ch_names'][1]: second_channel
    # })
    # st.write("EEG Signal (first two channels):")
    # st.line_chart(df)

    # Sleep stage detection using YASA
    #st.write("Detecting Sleep Stages...")
    #sls = yasa.SleepStaging(raw, eeg_name='EEG C4-M1', eog_name='EOG E1-M2', emg_name='EMG chin')
    #hypno = sls.predict()  # Predict sleep stages

    # Add button to start monitoring
    monitoring = st.button("START", icon="💤")

    # Monitoring loop to check for N2 stage
    if monitoring:
        st.write("... Start monitoring sleep stages ...")
        
        n_windows = len(data[0]) // window_size  # Total number of windows

        # Create placeholders for dynamic updates
        window_info_placeholder = st.empty()
        stage_info_placeholder = st.empty()

        for i in range(n_windows):
            start = i * window_size
            end = start + window_size - 1

            if end > len(data[0]):
                break

            # Simulate reading a 30-second window
            chunk_data = data[:, start:end]

            # Use YASA to predict sleep stages for this window (this is simulated)
            window_info_placeholder.write(f"Analyzing window {i + 1}/{n_windows}: {start/fs:.2f}-{(end+1)/fs:.2f} seconds")

            # Create a temporary Raw object for this chunk (YASA requires an MNE Raw object)
            raw_chunk = mne.io.RawArray(chunk_data, raw.info)

            # Sleep stage prediction using YASA for this chunk
            sls = yasa.SleepStaging(raw_chunk, eeg_name='EEG C4-M1', eog_name='EOG E1-M2', emg_name='EMG chin')
            hypno = sls.predict()  # Predict sleep stages for the chunk

            # Current sleep stage (for the last window)
            current_stage = hypno[-1]  # Last sleep stage detected in the current window
            stage_info_placeholder.write(f"Predicted sleep stage for the current window: {current_stage}")

            # Trigger alert if N2 stage is detected
            if current_stage == 'N2':
                st.write("ALERT! Person is in N2 stage. Wake up...")
                st.balloons()  # Simulate alert with balloons (you can replace this with a sound or other alert)
                playsound(configuration.ALARM_PATH)
                break
else:
    st.write("Please upload an EEG file to start.")

# Footer
st.write("*By Santiago Valentino Blas Laguzza, Carlos Andrés Mateos and Aylin Agatha Vazquez Chenlo*")