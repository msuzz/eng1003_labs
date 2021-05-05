"""
Implementation of the Sieve of Eratosthenes algorithm, as a function
"""

import numpy as np


def prime_generate(n):
    isPrime = np.ones(n+1, dtype=np.byte)
    isPrime[0] = 0      # 0 is not a prime number
    isPrime[1] = 0      # 1 is not a prime number
    i = 2
    while i**2 <= n:
        if isPrime[i]:
            for j in range(i*2, n+1, i):
                isPrime[j] = 0  # Unset primeness of multiples
        i += 1

    primes = []
    for i in range(n+1):
        if isPrime[i]:
            primes.append(i)

    return primes


poop = prime_generate(100)
print(poop)
