"""Three ways to approach Euler's number e.

1. Random sum:      keep adding U(0,1) until the sum passes 1; E[steps] = e.
2. Derangements:    fraction of permutations of n with no fixed point -> 1/e.
3. Taylor series:   e = sum 1/k! — deterministic, converges exponentially fast.

Monte Carlo methods 1 and 2 are interesting *because* they give a meaning to e
beyond "the base of natural log". Taylor wins on accuracy, but it doesn't
tell you anything about WHY e is there.
"""

import math
import random


def random_sum_estimate(trials):
    total = 0
    for _ in range(trials):
        s, n = 0.0, 0
        while s <= 1.0:
            s += random.random()
            n += 1
        total += n
    return total / trials


def derangement_estimate(n_elements, trials):
    original = list(range(n_elements))
    no_fixed_point = 0
    for _ in range(trials):
        perm = original.copy()
        random.shuffle(perm)
        if all(perm[i] != i for i in range(n_elements)):
            no_fixed_point += 1
    p = no_fixed_point / trials
    return 1.0 / p if p > 0 else float("inf")


def taylor_series(terms):
    s = 0.0
    factorial = 1
    for k in range(terms):
        if k > 0:
            factorial *= k
        s += 1.0 / factorial
    return s


def main():
    print(f"True value: e = {math.e:.10f}\n")

    print("[Method 1] Random-sum Monte Carlo")
    print(f"  {'trials':>10}  {'estimate':>12}  {'|error|':>10}")
    for t in [1_000, 10_000, 100_000]:
        est = random_sum_estimate(t)
        print(f"  {t:>10,}  {est:>12.8f}  {abs(est - math.e):>10.2e}")

    print("\n[Method 2] Derangements (n = 10 elements)")
    print(f"  {'trials':>10}  {'estimate':>12}  {'|error|':>10}")
    for t in [1_000, 10_000, 100_000]:
        est = derangement_estimate(10, t)
        print(f"  {t:>10,}  {est:>12.8f}  {abs(est - math.e):>10.2e}")

    print("\n[Method 3] Taylor series")
    print(f"  {'terms':>6}  {'estimate':>16}  {'|error|':>12}")
    for k in [2, 4, 6, 8, 10, 12, 15]:
        est = taylor_series(k)
        print(f"  {k:>6}  {est:>16.10f}  {abs(est - math.e):>12.2e}")

    print("\nTaylor reaches machine precision in ~15 terms.")
    print("Monte Carlo's error scales as 1/sqrt(N) — three more digits costs a million x trials.")


if __name__ == "__main__":
    main()
