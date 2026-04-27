"""Prime distribution: sieve, prime counting function, gaps, twin primes, Bertrand."""

import math


def sieve(n):
    """Sieve of Eratosthenes — returns the list of primes up to n (inclusive)."""
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    i = 2
    while i * i <= n:
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
        i += 1
    return [p for p in range(2, n + 1) if is_prime[p]]


def count_up_to(primes, x):
    """Binary search for pi(x) = number of primes <= x."""
    lo, hi = 0, len(primes)
    while lo < hi:
        mid = (lo + hi) // 2
        if primes[mid] <= x:
            lo = mid + 1
        else:
            hi = mid
    return lo


def prime_number_theorem(primes):
    print("Prime Number Theorem: pi(x) / (x / ln x) should approach 1\n")
    print(f"  {'x':>10}  {'pi(x)':>8}  {'x/lnx':>10}  {'ratio':>8}")
    for x in [1_000, 10_000, 100_000, 1_000_000]:
        pi_x = count_up_to(primes, x)
        approx = x / math.log(x)
        print(f"  {x:>10,}  {pi_x:>8,}  {approx:>10.1f}  {pi_x/approx:>8.4f}")


def prime_gaps(primes, first=10_000):
    gaps = {}
    for i in range(1, min(len(primes), first + 1)):
        g = primes[i] - primes[i - 1]
        gaps[g] = gaps.get(g, 0) + 1

    print(f"\nPrime gap frequency among first {first} consecutive pairs (gaps <= 36):")
    print(f"  {'gap':>5}  {'count':>6}")
    for g in sorted(gaps):
        if g > 36:
            break
        bar = "#" * (gaps[g] // 60)
        print(f"  {g:>5}  {gaps[g]:>6}  {bar}")


def twin_primes(primes, limit):
    prime_set = set(primes)
    return [(p, p + 2) for p in primes if p <= limit and (p + 2) in prime_set]


def bertrand_postulate(primes):
    """For every n >= 1 there is a prime in (n, 2n). Count how many."""
    print("\nBertrand's postulate: always a prime in (n, 2n)")
    for n in [5, 10, 25, 100, 500, 1_000, 5_000, 10_000]:
        cnt = count_up_to(primes, 2 * n) - count_up_to(primes, n)
        print(f"  n = {n:>6}   primes in ({n}, {2*n}): {cnt}")


def main():
    N = 1_000_000
    print(f"Sieving primes up to {N:,}...\n")
    primes = sieve(N)
    print(f"Found {len(primes):,} primes.\n")

    prime_number_theorem(primes)
    prime_gaps(primes, first=10_000)

    twins = twin_primes(primes, N)
    print(f"\nTwin primes up to {N:,}: {len(twins):,} pairs")
    print(f"First eight: {twins[:8]}")

    bertrand_postulate(primes)


if __name__ == "__main__":
    main()
