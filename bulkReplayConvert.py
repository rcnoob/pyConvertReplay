import argparse
import os
import json

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", type=str,
	help="input json folder")
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

def process_json(input_folder):
    output_folder = os.path.join(os.getcwd(), "output")

    for root, _, files in os.walk(input_folder):
        for filename in files:
            if filename.endswith('.json'):
                input_path = os.path.join(root, filename)

                relative_path = os.path.relpath(input_path, input_folder)
                output_path = os.path.join(output_folder, relative_path)
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                with open(input_path, 'r') as infile:
                    try:
                        data = json.load(infile)
                    except json.JSONDecodeError as e:
                        print(f"Error reading JSON from {input_path}: {e}")
                        continue

                if any("PositionString" in frame.get("Frame", {}) for frame in data):
                    converted_data = convert_strings_to_xyz(data)

                    with open(output_path, 'w') as outfile:
                        json.dump(converted_data, outfile, separators=(',', ':'))

                    print(f"Converted {input_path} and saved to {output_path}")
                else:
                    print(f"Skipping {input_path}: Already in new format.")

os.makedirs("output")
process_json(args["input"])