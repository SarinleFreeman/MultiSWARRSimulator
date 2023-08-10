#!/bin/bash -l
#SBATCH --account=pawsey0841
#SBATCH --partition=debug
#SBATCH --job-name=test_run
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time 00:05:00
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

srun -N 2 -n 2 python main.py --theta_int_range 5e-8,5e-8,1,8 --film_thickness_range 5e-6,5e-6,1,6


end_time=$(date +%s)
elapsed_time=$((end_time - start_time))
echo "The simulation took ${elapsed_time} seconds to run."

