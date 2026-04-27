"""Estimate pi by Monte Carlo: drop random points in the unit square,
count the fraction that land inside the quarter circle.

The ratio should be pi/4 because areas: quarter-circle / square = (pi r^2 / 4) / r^2 = pi/4.
"""

import math
import random


def estimate_pi(n):
    inside = 0
    for _ in range(n):
        x, y = random.random(), random.random()
        if x * x + y * y <= 1.0:
            inside += 1
    return 4.0 * inside / n


def std_and_mean(values):
    mean = sum(values) / len(values)
    var = sum((v - mean) ** 2 for v in values) / (len(values) - 1)
    return var ** 0.5, mean


def main():
    print(f"True value: pi = {math.pi:.10f}\n")

    print(f"{'N':>10}  {'estimate':>12}  {'|error|':>12}")
    print("-" * 38)
    for n in [100, 1_000, 10_000, 100_000, 1_000_000]:
        est = estimate_pi(n)
        print(f"{n:>10,}  {est:>12.6f}  {abs(est - math.pi):>12.6f}")

    # The error scales like 1/sqrt(N). Checking this is more convincing than a single run.
    print("\nRepeating 20 trials at N = 100,000 to see the spread:")
    trials = [estimate_pi(100_000) for _ in range(20)]
    sd, mean = std_and_mean(trials)
    print(f"  mean     = {mean:.6f}")
    print(f"  std dev  = {sd:.6f}")

    # Theoretical std dev of the estimator for Monte Carlo pi:
    # var(pi_hat) = 16 * p(1-p) / N with p = pi/4
    expected_sd = math.pi * math.sqrt(1 - math.pi / 4) / (2 * math.sqrt(100_000))
    print(f"  theory   = {expected_sd:.6f}  (pi * sqrt(1-pi/4) / (2*sqrt(N)))")


if __name__ == "__main__":
    main()
