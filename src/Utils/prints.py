from simple_chalk import chalk



def warning(string):
    return chalk.red.bold("Warning: {}".format(string))


def input_prepend(string):
    return chalk.yellow('Input: {}'.format(string))


def success(string, prepend=None):
    if prepend is None:
        return chalk.green('{}'.format(string))
    return chalk.green('{}: {}'.format(string, prepend))


def sprint(*args, **kwargs):
    print(success(" ".join(map(str, args)), **kwargs))


def wprint(*args, **kwargs):
    print(warning(" ".join(map(str, args)), **kwargs))


def purprint(*args, **kwargs):
    print(chalk.magenta.bold("XXX" + " ".join(map(str, args)) + "XXX", **kwargs))
