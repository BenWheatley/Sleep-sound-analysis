#!python3

import numpy as np
from scipy.io import wavfile

output = wavfile.read('processed.wav')
samplerate, data = output

# Determine if audio is mono or stereo
if len(data.shape) == 1:  # mono
    channels = 1
else:  # stereo
    channels = data.shape[1]

duration_seconds = data.shape[0] / samplerate

# Parameters for loudness detection
window_size = int(samplerate * 0.1)  # 100ms windows
threshold = 16  # Threshold for loudness, adjust as necessary

# Function to compute RMS
def rms(signal, timestamp):
    return np.sqrt(np.mean(signal**2))

# Find loud parts
loud_parts = []

for start in range(0, len(data), window_size):
    end = start + window_size
    window = data[start:end]

    if channels == 2:  # If stereo, average the channels
        window = window.mean(axis=1)
    
    if rms(window, timestamp) > threshold:
        timestamp = start / samplerate
        loud_parts.append(timestamp)

# Print timestamps of loud parts
for timestamp in loud_parts:
    print(f"Loud part at {timestamp:.2f} seconds")
