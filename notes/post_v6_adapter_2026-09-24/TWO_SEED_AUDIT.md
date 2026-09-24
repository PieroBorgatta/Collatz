# Two explicit seeds eliminate the unknown cycle-height bound

**Aggiornamento successivo:** compilazione dei 395 moduli e audit delle due radici
PASS nella [CI 36005012141](https://github.com/PieroBorgatta/Collatz/actions/runs/36005012141).
Il testo sotto conserva il perimetro e lo stato della revisione statica iniziale;
il [resoconto finale](RESULTS_IT.md) contiene le evidenze del replay successivo.

Independent mathematical analysis, 2026-09-24. This supplements the active weighted occupation adapter; it does not replace that work.

## Main fact

For any deterministic map f, distinct points x,y with f(x)=f(y) cannot both be periodic. If p,q>0 are return periods, pq is a common period; applying f^(pq-1) to the common-image equality gives x=y. This requires no conjecture about Collatz cycles. It does not decide which of x,y is nonperiodic.

For the existing family G(r,k)=ndGeneralTargetRoot r k, the baseline proves

    3*G(r,k)+1 = 4^k*(3*r+1)
    Syracuse(G(r,k)) = Syracuse(r).

The first identity proves strict increase in k; the second says all family members have the same Syracuse image. Thus any two distinct members contain a nonreturning seed.

## Congruence and finite uniform bound

Given q,X and a desired residue y, residue surjectivity gives p:Fin(3^q). Set

    k1 = p.val + (X+1)*3^q,
    k2 = k1 + 3^q.

Both G(r,k1) and G(r,k2) are odd, greater than X, in residue y, and reach the original target provided 3*r+1=2^e*a. Both have the same Syracuse image. At least one therefore has no positive Syracuse return.

Because p<3^q, k2<(X+3)*3^q. The explicit start is r=(4*a)/3 when a%3=1, and r=(2*a)/3 otherwise; for positive a not divisible by 3 this start satisfies r<=2*a. Since G is monotone in its first parameter and strictly increasing in its index, both candidates are below the uniform bound

    T(a,q,X) = G(2*a, (X+3)*3^q).

This bound is independent of the good residue and of the choice of the nonreturning candidate. Hence the final constants do not require an algorithm to choose either one.

## No parameter cycle

Fix b=2^80 and a certified natural mixing constant C. Define

    Nseed = explicitLogarithmicSeedGeneration b C,
    qseed = ndRootCoreBackwardConductor b (explicitSeedFloor b Nseed / 4) Nseed,
    T = T(a,qseed,16^b),
    m = 132*T*C+1,
    Nmark = explicitLogarithmicGoodMarkedStart b C Nseed,
    J = Nmark + 2*m + 20*10^9,
    H = ndExplicitRootIntervalHeight b 17 T J.

The finite averaging argument chooses the good residue at qseed. Both candidates have identical backward marked mass because their residues agree. They therefore both satisfy the initial marked-mass lower bound. The frozen persistence theorem applies to each, uniformly in all later generations, with the same initial floor b, denominator 1 and root span 0. Choosing m only after the bound T is available does not change qseed or require a new seed.

## Uniform count and cutoff

For the nonreturning seed R<=T, the original no-return census has coefficient P=R. Choosing the square-error budget with T rather than R is sufficient:

    132*R*C <= 132*T*C <= m^2.

The terminal mass lower bound is eta=3/(8*3^m). The original public count then yields eta/(32*R)*Y, which is at least eta/(32*T)*Y. The same explicit height H bounds either state: apply `iterate_physicalIntervalMax_le_explicit` with root upper bound M=T. No additional monotonicity theorem for the later generation or height functions is needed.

Therefore the intended explicit constants are

    c(a,C) = 3/(256*T*3^m),
    Y0(a,C) = 32*(H+1),

with count{0<n<Y : ordinary Collatz orbit reaches a} >= c(a,C)*Y for every Y>=Y0(a,C), using the external analytic ingredients. Specializing to the library's certified numerical C makes these expressions functions of the public target alone.

## What this does and does not improve

The pair argument removes the unknown height of a possible cycle from the existential seed choice. The finite bound T also removes the unknown good residue from the final constants. It preserves the original coefficient R at the chosen nonreturning seed rather than replacing it by R(3R+1).

It still pays the explicit upper-bound ratio T/R in a uniform public constant. Thus removal of the factor 3R+1 is not, by itself, a proof that every numerical constant is sharper than the weighted route; such a comparison should use the same parameter choices. The constants remain enormous and no practical numerical evaluation is claimed.

The argument is classical in selecting the nonperiodic member. That does not prevent uniform constants, since they are computed before making the choice. An executable program that outputs the nonreturning member is not obtained. The effectivity of the final expressions is relative to the supplied certified numerical analytic constants, not an independent rederivation of those constants.

The underlying injectivity-on-periodic-points fact is elementary and already present in Mathlib. No novelty claim is made for that fact; the proposed contribution is its application to this specific congruence-controlled seed family and to the external theorem's quantitative constants.

## Implementation state

The other agent owns `/tmp/TwoSeedNonreturn.lean` with the pair lemma and bounded residue lift. I wrote `/tmp/TwoSeedDensity.lean` with three bounded frozen-seed lemmas, the constants above, a theorem conditional on supplied fine-scale mixing, and its specialization to the external fixed numerical mixing theorem. These sources have not yet been compiled at the time of this note. Baseline sources are unchanged.
