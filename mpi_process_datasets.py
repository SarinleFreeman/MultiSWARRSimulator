import argparse
import glob
import json
import os

from mpi4py import MPI

from src.SingleInstance.User.CLI.handler import CLIHandler
from src.SingleInstance.Capacity.CapacityCalculations.STM.handler import STMCalcHandler
from src.Paths.Constructors.DynamicPathConstructor import DynamicPathConstructor


def process_dataset(default_args, base_dir):
    d_p_b = DynamicPathConstructor(default_args=default_args, number_of_signals=500,
                                   base_dir=base_dir)

    d_p_b.set_handlers(handlers=[
        STMCalcHandler(next_step=None),
    ])
    d_p_b.set_dirs()
    d_pth = d_p_b.build_path()
    # Take dynamic path
    d_pth.take_path(init_req={'TYPE': 'STM_CALC', 'ARGS': d_p_b.args})


# Set up command-line argument parsing
parser = argparse.ArgumentParser(description='Process datasets in a specified directory.')
parser.add_argument('base_data_parent_dir', type=str, help='Path to the parent directory containing the base data '
                                                           'directories.')

# Parse command-line arguments
args = parser.parse_args()

# Main loop
base_data_parent_dir = os.path.join(os.getcwd(), args.base_data_parent_dir)

# Find all directories in the base_data_parent_dir
all_dirs = [d for d in glob.glob(os.path.join(base_data_parent_dir, '*')) if os.path.isdir(d)]

# MPI setup
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Divide the directories among MPI processes
dirs_per_process = len(all_dirs) // size
start_index = rank * dirs_per_process
end_index = (rank + 1) * dirs_per_process if rank != size - 1 else len(all_dirs)

# Process assigned directories
for count, dir_path in enumerate(all_dirs[start_index:end_index], start=start_index):
    print(f"[Process {rank}] On {dir_path}")
    print(f"[Process {rank}] {count + 1}/{len(all_dirs)}")
    args_file_path = os.path.join(dir_path, 'args')

    # Check if the args file exists in the directory
    if os.path.isfile(args_file_path):
        # Read the args file and load the default args as a dictionary
        with open(args_file_path, 'r') as args_file:
            new_default_args = json.load(args_file)

        # Run the algorithm with the new default args and the base directory path
        process_dataset(new_default_args, dir_path)
