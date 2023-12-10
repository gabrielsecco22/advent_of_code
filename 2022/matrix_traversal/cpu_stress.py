import numpy as np
import multiprocessing as mp

def stress_test(core_num):
    s = 0
    for i in range(10000000000):
        s = s + i
    print(f"Core {core_num} finished.")


if __name__ == "__main__":
    # Create a pool of 4 processes.
    pool = mp.Pool(16)
    # Run the stress test on all 4 cores.
    pool.map(stress_test, range(4))
    # Close the pool.
    pool.close()
    # Join the pool.
    pool.join()
