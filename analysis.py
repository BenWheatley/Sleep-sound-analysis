#!python3

import math
import warnings
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

output = wavfile.read('processed.wav')
samplerate, data = output

# Determine if audio is mono or stereo
if len(data.shape) == 1:  # mono
    channels = 1
else:  # stereo
    channels = data.shape[1]

duration_seconds = data.shape[0] / samplerate

# Parameters for loudness detection
window_seconds = 0.1
window_size = int(samplerate * window_seconds)
threshold = 64  # Threshold for loudness, adjust as necessary
graph = []

# Function to compute RMS
def rms(signal, timestamp):
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always", RuntimeWarning)  # Catch all RuntimeWarnings
        rms_value = np.sqrt(np.mean(signal**2))
        
        if w and issubclass(w[-1].category, RuntimeWarning):
            print(f"RuntimeWarning at timestamp {timestamp:.2f} seconds")
            return 0
    
    return rms_value

# Find loud parts
loud_parts = []

for start in range(0, len(data), window_size):
    end = start + window_size
    window = data[start:end]

    if channels == 2:  # If stereo, average the channels
        window = window.mean(axis=1)
    
    loudness = rms(window, start)
    if loudness == 0:
        graph.append(None)
    else:
        graph.append( math.log2(loudness) )
    
    if loudness > threshold:
        timestamp = start / samplerate
        loud_parts.append(timestamp)

# Print timestamps of loud parts
for timestamp in loud_parts:
    print(f"Loud part at {timestamp:.2f} seconds")

plt.plot(graph, linestyle='None', marker='.', markersize=1)
plt.title('Graph of log2 loudness')
plt.xlabel(f'time index ({window_seconds:.2f}s)')
plt.ylabel('log2(value)')
plt.grid(True)
plt.show()