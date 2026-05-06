# Things I found interesting

## Monte Carlo's cost is brutal

The pi estimator's standard deviation shrinks like `1/sqrt(N)`. That sounds fine
until you realize: to gain **three more correct digits**, you need to multiply
N by a million. The Taylor series for e, in contrast, adds about one correct
digit per term — it reaches machine precision in about 15 iterations.

So why even use Monte Carlo? Because it **generalizes**. Taylor needs a closed-form
series for the thing you're estimating. Monte Carlo just needs a way to sample.
The derangement estimate for e is beautiful: you never "compute" e, you just
keep shuffling and counting.

## The golden ratio hides in the secant method

If you write down the secant recurrence and ask "what's the convergence order?",
the answer is a quadratic: `p^2 = p + 1`. That's the golden ratio equation.
So the secant method converges at rate `phi ~= 1.6180...`

This was the single most surprising thing in this project. A method I'd never
heard of turned out to converge at the same irrational number that shows up
in Fibonacci, pentagons, and sunflower seeds. I wasn't expecting number-theory
constants to fall out of a numerical algorithm's error analysis.

## Newton's method is faster but pickier

Newton converges quadratically — the correct-digit count doubles every step.
But it needs `f'(x)`. Worse, if `f'(x)` happens to be small near your current
guess, Newton can fly off to the wrong root or diverge entirely. Bisection is
slower but bulletproof: as long as `f` changes sign across the interval,
it cannot fail.

## The Prime Number Theorem is... true?

The density of primes near x is about `1/ln(x)`. My sieve confirms this:

| x | pi(x) | x / ln(x) | ratio |
|-----|-----|-----|-----|
| 10,000 | 1,229 | 1,086 | 1.13 |
| 100,000 | 9,592 | 8,686 | 1.10 |
| 1,000,000 | 78,498 | 72,382 | 1.08 |

The ratio slowly approaches 1. I learned that Li(x) = integral(1/ln t, 0..x)
is a much better approximation than x/ln x. Watching a theorem converge
numerically made it feel much more real than just reading the statement.

## Goldbach comet: a visible pattern in an unproven conjecture

Every even n > 2 probably equals p + q for some primes p, q. Verified up
to ~4x10^18 but still not proven. I plot g(n) = number of prime pair
decompositions for each even n and you see a fan-shaped "comet".

The comet has stripes. Even n divisible by 6 have *more* decompositions
than even n that are 2 mod 6. That makes sense once you stare at it:
if p + q = n and n is divisible by 6, then p and q can cover more
residue classes mod 6 without being composite. But I'd never have
predicted that pattern from the problem statement alone.
