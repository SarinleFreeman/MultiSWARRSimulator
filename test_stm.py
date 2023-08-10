import os
import json
from mpi4py import MPI
from copy import copy
from src.Paths.Constructors.DynamicPathConstructor import DynamicPathConstructor
from src.SingleInstance.Capacity.CapacityCalculations.PC.handler import PCCalcHandler
from src.SingleInstance.Capacity.CapacityCalculations.STM.handler import STMCalcHandler
from src.SingleInstance.Capacity.DirCreator.handler import CPCDirCreator


def calc_for_dir(dir_name):
    # Read args file
    with open(os.path.join(base_dir, dir_name, "args"), "r") as args_file:
        args_data = json.load(args_file)

    d_args = copy(args_data)  # Make a copy of args_data to avoid overwriting

    p_c = DynamicPathConstructor(default_args=copy(d_args), number_of_signals=100,
                                 base_dir=d_args['sim_dir'], inst_name=d_args['identifier'],
                                 handlers=[STMCalcHandler(next_step='PC_CALC'),
                                           PCCalcHandler(next_step=None)])

    d_pth = p_c.build_path()
    d_pth.take_path(init_req={'TYPE': 'STM_CALC', 'ARGS': p_c.args})


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

base_dir = os.path.join(os.getcwd(), 'temp1')
dir_list = [dir_name for dir_name in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, dir_name))]

for i in range(rank, len(dir_list), size):
    calc_for_dir(dir_list[i])
