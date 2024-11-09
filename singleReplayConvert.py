import argparse
import json
import os

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", type=str,
	help="input json filename")
args = vars(ap.parse_args())

def convert_strings_to_xyz(data):
    for entry in data:
        frame = entry["Frame"]
        
        pos_values = list(map(float, frame["PositionString"].split()))
        frame["Position"] = {"X": pos_values[0], "Y": pos_values[1], "Z": pos_values[2]}
        
        rot_values = list(map(float, frame["RotationString"].split()))
        frame["Rotation"] = {"Pitch": rot_values[0], "Yaw": rot_values[1], "Roll": rot_values[2]}
        
        speed_values = list(map(float, frame["SpeedString"].split()))
        frame["Speed"] = {"X": speed_values[0], "Y": speed_values[1], "Z": speed_values[2]}
        
        del frame["PositionString"]
        del frame["RotationString"]
        del frame["SpeedString"]
    
    return data

with open(args["input"], 'r') as infile:
    data = json.load(infile)

converted_data = convert_strings_to_xyz(data)

os.makedirs("output", exist_ok=True)
path = os.path.join("output", args["input"])
with open(path, 'w') as outfile:
    json.dump(converted_data, outfile, separators=(',', ':'))

print("Conversion complete")