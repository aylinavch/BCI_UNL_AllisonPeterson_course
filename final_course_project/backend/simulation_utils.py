from matplotlib import pyplot as plt
import numpy as np
from scipy.signal import iirnotch, filtfilt, butter, sosfiltfilt

def filter_signal(signal, Wn, fs):
    b, a = iirnotch(50, 30, fs)
    signal_notch = filtfilt(b, a, signal)
    sos = butter(2**3, Wn, btype='bandpass', output='sos', fs=fs)
    return sosfiltfilt(sos, signal_notch)


# def plot_psg(signal, fs, plot_placeholder):
#     """
#     """
    
#     fs = int(fs)
#     window_duration = 30
#     window_size = int(window_duration * fs)

#     fig, ax = plt.subplots(figsize=(15, 5))
#     fig.patch.set_alpha(0)
#     plt.grid() 

#     ax.spines['top'].set_color('white')      # Top spine color
#     ax.spines['right'].set_color('white')    # Right spine color
#     ax.spines['left'].set_color('white')     # Left spine color
#     ax.spines['bottom'].set_color('white')    # Bottom spine color
#     ax.tick_params(axis='x', colors='white')  # Color de los ticks del eje X
#     ax.tick_params(axis='y', colors='white')  # Color de los ticks del eje Y

#     for i in range(0, len(signal) - window_size, fs):
#         window_data = signal[i:i + window_size]
#         time_axis = np.arange(i, i + window_size) / fs 

#         ax.cla()
#         ax.set_facecolor('none')
#         ax.plot(time_axis, window_data, color='yellow')
#         ax.set_title('C3', fontsize=14, color='white')
#         ax.set_xlabel('Tiempo (s)', fontsize=12, color='white')
#         ax.set_ylabel('Amplitud (uV)', fontsize=12, color='white')

#         plot_placeholder.pyplot(fig)

#         time.sleep(1)

#         if i%(30*fs):
#             stage_placeholder.write(f'')