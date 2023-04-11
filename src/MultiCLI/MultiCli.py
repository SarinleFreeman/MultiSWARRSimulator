import argparse
from typing import List, Any

from simple_chalk import chalk


def namespace_to_dict(namespace: argparse.Namespace) -> dict:
    return {
        k: namespace_to_dict(v) if isinstance(v, argparse.Namespace) else v
        for k, v in vars(namespace).items()
        if v is not None
    }


class MultiCLI:
    def __init__(self: 'MultiCLI', defaults: dict) -> None:
        self.defaults = defaults
        self.args = None

        self.parser = argparse.ArgumentParser(
            prog='main',
            description=print(chalk.blue.bold(
                'Welcome to the Multi-Dimensional Spin Wave Simulator. The program has a corresponding manual located '
                'at'
                'X explaining how to utilize the system effectively.'
                'I advise you to read said manual before use.\n '
            )),
        )

    def parse_user_inputs(self: 'MultiCLI') -> None:

        # Add default key arguments to parser
        for key in self.defaults.keys():
            key_range = f"{key}_range"
            key_shrt = "_".join([k[:2] for k in key_range.split('_')])
            self.parser.add_argument(f'--{key_range}', f'-{key_shrt}', help=chalk.blue(
                f"This parameter is used to specify the range and the number of points for the {key} variable in the "
                "format min,max,num_points,rounding_factor."),
                                     type=str,
                                     default=None)

        args = self.parser.parse_args()

        # Parse the arguments
        for key in self.defaults.keys():
            key_range = f"{key}_range"
            arg_value = getattr(args, key_range)
            if arg_value:
                # Split the argument into a list and check if it is in the correct format
                arg_range = arg_value.split(',')
                if len(arg_range) == 4:
                    min_val = float(arg_range[0])
                    max_val = float(arg_range[1])
                    num_points = int(arg_range[2])
                    rounding_factor = int(arg_range[3])

                    setattr(args, key_range, {'min': min_val, 'max': max_val, 'num_points': num_points,
                                              'rounding_factor': rounding_factor})
                else:
                    raise ValueError(
                        f"Invalid format for --{key_range}. It should be in the format min,max,num_points,rounder")

        self.args = args

    def get_parsed_inputs(self: 'MultiCLI') -> List[List[Any]]:
        parsed_args = namespace_to_dict(self.args)

        # Reform the parsed arguments for use in the ParamGenerator.

        return [[dim[0], dim[1].get('min'), dim[1].get('max'), dim[1].get('num_points'), dim[1].get('rounding_factor')]
                for dim in parsed_args.items() if dim[0].replace("_range", "") in self.defaults.keys()]
