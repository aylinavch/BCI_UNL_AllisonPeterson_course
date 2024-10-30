import configuration
import mne
import re
import time
from datetime import datetime
from playsound import playsound
import numpy as np
import streamlit as st
from backend.simulation_utils import filter_signal
from matplotlib import pyplot as plt
import yasa


def load_psg():
    """
    Load polysomnography data from a file
    """
    raw = mne.io.read_raw_edf(configuration.EDF_PATH, preload=True)
    return raw
#scoring_path = configuration.SCORING_PATH

def simulate(raw, plot_placeholder, stage_placeholder, hypno_placeholder, prevstage_placeholder, t_alpha, t_omega, SLEEP_STAGES = ['W']):
    """
    """
    data_raw, fs, ch_names = raw.get_data(), raw.info['sfreq'], raw.info['ch_names']
    fs = int(fs)

    EEG_CHANNELS = [i for i in ch_names if re.match(r"\bEEG\w*\b", i)]
    EOG_CHANNELS = [i for i in ch_names if re.match(r"\bEOG\w*\b", i)]
    EMG_CHANNELS = [i for i in ch_names if re.match(r"\bEMG\w*\b", i)]
    signal = np.ravel(raw.get_data(picks=configuration.EEG_CHANNEL_NAME))
    signal_filtered = filter_signal(signal, [0.5, 35], fs)*1e6
    
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

    for i in range(0, len(signal_filtered) - window_size, fs):
        n_epoch = int(i//(30*fs))+1
        
        if n_epoch==1:
            current_stage=' '
        elif n_epoch==2:
            current_stage='W'
        
        if i <= 30*fs:
            window_data = signal_filtered[:i]
            time_axis = np.arange(0, i) / fs 
        else:    
            window_data = signal_filtered[i - window_size:i]
            time_axis = np.arange(i - window_size, i) / fs 

        ax.cla()
        ax.set_facecolor('none')
        ax.plot(time_axis, window_data, color='yellow')
        ax.set_title('EEG', fontsize=14, color='white')
        ax.set_xlabel('Tiempo (s)', fontsize=12, color='white')
        ax.set_ylabel('Amplitud (μV)', fontsize=12, color='white')

        plot_placeholder.pyplot(fig)

        if n_epoch>2 and i%int(30*fs)==0:
            if n_epoch == 3:
                st.toast("Starting to detect sleep stages")
            start = i - window_size_scoring
            end = i + 1
            chunk_data = data_raw[:, int(start):int(end)]
            raw_chunk = mne.io.RawArray(chunk_data, raw.info)
            sls = yasa.SleepStaging(raw_chunk, eeg_name=configuration.EEG_CHANNEL_NAME, eog_name='EOG E1-M2', emg_name='EMG chin')
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
            ax_hypno.set_yticks([0, 1, 2, 3, 4])
            ax_hypno.set_yticklabels(['Wake', 'N1', 'N2', 'N3', 'REM']) #@TODO: Change it to be like an hypnogram
            
            hypno_placeholder.pyplot(fig_hypno)
            
            now = datetime.now()
            if n_epoch > 5:
                if now.time() > t_alpha and not 'N3' in SLEEP_STAGES[-5:]: # Before deadline time
                    st.write("Wake up!", datetime.now().strftime('%H:%M'))
                    playsound(configuration.ALARM_PATH)
                elif now.time() > t_omega: #WAKE UP - Deadline time
                    st.write("Wake up!", datetime.now().strftime('%H:%M'))
                    playsound(configuration.ALARM_PATH)
        
        stage_placeholder.write(f"**Epoch:** {n_epoch}")
        prevstage_placeholder.write(f":blue[**Previous sleep stage:** {current_stage}]")
        #time.sleep(0.01)

