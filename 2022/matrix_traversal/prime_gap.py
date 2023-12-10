from timeit import timeit

def primes_sieve(limit):
    # Initialize a boolean array indicating whether each number is prime
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False

    # Mark multiples of each prime number as composite
    for i in range(2, int(limit ** 0.5) + 1):
        if is_prime[i]:
            for j in range(i**2, limit + 1, i):
                is_prime[j] = False

    # Return a list of all prime numbers

    l = [i for i in range(limit + 1) if is_prime[i]]
    print(len(l))
    return l


def bench(n):
    primes = primes_sieve(2**n)
    max_gap = 0

    p1 = 2
    p2 = 3

    for i in range(len(primes) - 1):
        gap = primes[i+1] - primes[i]
        if gap > max_gap:
            max_gap = gap
            p1, p2 = primes[i], primes[i+1]

    print(f"The biggest prime number gap between 1 and 2^{n} is {p2}-{p1}:", max_gap)


if __name__ == "__main__":
    # for i in range(2, 30):
    #     t = timeit(lambda : bench(i), number=1)
    #     print(f"Time taken: {t:.2f} seconds")

    for i in range(2, 30):
        t = timeit(lambda : primes_sieve(2**i), number=1)
        print(f"Time taken: {t:.2f} seconds for 2^{i}")