"""Goldbach's conjecture: every even n > 2 is a sum of two primes.

For each even n we compute g(n) = the number of unordered prime pairs (p, q)
with p + q = n. Plotted as dots for each n, the picture looks like a comet —
the "Goldbach comet".

Unproven for 280 years, but it has been verified for every even number up to
about 4 * 10^18 by Oliveira e Silva. Here I check it for small n and also
look at the distribution of g(n).
"""


def sieve_bool(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    i = 2
    while i * i <= n:
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
        i += 1
    return is_prime


def goldbach_pairs(n, is_prime):
    """Count unordered prime pairs (p, q) with p + q = n, p <= q."""
    return sum(1 for p in range(2, n // 2 + 1)
               if is_prime[p] and is_prime[n - p])


def verify(limit, is_prime):
    """Check that every even n in [4, limit] has at least one Goldbach pair."""
    bad = []
    for n in range(4, limit + 1, 2):
        if goldbach_pairs(n, is_prime) == 0:
            bad.append(n)
    return bad


def ascii_comet(start, end, is_prime):
    print(f"Goldbach comet (n = {start} to {end}): each '.' is one prime pair\n")
    print(f"  {'n':>5} | {'g(n)':>4} | plot")
    for n in range(start, end + 1, 2):
        g = goldbach_pairs(n, is_prime)
        print(f"  {n:>5} | {g:>4} | {'.' * g}")


def distribution(limit, is_prime):
    values = []
    freq = {}
    for n in range(4, limit + 1, 2):
        g = goldbach_pairs(n, is_prime)
        values.append(g)
        freq[g] = freq.get(g, 0) + 1

    print(f"\nDistribution of g(n) for even n in [4, {limit}]:")
    scale = max(1, max(freq.values()) // 30)
    print(f"  {'g(n)':>5}  {'count':>5}")
    for g in sorted(freq):
        bar = "=" * (freq[g] // scale)
        print(f"  {g:>5}  {freq[g]:>5}  {bar}")

    print(f"\n  min = {min(values)}   max = {max(values)}   "
          f"mean = {sum(values)/len(values):.2f}")
    print("  g(n) grows with n — bigger even numbers have more ways to split.")


def main():
    N = 2_000
    is_prime = sieve_bool(N)

    bad = verify(N, is_prime)
    if bad:
        print(f"Counterexamples up to {N}: {bad[:10]}")
    else:
        print(f"Goldbach's conjecture verified for all even n in [4, {N}].")

    ascii_comet(4, 120, is_prime)
    distribution(N, is_prime)


if __name__ == "__main__":
    main()
