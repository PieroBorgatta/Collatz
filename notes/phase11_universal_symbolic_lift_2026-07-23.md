# Phase 11: a universal symbolic lift for one unstable K16 cell

Date: 2026-07-23

## Status

This note replaces one finite lift sample by an exact infinite
classification.  It is deliberately local: all statements about monitored
states are relative to the existing `max_K = 16` monitor table.  The result
does not prove descent or the Collatz conjecture.

The source state is

```text
K10:L7:w1-1-1-1-1-1-4:b1
```

and the finite transfer used `t = 0` as the representative of
`t mod 16 = 0`.  Write instead

```text
t = 16*u,  u >= 0.
```

The exact source constructor in `orbit_harness.source_start` gives

\[
 n(u)=1407+2048(16u)=1407+32768u.
\]

Since

\[
 3n(u)+1=2(2111+49152u)
\]

and the factor in parentheses is always odd, the first odd Syracuse step
has exponent exactly one and

\[
 S(n(u))=y(u)=2111+49152u.
\]

Thus the observed discrepancy between `u = 0` and `u = 3` is already a
one-step symbolic phenomenon; no orbit scan is needed.

## Affine valuation lemma

Let

\[
 x(u)=a+2^s c u,\qquad c,d\ \text{odd},
\]

and let a monitored rational be \(q=p/d\), with \(d\) odd.  Put

\[
 C=da-p,\qquad h=\nu_2(C).
\]

Then

\[
 \nu_2(dx(u)-p)=
 \begin{cases}
 h, & h<s,\\
 s+\nu_2(F+Gu), & h\ge s,
 \end{cases}
\]

where

\[
 F=C/2^s,\qquad G=dc
\]

and \(G\) is odd.  The first case is constant because the two summands
have distinct valuations.  The second is obtained by factoring \(2^s\).

For every \(m\ge 0\), define the unique root cylinder

\[
 r_m(F,G)= -F G^{-1}\pmod {2^m}.
\]

Then

\[
 \nu_2(F+Gu)\ge m
 \quad\Longleftrightarrow\quad
 u\equiv r_m(F,G)\pmod {2^m}.
\]

Moreover, exact valuation \(m\) is the cylinder at depth \(m\) minus its
unique lifted child at depth \(m+1\).  Consequently an affine monitored
family is represented by a single binary spine, not by a large finite
enumeration of `u`.

## Exact source classification

An exact pass over all 1,247 primitive expanding representatives in
`phantom_representatives_k3_16.csv` shows that only two monitors can ever
be eligible on \(n(u)\).

### The declared K10 source

For

\[
 q_{10}=-2059/1163
\]

one has

\[
 1163n(u)+2059
   =2^{15}(50+1163u).
\]

Therefore

\[
 v_{10}(u)=15+\nu_2(50+1163u),\qquad
 b_{10}(u)=
 \left\lfloor
 \frac{14+\nu_2(50+1163u)}{10}
 \right\rfloor.
\]

This monitor is eligible for every \(u\).

### The only K16 competitor

The only other possible source monitor is

```text
K16:L12:w1-1-1-1-1-1-4-1-1-1-1-2
```

with \(q=-716401/465905\).  Here

\[
 465905n(u)+716401
   =2^{15}(20027+465905u).
\]

It is eligible precisely when its valuation is at least \(17=A+1\), or

\[
 \nu_2(20027+465905u)\ge2
 \quad\Longleftrightarrow\quad
 u\equiv1\pmod4.
\]

On this class the K10 form is odd after removal of \(2^{15}\), so the K10
valuation is exactly 15 while the K16 valuation is at least 17.  The K16
monitor therefore wins the exact `best_hit` ordering.

Outside `u = 1 mod 4`, K10 is the only eligible monitor.  It has `b >= 2`
exactly when

\[
 \nu_2(50+1163u)\ge6
 \quad\Longleftrightarrow\quad
 u\equiv42\pmod {64}.
\]

Hence the declared raw source node with `b1` is canonical exactly on

\[
 \boxed{
 u\not\equiv1\pmod4
 \quad\text{and}\quad
 u\not\equiv42\pmod {64}.
 }
\]

## Exact one-step destination classification

Only three of the 1,247 monitors can ever be eligible on
\(y(u)=2111+49152u\).

### Baseline K9 monitor

For

```text
K9:L6:w1-1-1-1-1-4
```

with \(q=-95/31\),

\[
 31y(u)+95=2^{14}(4+93u).
\]

It is eligible for every \(u\), with

\[
 v_9(u)=14+\nu_2(4+93u),\qquad
 b_9(u)=
 \left\lfloor
 \frac{13+\nu_2(4+93u)}9
 \right\rfloor.
\]

In particular, \(b_9\ge2\) exactly on

\[
 u\equiv12\pmod {32}.
\]

### K15 competitor

For

