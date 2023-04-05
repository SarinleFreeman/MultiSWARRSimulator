import os
import time
from simulate import run_simulation
from mpi_process_datasets import process_datasets
from mv_cpc import move_cpc_files

# Set the theta_int range
theta_int_range = [(x * 1e-9) for x in range(1, 11)]

# Iterate over theta_int values
start_time = time.time()
for theta_int in theta_int_range:
    print(f"Running simulation with theta_int = {theta_int}")

    # Run the simulation and store data in simulation_data
    run_simulation(theta_int)

    # Generate capacities for each dataset
    process_datasets("simulation_data")

    # Move the capacities and relevant files to a new directory
    move_cpc_files("simulation_data", "cpc_dir", files=['args', 'stm_corr_data_path', 'stm_reconstruct'])

    # Remove simulation_data for storage purposes
    for item in os.listdir("simulation_data"):
        item_path = os.path.join("simulation_data", item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)

end_time = time.time()
elapsed_time = end_time - start_time
print(f"The simulation took {elapsed_time} seconds to run.")