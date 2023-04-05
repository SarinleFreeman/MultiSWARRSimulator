#!/bin/bash -l
#SBATCH --account=pawsey0841
#SBATCH --partition=work
#SBATCH --job-name=ant_change_run
#SBATCH --ntasks=2560
#SBATCH --ntasks-per-node=128
#SBATCH --cpus-per-task=1
#SBATCH --time 24:00:00
#SBATCH --output=output_test.log
#SBATCH --exclusive

# Install relevant packages

module load python/3.9.15
module load py-setuptools/57.4.0-py3.9.15
module load py-matplotlib/3.4.3
module load py-mpi4py/3.1.2-py3.9.15
module load py-numpy/1.20.3
module load py-scikit-learn/1.0.1
module load py-pandas/1.3.4
module load py-pip/22.2.2-py3.9.15
module load py-scipy/1.7.1

pip install simple_chalk
pip install joblib
pip install psutil

# Use new path

export PYTHONPATH=/software/projects/pawsey0841/setonix/python/lib/python3.9.15/site-packages:$PYTHONPATH

# Set environment variables
export OMP_NUM_THREADS=1
export MPICH_OFI_STARTUP_CONNECT=1
export MPICH_OFI_VERBOSE=1


start_time=$(date +%s)

# Loop over theta_int values
for theta_int in $(seq 1e-8 1e-9 10e-8); do
  echo "Running simulation with theta_int = $theta_int"

  # Run the simulation and store data in simulation_data
  srun -N 20 -n 2560 -c 1 python simulate.py --theta_int $theta_int

  # Generate capacities for each dataset.
  srun -N 20 -n 2560 -c 1 python mpi_process_datasets.py "simulation_data"

  # Move the capcities and relevant files to a new directory
  srun -N 1 -n 1 -c 1 python mv_cpc.py simulation_data cpc_dir --file args 'stm_corr_data_path '  'stm_reconstruct'

  # Remove simulation_data for storage purposes
  rm -rf simulation_data/*

done


end_time=$(date +%s)
elapsed_time=$((end_time - start_time))

echo "The simulation took ${elapsed_time} seconds to run."
