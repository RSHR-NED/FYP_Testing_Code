import os
import numpy as np
import soundfile as sf
import pyworld as pw

# Define the factors to adjust the voice
pitch_factors = np.linspace(0.5, 2, 3)
timbre_factors = np.linspace(0.2, 2, 3)
resonance_factors = np.linspace(0.3, 2, 3)

# Create the directory for the processed voices
if not os.path.exists('processedVoices'):
    os.makedirs('processedVoices')

# Loop over all the voice files in the 'voices' folder
for file in os.listdir('voices'):
    # Load the voice file
    x, sr = sf.read(os.path.join('voices', file))
    
    # Check if the audio file has multiple channels and convert to mono if necessary
    if x.ndim > 1:
        x = np.mean(x, axis=1)
    
    # Extract the fundamental frequency and spectral envelope using PyWorld
    f0, sp, ap = pw.wav2world(x, sr)
    
    # Loop over all combinations of the pitch, timbre, and resonance factors
    for pitch_factor in pitch_factors:
        for timbre_factor in timbre_factors:
            for resonance_factor in resonance_factors:
                # Adjust the fundamental frequency, spectral envelope, and aperiodicity
                f0_shifted = f0 * pitch_factor
                sp_scaled = sp * timbre_factor
                ap_scaled = ap * resonance_factor
                
                # Synthesize the adjusted voice using PyWorld
                y = pw.synthesize(f0_shifted, sp_scaled, ap_scaled, sr)
                
                # Save the processed voice file to the 'processedVoices' folder
                filename = os.path.splitext(file)[0]
                processed_filename = f'{filename}_p{pitch_factor:.1f}_t{timbre_factor:.1f}_r{resonance_factor:.1f}.wav'
                sf.write(os.path.join('processedVoices', processed_filename), y, sr)
