#!/bin/bash -l
#SBATCH --account=pawsey0841
#SBATCH --partition=debug
#SBATCH --job-name=test_run
#SBATCH --ntasks=512
#SBATCH --ntasks-per-node=128
#SBATCH --cpus-per-task=1
#SBATCH --time=00:1:00
#SBATCH --output=output_test.log
#SBATCH --exclusive

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

export PYTHONPATH=/software/projects/pawsey0841/setonix/python/lib/python3.9.15/site-packages:$PYTHONPATH

export OMP_NUM_THREADS=1
export MPICH_OFI_STARTUP_CONNECT=1
export MPICH_OFI_VERBOSE=1

srun -N 4 -n 512 -c 1 python mpi_process_datasets.py "simulation_data"
