#!/usr/bin/python3
import numpy as np

block_size = 5

input_sequence = np.random.randint(1,10,23)
print(input_sequence)


def block_gen(sequence):
    block = []
    for item in sequence:
        block.append(item)
        if len(block) >= 5:
            yield block
            block = []
    yield block

blocks = block_gen(input_sequence)

for block in blocks:
    print( block)
