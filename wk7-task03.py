"""
Implementation of the Sieve of Eratosthenes algorithm, as a function
TODO: Make 
"""

import numpy as np


def prime_generate(n):
    n += 1              # Increase n by one, so n is in output
    isPrime = np.ones(n, dtype=np.byte)
    isPrime[0] = 0      # 0 is not a prime number
    isPrime[1] = 0      # 1 is not a prime number
    primes = []         # Array of primes to be returned
    for i in range(2,n):
        if isPrime[i] == 1:
            primes.append(i)  # Add to our list
            for j in range(i+1,n):
                if np.remainder(j, i) == 0 and i*j < n:
                    isPrime[i*j] = 0  # Unset primeness of multiples
    return primes


poop = prime_generate(100)
print(poop)
