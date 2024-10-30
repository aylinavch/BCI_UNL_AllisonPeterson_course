import configuration
import mne
import time
from datetime import datetime
from playsound import playsound
import numpy as np
import streamlit as st
#import backend.simulation_utils
from matplotlib import pyplot as plt
import yasa


def load_psg():
    """
    Load polysomnography data from a file
    """
    raw = mne.io.read_raw_edf(configuration.EDF_PATH, preload=True)
    return raw.get_data(), raw.info
#scoring_path = configuration.SCORING_PATH

def plotter(data, fs, raw_info, plot_placeholder, stage_placeholder, hypno_placeholder, prevstage_placeholder, t_alpha,t_omega,SLEEP_STAGES = ['W']):
    """
    """
    signal = data[1]*1e6
    #signal =  @TODO: Filter eeg signal
    fs = int(fs)
    window_duration = 30
    window_size = int(window_duration * fs)
    window_size_scoring = int(window_duration * fs * 2)
    
    # HYPNOGRAM
    fig_hypno, ax_hypno = plt.subplots(figsize=(15, 3))           
    fig_hypno.patch.set_alpha(0)
    ax_hypno.spines['top'].set_color('white')
    ax_hypno.spines['right'].set_color('white')
    ax_hypno.spines['left'].set_color('white')
    ax_hypno.spines['bottom'].set_color('white')
    ax_hypno.tick_params(axis='x', colors='white')
    ax_hypno.tick_params(axis='y', colors='white')

    # EEG
    fig, ax = plt.subplots(figsize=(15, 5))
    fig.patch.set_alpha(0)
    ax.spines['top'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['bottom'].set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    for i in range(0, len(signal) - window_size, fs):
        n_epoch = int(i//(30*fs))+1
        
        if n_epoch==1:
            current_stage=' '
        elif n_epoch==2:
            current_stage='W'
        
        if i <= 30*fs:
            window_data = signal[:i]
            time_axis = np.arange(0, i) / fs 
        else:    
            window_data = signal[i - window_size:i]
            time_axis = np.arange(i - window_size, i) / fs 

        ax.cla()
        ax.set_facecolor('none')
        ax.plot(time_axis, window_data, color='yellow')
        ax.set_title('EEG', fontsize=14, color='white')
        ax.set_xlabel('Tiempo (s)', fontsize=12, color='white')
        ax.set_ylabel('Amplitud (uV)', fontsize=12, color='white')

        plot_placeholder.pyplot(fig)

        if n_epoch>2 and i%int(30*fs)==0:
            if n_epoch == 3:
                st.toast("Starting to detect sleep stages")
            start = i - window_size_scoring
            end = i + 1
            chunk_data = data[:, int(start):int(end)]
            raw_chunk = mne.io.RawArray(chunk_data, raw_info)
            sls = yasa.SleepStaging(raw_chunk, eeg_name='EEG C4-M1', eog_name='EOG E1-M2', emg_name='EMG chin')
            hypno = sls.predict()
            current_stage = hypno[-1]
            SLEEP_STAGES.append(current_stage)
            time_hypno = np.linspace(1, n_epoch-1, len(SLEEP_STAGES))
            
            ax_hypno.cla()
            ax_hypno.set_facecolor('none')
            ax_hypno.plot(time_hypno, SLEEP_STAGES, '-o', color='blue')
            ax_hypno.set_title('HYPNOGRAM', fontsize=14, color='white')
            ax_hypno.set_xlabel('Time (epochs)', color='white')
            ax_hypno.set_ylabel('Sleep Stage', color='white')
            ax_hypno.set_ylim(-0.5, 4.5)
            ax_hypno.set_yticks([0, 4, 1, 2, 3])
            ax_hypno.set_yticklabels(['Wake', 'REM', 'N1', 'N2', 'N3']) #@TODO: Change it to be like an hypnogram
            
            hypno_placeholder.pyplot(fig_hypno)
            now = datetime.now()
            if n_epoch > 5:
                if now.time() > t_alpha:
                    if not 'N3' in SLEEP_STAGES[-5:-1]:
                        st.write("Wake up! The time is now", datetime.now().strftime('%H:%M'))
                        playsound('final_course_project/data/alarm_sound.mp3')
                elif now.time() > t_omega:
                    st.write("Wake up! The time is now", datetime.now().strftime('%H:%M'))
                    playsound('final_course_project/data/alarm_sound.mp3')
        stage_placeholder.write(f"**Epoch:** {n_epoch}")
        prevstage_placeholder.write(f":blue[**Previous sleep stage:** {current_stage}]")
        #time.sleep(0.01)
    # window_size = int(fs * 30 * 2)
    # Get EDF necessary data
    

    #st.write("... Start monitoring sleep stages ...")
    
    #n_windows = len(data[0]) // window_size  # Total number of windows

    # # Create placeholders for dynamic updates
    # window_info_placeholder = st.empty()
    # stage_info_placeholder = st.empty()

    # for i in range(n_windows):
    #     start = i * window_size
    #     end = start + window_size - 1

    #     if end > len(data[0]):
    #         break

    #     # Simulate reading a 30-second window
    #     chunk_data = data[:, start:end]

    #     # Use YASA to predict sleep stages for this window (this is simulated)
    #     window_info_placeholder.write(f"Analyzing window {i + 1}/{n_windows}: {start/fs:.2f}-{(end+1)/fs:.2f} seconds")

    #     # Create a temporary Raw object for this chunk (YASA requires an MNE Raw object)
    #     raw_chunk = mne.io.RawArray(chunk_data, raw.info)

    #     # Sleep stage prediction using YASA for this chunk
    #     
    #     # Current sleep stage (for the last window)
    #     current_stage = hypno[-1]  # Last sleep stage detected in the current window
    #     stage_info_placeholder.write(f"Predicted sleep stage for the current window: {current_stage}")

    #     # Trigger alert if N2 stage is detected
    #     if current_stage == 'N2':
    #         st.write("ALERT! Person is in N2 stage. Wake up...")
    #         st.balloons()  # Simulate alert with balloons (you can replace this with a sound or other alert)
    #         playsound(configuration.ALARM_PATH)
    #         break

