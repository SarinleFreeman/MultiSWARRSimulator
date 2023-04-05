import os
import json
import pandas as pd
import argparse
from mpi4py import MPI
import math

# Initialize MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Argument parsing for the parent folder path
parser = argparse.ArgumentParser(description="Process the parent folder path.")
parser.add_argument("parent_folder", type=str, help="Path to the parent folder")
args = parser.parse_args()

parent_folder = os.path.join(os.getcwd(),args.parent_folder)

folders = [os.path.join(parent_folder, f) for f in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder, f))]
print(folders)
# Divide the folders among the available processes
folders_per_process = int(math.ceil(len(folders) / float(size)))
start = rank * folders_per_process
end = min(start + folders_per_process, len(folders))
folders_to_process = folders[start:end]

data = []

for folder in folders_to_process:
    # Read args file
    with open(os.path.join(folder, "args"), "r") as f:
        folder_args = json.load(f)

    # Read stm_corr_data_path file
    with open(os.path.join(folder, "stm_corr_data_path "), "r") as f:
        stm_corr_data = json.load(f)

    # Calculate STM value
    STM = sum(stm_corr_data)

    # Store the args and STM in a dictionary and append to the data list
    folder_args["STM"] = STM
    data.append(folder_args)

# Gather the data from all processes
combined_data = comm.gather(data, root=0)

if rank == 0:
    # Flatten the gathered data
    combined_data_flat = [item for sublist in combined_data for item in sublist]

    # Create a pandas DataFrame from the data list
    df = pd.DataFrame(combined_data_flat)
    print(df)

    # Save the DataFrame to a CSV file
    df.to_csv("combined_data.csv", index=False)
