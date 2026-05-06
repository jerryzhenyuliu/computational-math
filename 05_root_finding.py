"""Three methods for solving f(x) = 0, compared on the same three equations.

  Bisection:  linear convergence. Each step halves the interval.
  Secant:     superlinear ~1.618 (the golden ratio!). Uses a finite-difference slope.
  Newton:     quadratic. Needs f'(x) but doubles the correct digits per step.

I was surprised the secant method's convergence order is the golden ratio.
That comes from solving the recurrence e_{n+1} ~ C * e_n * e_{n-1}, whose
characteristic equation is x^2 = x + 1 — the golden ratio equation.
"""

import math


def bisection(f, a, b, tol=1e-12, max_iter=200):
    assert f(a) * f(b) < 0, "f(a) and f(b) must have opposite signs"
    history = []
    for _ in range(max_iter):
        mid = (a + b) / 2
        history.append(mid)
        if (b - a) <= 2 * tol:
            break
        if f(mid) * f(a) < 0:
            b = mid
        else:
            a = mid
    return history


def newton(f, df, x0, tol=1e-12, max_iter=100):
    x = x0
    history = [x]
    for _ in range(max_iter):
        fx = f(x)
        if abs(fx) < tol:
            break
        dfx = df(x)
        if abs(dfx) < 1e-15:
            break
        x = x - fx / dfx
        history.append(x)
    return history


def secant(f, x0, x1, tol=1e-12, max_iter=100):
    history = [x0, x1]
    for _ in range(max_iter):
        f0, f1 = f(x0), f(x1)
        if abs(f1 - f0) < 1e-15:
            break
        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
        history.append(x2)
        if abs(x2 - x1) < tol:
            break
        x0, x1 = x1, x2
    return history


def estimate_order(history, true_root):
    """For error e_n -> 0, |e_{n+1}| ~ C * |e_n|^p.  So p ~ log|e_{n+1}| / log|e_n|."""
    errs = [abs(x - true_root) for x in history]
    orders = []
    for i in range(2, len(errs)):
        if 1e-14 < errs[i - 1] < 0.1 and errs[i] > 1e-14:
            orders.append(math.log(errs[i]) / math.log(errs[i - 1]))
    return orders


CASES = [
    {
        "name": "cos(x) = x",
        "f":    lambda x: math.cos(x) - x,
        "df":   lambda x: -math.sin(x) - 1,
        "interval": (0.0, math.pi / 2),
        "newton_x0": 0.5,
        "secant_pair": (0.0, 1.0),
        "root": 0.7390851332151607,
    },
    {
        "name": "x^5 - x - 1 = 0",
        "f":    lambda x: x**5 - x - 1,
        "df":   lambda x: 5 * x**4 - 1,
        "interval": (1.0, 2.0),
        "newton_x0": 1.5,
        "secant_pair": (1.0, 1.5),
        "root": 1.1673039782614187,
    },
    {
        "name": "exp(x) = 3x",
        "f":    lambda x: math.exp(x) - 3 * x,
        "df":   lambda x: math.exp(x) - 3,
        "interval": (0.5, 1.5),
        "newton_x0": 1.0,
        "secant_pair": (0.5, 1.5),
        "root": 1.5121345516578424,
    },
]


def summary_table():
    print(f"{'equation':>20}  {'bisection':>16}  {'newton':>16}  {'secant':>16}")
    print("-" * 72)
    for c in CASES:
        hb = bisection(c["f"], *c["interval"])
        hn = newton(c["f"], c["df"], c["newton_x0"])
        hs = secant(c["f"], *c["secant_pair"])
        eb = abs(hb[-1] - c["root"])
        en = abs(hn[-1] - c["root"])
        es = abs(hs[-1] - c["root"])
        print(f"  {c['name']:>18}  "
              f"{len(hb):>4}steps/{eb:.0e}  "
              f"{len(hn)-1:>4}steps/{en:.0e}  "
              f"{len(hs)-1:>4}steps/{es:.0e}")


def step_by_step(case):
    hb = bisection(case["f"], *case["interval"])
    hn = newton(case["f"], case["df"], case["newton_x0"])
    hs = secant(case["f"], *case["secant_pair"])
    root = case["root"]

    print(f"\nStep-by-step error for {case['name']}:")
    print(f"  {'step':>4}  {'bisection':>12}  {'newton':>12}  {'secant':>12}")
    for i in range(min(len(hb), 15)):
        eb = abs(hb[i] - root)
        en = abs(hn[i] - root) if i < len(hn) else 0.0
        es = abs(hs[i] - root) if i < len(hs) else 0.0
        print(f"  {i+1:>4}  {eb:>12.2e}  {en:>12.2e}  {es:>12.2e}")
        if max(eb, en, es) < 1e-11:
            print("       ... all three converged.")
            break


def convergence_order_demo():
    print("\nSecant method convergence order (should be ~1.618):")
    c = CASES[0]
    hs = secant(c["f"], *c["secant_pair"])
    orders = estimate_order(hs, c["root"])
    orders_in_range = [o for o in orders if 1.0 < o < 3.0]
    if orders_in_range:
        avg = sum(orders_in_range) / len(orders_in_range)
        print(f"  measured order = {avg:.4f}")
    print(f"  golden ratio   = {(1 + 5**0.5)/2:.4f}")


def main():
    summary_table()
    step_by_step(CASES[0])
    convergence_order_demo()

    print("\nHow many steps to reach 1e-12 tolerance (roughly):")
    print("  bisection  ~40 steps   (each step halves the interval)")
    print("  secant     ~8  steps   (order ~ phi = 1.618)")
    print("  newton     ~6  steps   (order 2 — digits double per step)")


if __name__ == "__main__":
    main()
