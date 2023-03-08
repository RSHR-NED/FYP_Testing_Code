import librosa
import os
import json
import numpy as np

DATASET_PATH = "./001_augmented/008"
SAMPLES_TO_CONSIDER = 22050 # 1 sec. of audio

# dictionary where we'll store mapping, labels, MFCCs and filenames
data = {
    "mapping": [],
    "labels": [],
    "MFCCs": [],
    "files": []
}
# a dict of mapping

_mapping = {
    1:"Bis'mi",
    2:"Al-lahi",
    3:"Al-rahmaani",
    4:"Al-raheemi",
    5:"Alhamdu",
    6:"lillaahi",
    7:"Rabbil",
    8:"aalameen",
    9:"Ar-Rahmaan",
    10:"Ar-Raheem",
    11:"Maaliki",
    12:"Yumid",
    13:"Diin",
    14:"Iyyaka",
    15:"Na'abudu",
    16:"Iyyaka",
    17:"Nasta'een",
    18:"Ihdinas",
    19:"Siraatal",
    20:"Mustaqeem",
    21:"Siraatal",
    22:"Ladheena",
    23:"An'amta",
    24:"Alaihim",
    25:"Ghayril",
    26:"Maghdubi",
    27:"Alaihim",
    28:"Wala al-dalina"
}

n_fft = 2048
hop_length = 512
def preprocess_dataset(data, dataset_path, json_path, num_mfcc=13, n_fft=2048, hop_length=512):
    """Extracts MFCCs from music dataset and saves them into a json file.
    :param dataset_path (str): Path to dataset
    :param json_path (str): Path to json file used to save MFCCs
    :param num_mfcc (int): Number of coefficients to extract
    :param n_fft (int): Interval we consider to apply FFT. Measured in # of samples
    :param hop_length (int): Sliding window for FFT. Measured in # of samples
    :return:
    """

    # loop through all sub-dirs
    for i, (dirpath, dirnames, filenames) in enumerate(os.walk(dataset_path)):

        # ensure we're at sub-folder level
        if dirpath is not dataset_path:

            # save label (i.e., sub-folder name) in the mapping
            label = dirpath[-2:]
            label = int(label)
            print("label",label)
            data["mapping"].append(_mapping[label])

            # process all audio files in sub-dir and store MFCCs
            for f in filenames:
                file_path = os.path.join(dirpath, f)

                # load audio file and slice it to ensure length consistency among different files
                audio, sample_rate = librosa.load(file_path, res_type='kaiser_fast') 

                # Compute spectrogram
                spec = librosa.stft(audio, n_fft=n_fft, hop_length=hop_length)

                # Convert to power spectrogram
                spec_power = librosa.power_to_db(np.abs(spec)**2, ref=np.max)

                mfccs_features = librosa.feature.mfcc(S=spec_power, n_mfcc=13)
                mfccs_scaled_features = np.mean(mfccs_features.T,axis=0)
                mffccs = mfccs_scaled_features.tolist()

               
                data["MFCCs"].append(mffccs)
                # data["labels"].append(i-1)
                data["labels"].append(label)
                data["files"].append(file_path)
                print("{}: {}".format(file_path, i-1))

    # save data in json file
    with open(json_path, "w") as fp:
        json.dump(data, fp, indent=4)

# JSON_PATH = "data8.json"
# if __name__ == "__main__":
#     preprocess_dataset(data, DATASET_PATH, JSON_PATH)

'''Combine json files'''
merged_data = {
    "mapping": [],
    "labels": [],
    "MFCCs": [],
    }

# Loop through each JSON file
for filename in ["data1.json", "data2.json", "data3.json", "data4.json", "data5.json", "data6.json", "data7.json", "data8.json"]:
    with open(filename) as file:
        data = json.load(file)
        # Merge the data into the dictionary
        merged_data["mapping"] += data["mapping"]
        merged_data["labels"] += data["labels"]
        merged_data["MFCCs"] += data["MFCCs"]

# Write the merged data to a new file
with open("data_spect_mfcc.json", "w") as file:
    json.dump(merged_data, file)