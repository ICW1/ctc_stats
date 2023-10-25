import pandas as pd
import numpy as np

from itertools import product


def run_sense_check():
    ''' Get the counts of 3s in the corner and counts of all possible combinations, and the probability '''
    # Create an array containing the digits 1 to 9
    digits = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])

    # Generate all length-4 permutations of the digits using itertools
    perms = list(product(digits, repeat=4))

    # Convert the permutations into a Pandas DataFrame
    df = pd.DataFrame(perms, columns=['a', 'b', 'c', 'd'])

    # Filter out rows where a == b, a == c, b == d, c == d. (typical Sudoku constraints)
    df = df.loc[
        (df['a'] != df['b']) & \
        (df['a'] != df['c']) & \
        (df['b'] != df['d']) & \
        (df['c'] != df['d'])
    ]

    # Get the numbers we want
    N_all = df.shape[0]
    N_titcs = (df == 3).all(axis=1).sum()

    return N_all, N_titcs, N_titcs/N_all


if __name__ == "__main__":
    N_all, N_titcs, prob = run_sense_check()
    print(f"Number of all possible combinations: {N_all}")
    print(f"Number of combinations with 3s in the corner: {N_titcs}")
    print(f"Probability of 3s in the corner: {prob}")