# New-direction analysis for Collatz v6 — 24 September 2026

This note is an independent mathematical audit, not a claimed Collatz proof or priority claim. Existing project files were only read. The exact probe is `tower_probe.py`; results are `tower_results.json`. For the final proposal, literature comparison, and limits, see `REVIEW_IT.md` and `literature.md`.

## What v6 already does, and therefore cannot be sold as the new direction

- Exact cylinder criterion modulo `2^(A+1)`, not merely `2^A`.
- Fixed expansive-word precision tax, exact compatible affine switching.
- Failure of freely reset scalar precision, three-trace lasso, incompatible scalar labels on branching SCCs.
- Explicit defect/cancellation ledger and a constant-defect tower in which destination precision is arbitrarily large.
- Proposed exact-cylinder checker handling critical valuation towers.
- The older project notes already developed an exact lazy trie, observed no exact state merges on one residual frontier, and rejected a finite scalar-label SCC closure.

Therefore "use exact cylinders", "add the 3-adic phase", "keep a cancellation ledger", or "replace samples by symbolic tries" are individually insufficient claims of novelty.

## A rigorous adversarial macro, derived from the v6 cancellation tower

For even `k >= 4`, put

    n_k = (2^(k+1) - 11)/3.

The first exact Syracuse step has exponent 1 and sends it to

    m_k = 2^k - 5.

Write `k = 3r+h`, with `r = floor((k-1)/3)` and `h in {1,2,3}`.
The word `[1,2]` has affine map

    W(x) = (9x+5)/8 = (9/8)(x+5)-5.

It matches exactly when `x+5` has valuation at least 4. Thus exactly `r` full copies of `[1,2]` match from `m_k`, giving

    x_r = 2^h * 9^r - 5.

The first departure from this repeated word is:

| h | exact terminal word | exit y | exact 3-adic form |
|---|---|---|---|
| 1 | `[3]` | `(3*9^r-7)/4` | `4y+7 = 3^(2r+1)` |
| 2 | `[1,1]` | `9^(r+1)-10` | `y+10 = 3^(2r+2)` |
| 3 | `[1,4]` | `(9^(r+1)-5)/4` | `4y+5 = 3^(2r+2)` |

Proof of terminal exponents uses `9^r = 1 mod 8` and direct factorization. The macro from `n_k` consists of `[1]`, then `[1,2]^r`, then the terminal word.

The exit/source ratios satisfy

    y/n_k ~ c_h * (9/8)^r,
    c_1=9/16, c_2=27/8, c_3=27/64.

Therefore these ratios tend to infinity in every phase. An unbounded precision reset does NOT repay its real growth merely upon leaving the next phantom.

Stronger exact statement: for every even `k >= 30`, no intermediate value through this macro endpoint is below `n_k`, and its endpoint is strictly above `n_k`. Every intermediate `[1,2]` endpoint increases and every exponent-1 step increases. Only the terminal exponent-3 or exponent-4 endpoint needs comparison. Their differences are

    h=1: 12(y-n_k) = 9^(r+1) - 16*8^r + 23;
    h=2:  3(y-n_k) = 27*9^r - 8*8^r - 19;
    h=3: 12(y-n_k) = 27*9^r - 64*8^r + 29.

For the allowed even-k phases, h=1 is positive from r=5, h=2 already from r=2, h=3 from r=9. Multiplying the dominant term by 9 and the comparison term by 8 preserves positivity thereafter. This yields the common safe threshold k=30.

## Exact finite experiment

Ran `python3 tower_probe.py --max-k 2000`.

- 999 inputs: every even k from 4 to 2000.
- All prescribed exponent words and all macro formulas verified using arbitrary-precision integers.
- All k >= 30 survived beyond their macro endpoint without a strict descent.
- A first strict descent was observed for all 999 tested inputs; this is finite evidence only.
- Largest observed first-descent length was 1,649 Syracuse steps, at k=1,988.

Selected cases (logarithm is merely a display diagnostic; all identities and inequalities were checked exactly):

| k | macro steps | log2(exit/source) | first strict-descent step |
|---|---:|---:|---:|
| 30 | 21 | 0.28421 | 23 |
| 100 | 68 | 4.77745 | 70 |
| 200 | 135 | 12.96994 | 169 |
| 500 | 335 | 29.96244 | 435 |
| 1000 | 668 | 55.75495 | 832 |
| 2000 | 1335 | 114.92494 | 1612 |

This should be a mandatory benchmark for any amortized or mixed real/2-adic ranking candidate.

## General exact macro state and the useful 3-adic information

Let an expansive word w have `(P,Q,C)=(3^ell,2^A,C)` and `D=P-Q>0`.
For a matched run of j copies and `H(n)=Dn+C`,

    H(n_j) = P^j H(n_0)/Q^j.

If `H(n_0)=2^(jA+h)u`, with u odd, then

    H(n_j)=2^h * 3^(ell*j) * u.

So the 2-adic precision that disappears becomes exact 3-adic divisibility of the same affine numerator. Tracking only `v2(H)` discards this retained information. A useful symbolic macro state is `(word family/phase, h, j, odd cofactor u, source-height relation)` with j a parameter, not a bounded lookup-table index.

However, the obvious combined potential fails automatically:

    log2 H(n_j) - v2(H(n_j))
       = log2 H(n_0) - v2(H(n_0)) + j*ell*log2(3).

The odd cofactor grows by `3^(ell*j)`. Counting that growth positively cannot yield a decreasing rank. Stripping both 2 and 3 gives a core invariant during this run, which is useful for exact compression but by itself is not progress.

The concrete exit family above becomes three exponential Diophantine families `a*y+b=3^t`. Their subsequent exits must retain the exponent t; replacing y by one of finitely many residues discards exactly the arithmetic dependence that needs control.


## Intersection with the covered odd section E

For even k>=4, the source n_k has exact first exponent1, so it can lie only in the first of E's six ports. Its membership is equivalent to n_k=13mod18, or2^(k+1)=50mod54. Reducing modulo27 and using order18 of2 gives k=10mod18. Hence infinitely many tower sources belong to the covered section. Their first endpoint2^k-5 is20mod27. For k>=46 in this progression the proved k>=30 obstruction applies. The phantom exit is not necessarily the first return to E.
