#!/bin/bash -l
#SBATCH --account=pawsey0841
#SBATCH --partition=debug
#SBATCH --job-name=test_run
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=00:40:00
#SBATCH --output=output_test.log


module load python/3.9.15
module load py-setuptools/57.4.0-py3.9.15
module load py-scikit-learn/1.0.1

module load py-pip/22.2.2-py3.9.15

export PYTHONPATH=/software/projects/pawsey0841/setonix/python/lib/python3.9.15/site-pa>

export OMP_NUM_THREADS=1
export MPICH_OFI_STARTUP_CONNECT=1
export MPICH_OFI_VERBOSE=1

srun -N 1 -n 1 -c 1 python simulate.py



