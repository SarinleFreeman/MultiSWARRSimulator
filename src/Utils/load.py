import pickle
import numpy as np


def internal_load(filename):
    with open(filename, "rb") as f:
        while True:
            try:
                yield pickle.load(f)
            except EOFError:
                break
            except Exception as e:
                print("An error occurred while loading the data:")
                print(str(e))
                break


def loadall(filename):
    try:
        data = np.asarray([i for i in internal_load(filename)])
        return np.asarray(data)
    except Exception as e:
        print("An error occurred while processing the data:")
        print(str(e))


def load_latest(filename):
    try:
        latest_values = None
        for i in internal_load(filename):
            latest_values = i

        if latest_values is not None:
            return np.asarray(latest_values)
        else:
            return None, None, 0
    except Exception as e:
        print("An error occurred while processing the data:")
        print(str(e))