```text
K15:L11:w1-1-1-1-1-4-1-1-1-1-2
```

\[
 144379y(u)+269627
   =2^{14}(18619+433137u).
\]

It is eligible and wins exactly when

\[
 u\equiv1\pmod4.
\]

These sources were already shadowed at time zero, so this case does not
occur after restricting to the declared canonical K10/b1 source cell.

### K16 competitor

For

```text
K16:L11:w1-1-1-1-1-4-1-1-1-1-3
```

\[
 111611y(u)+269627
   =2^{14}(14397+334833u).
\]

It is eligible and wins exactly when

\[
 u\equiv3\pmod8.
\]

Its repetition coordinate is

\[
 b_{16}(u)=
 \left\lfloor
 \frac{13+\nu_2(14397+334833u)}{16}
 \right\rfloor.
\]

The K15 and K16 eligibility cylinders are disjoint.  On either cylinder
the K9 scaled form is odd, so the competitor has strictly larger
valuation.  Everywhere else K9 is the only eligible monitor.

## Local theorem

Relative to the current `max_K = 16` monitor table:

1. `K10:L7:w1-1-1-1-1-1-4:b1` is the canonical source for `t = 16*u`
   exactly when

   \[
   u\not\equiv1\pmod4,\qquad
   u\not\equiv42\pmod {64}.
   \]

2. On that canonical source set, the next distinct monitored hit occurs
   after one Syracuse step and is

   \[
   \begin{cases}
   \texttt{K16:L11:w1-1-1-1-1-4-1-1-1-1-3:b}_{16}(u),
       & u\equiv3\pmod8,\\
   \texttt{K9:L6:w1-1-1-1-1-4:b}_{9}(u),
       & \text{otherwise}.
   \end{cases}
   \]

The original two values are immediate:

```text
u = 0:  n = 1407  -> K9 ... :b1
u = 3:  n = 99711 -> K16 ... :b1
```

So `t mod 16 = 0` is not an infinite transfer cell.  It already contains
different destinations, different repetition coordinates, and points
whose canonical source is different.

## Unbounded-`b` obstruction

The failure cannot be repaired by choosing a larger finite `b_max`.

For every \(m\), choose

\[
 u_m=r_m(50,1163).
\]

Then

\[
 \nu_2(50+1163u_m)\ge m.
\]

For \(m\ge2\), all these roots satisfy `u = 2 mod 4`; hence they are
disjoint from the K16 shadow cylinder `u = 1 mod 4`.  The K10 monitor
remains the winning source, while

\[
 b_{10}(u_m)\ge
 \left\lfloor\frac{14+m}{10}\right\rfloor
\]

is unbounded.

There are two further unbounded destination spines inside canonical
K10/b1 sources:

- \(u=r_m(4,93)\) has `u = 0 mod 4`, keeps the source at K10/b1, and
  makes \(b_9\) unbounded;
- \(u=r_m(14397,334833)\) has `u = 3 mod 8`, keeps the source at
  K10/b1, and makes \(b_{16}\) unbounded.

Therefore neither a fixed lift depth nor a fixed repetition cutoff can
turn this transfer row into a universal finite partition.

## Dependence on the monitor cutoff

“Canonical” is also relative to `max_K`.  The `u = 3 mod 8` branch is
already absorbed when the table is enlarged from K16 to K17.  The K17
representative

```text
K17:L12:w1-1-1-1-1-1-4-1-1-1-1-3
```

has \(q=-716401/400369\), and

\[
 400369n(u)+716401
   =2^{15}(17213+400369u).
\]

Its monitor condition is

\[
 \nu_2(17213+400369u)\ge3
 \quad\Longleftrightarrow\quad
 u\equiv3\pmod8.
\]

Thus exactly the apparent transition to the top K16 layer becomes an
initially shadowed source at K17.  Finite-K transfer graphs must be
treated as cutoff-dependent truncations, not stable quotients.

## Consequences for Phase 11

The appropriate replacement for finite representative enumeration is a
lazy symbolic trie:

1. store each affine family as `(s, F, G)`;
2. attach the root cylinder `u = r_m(F,G) mod 2^m` required by its monitor
   threshold;
3. compare eligible monitors symbolically on each cylinder;
4. refine only the unique root child when a repetition coordinate or
   winner is still variable;
5. retain an explicit unresolved boundary/cutoff state instead of
   interpreting it as finite escape mass.

This representation is exact and compact, but generally infinite.  A
successful global argument therefore needs an induction, ranking, or
amortized descent theorem along these root spines.  More finite spectral
enumeration cannot remove the obstruction.

## Reproduction

Run the exact audit:

```bash
python3 scripts/phantom_taxonomy/symbolic_lift_audit.py
```

It loads the existing representative table, derives candidates from the
affine valuation lemma, checks the two source and three destination
candidates, verifies the stated root congruences, and checks five fixed
examples.  It does not scan a range of `u`.
