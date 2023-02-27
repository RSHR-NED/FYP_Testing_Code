# combine all json file into one
import json
merge_data= {
    "mapping": [],
    "labels": [],
    "MFCCs": [],
}
for filename in ["data_a1.json", "data_a2.json", "data_a3.json", "data_a4.json", "data_a5.json", "data_a6.json", "data_a7.json", "data_a8.json"]:
    with open() as file:
        data = json.load(file)
        # Merge the data into the dictionary
        merge_data["mapping"] += data["mapping"]
        merge_data["labels"] += data["labels"]
        merge_data["MFCCs"] += data["MFCCs"]

# Write the merged data to a new file
with open("data_surah_1.json", "w") as file:
    json.dump(merge_data, file, indent=4)