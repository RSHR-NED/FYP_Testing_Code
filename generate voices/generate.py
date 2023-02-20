import os
import numpy as np
import soundfile as sf
import pyworld as pw
import time

start_time = time.time()

# Define the factors to adjust the voice
pitch_factors = np.linspace(0.5, 2, 3)
timbre_factors = np.linspace(0.2, 2, 3)
resonance_factors = np.linspace(0.3, 2, 3)

# Create the directory for the processed voices
if not os.path.exists('001_augmented'):
    os.makedirs('001_augmented')

# Loop over all the voice files in the '001' folder
for ayat_count in os.listdir('001'):
    for word_count in os.listdir(os.path.join('001', ayat_count)):
        print(f"Starting Processing ayat {ayat_count} word {word_count}")

        # find the largest audio file name (number in format 001.wav, 002.wav, etc.)
        largest = 0
        for current_file in os.listdir(os.path.join('001', ayat_count, word_count)):
            filename = os.path.splitext(current_file)[0]
            if int(filename) > largest:
                largest = int(filename)

        new_file = largest + 1  # the next file to be created

        for current_file in os.listdir(os.path.join('001', ayat_count, word_count)):
            # Load the voice file
            x, sr = sf.read(os.path.join('001', ayat_count, word_count, current_file))

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
                        
                        # Save the processed voice file to the '001_augmented' folder
                        new_file_name = str(new_file).zfill(3)  # create new file name with 0 padding
                        sf.write(os.path.join('001_augmented', ayat_count, word_count, f'{new_file_name}.wav'), y, sr)
                        new_file += 1
            print(f"Done processing audio file {current_file}")

        print(f"Done processing all audio files of ayat {ayat_count} word {word_count}\n")
    print(f"Done processing all audio files of ayat {ayat_count}\n\n\n")

print(f"Done processing all audio files")
print(f"Total time taken: {time.time() - start_time} seconds")
