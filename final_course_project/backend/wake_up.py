#This should have the logic of the aparatus
#It will take the hour the person want to wake up and the stage they are,
# and then wake them up

import mne
from datetime import datetime
from playsound import playsound
import numpy as np
import yasa

def classif_chunk(chunk_data,raw_info):
    raw_chunk = mne.io.RawArray(chunk_data, raw_info)
    sls = yasa.SleepStaging(raw_chunk, eeg_name='EEG C4-M1', eog_name='EOG E1-M2', emg_name='EMG chin')
    hypno = sls.predict()
    
    return hypno[-1]

def collect_chunks(data, fs, raw_info):
    SLEEP_STAGES = ['W']
    signal = data[1]*1e6
    fs = int(fs)
    window_duration = 30
    window_size = int(window_duration * fs)
    window_size_scoring = int(window_duration * fs * 2)
    for i in range(0, len(signal) - window_size, fs):
        start = i - window_size_scoring
        end = i + 1
        chunk_data = data[:, int(start):int(end)]
        current_stage = classif_chunk(chunk_data,raw_info)
        SLEEP_STAGES.append(current_stage)
    
    return SLEEP_STAGES
    
def alarm_on(wake_up_time,SLEEP_STAGES):
    if datetime.now() > wake_up_time:
        if not any(SLEEP_STAGES[-6:]=='N3'):
            print("Wake up!", datetime.now().strftime('%H:%M:%S'))
            playsound('final_course_project\data\alarm_sound.mp3')
    
    return 0