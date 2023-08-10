import random


class BinaryWave:

    def __init__(self, init_val, mapping=(1, 1.2)):
        self.current_val = init_val
        self.mapping = mapping
        self.stored_values = [init_val]

    def switch_bin_val(self):
        self.current_val = self.mapping[1]
        #num = random.randint(0,1)
        #self.current_val = self._binarize(num)


    def store_current(self):
        self.stored_values.append(self.current_val)

    def empty_binary(self):
        self.stored_values = []

    def get_current(self):
        return self.current_val

    def get_stored(self):
        return self.stored_values

    def _binarize(self, a):
        if a == 0:
            return self.mapping[0]
        elif a == 1:
            return self.mapping[1]
