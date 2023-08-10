import json
import logging
import os
from copy import copy


def create_dir(path: str) -> None:

    if os.path.exists(path):
        print(f'Path {path} already exists, ignoring request')
    else:
        os.mkdir(path)


def store_args(path: str, args: dict) -> None:
    copied_args = copy(args)
    copied_args['wave_numbers'] = []
    stored_args = json.dumps(copied_args, indent=4)

    with open(path, "w") as outfile:
        outfile.write(stored_args)
