# Phase 11: affine trace graph verdict

Date: 2026-07-27

## Result

Compatible affine trace switching is exact and useful, but it does not supply
a global rank for genuinely aperiodic switching.

The mechanism has now been characterized algebraically. A scalar trace on a
finite control graph exists only when all directed cycles through a control
node are coherent with the same rational formal point. This includes periodic
phantom lassos and redundant branching around one phantom. It excludes a
branching SCC whose cycles correspond to different phantom fixed points.

This is a structural theorem and an exact linear-algebra test, not a finite
orbit diagnostic.

## Formal point carried by a trace label

For a positive label `(D,C)`, define

\[
x_{D,C}=-\frac{C}{D}.
\]

For an exponent edge \(e\), define

\[
T_e(x)=\frac{3x+1}{2^e}.
\]

The compatible-switch equations are

\[
3D'=qD,\qquad D'+2^eC'=qC,
\]

where \(q\) is odd for the precision theorem. Direct division of these two
identities gives

\[
x_{D',C'}=T_e(x_{D,C}).
\]

Lean theorem `switchingFormalPoint_transport` proves this over the rationals.
Thus `(D,C)` cannot be chosen as a local ranking decoration: it is an actual
rational orbit point constrained by every edge.

## Consequence for cycles

If a directed cycle has exponent word \(w\), returning to the same control
node forces its label point \(x\) to satisfy

\[
\operatorname{Affine}_w(x)=x.
\]

For a nondegenerate word this fixed point is unique:

\[
x=q_w=
\frac{C_w}{2^{A_w}-3^{L_w}}.
\]

Lean theorem
`syracuseWordAffineEndpointQ_fixed_eq_formalFixedPoint` proves uniqueness.
The theorem `no_common_rational_fixed_point_of_distinct_words` then proves:
two cycle words with different \(q_w\) cannot be carried by one scalar trace
at the same control node.

The concrete corollary for `[1]` and `[1,2]` is Lean-checked. Their fixed
points are respectively `-1` and `-5`, so no common scalar trace exists.

## Exact graph solver

`scripts/phantom_taxonomy/affine_trace_graph_solver.py` takes a finite graph
with edges

```text
source -- exponent --> target
```

and solves the rational equations

\[
2^e x_{\rm target}-3x_{\rm source}=1
\]

by exact Gaussian elimination over `Fraction`.

If the unique solution is negative at every node, a common denominator
produces primitive natural labels with `q=3`:

\[
D+2^eC_{\rm target}=3C_{\rm source}.
\]

The solver verifies:

```text
[1] cycle:
  D=1, C=1

[1,2] cycle:
  D=1, C=(5,7)

[1,1,2] cycle:
  D=11, C=(19,23,29)

compatible redundant branching:
  accepted

branching with [1] and [1,2] cycles:
  inconsistent

[2] self-cycle:
  unique point +1, rejected as a negative phantom trace
```

It enumerates no integer orbit and no residue range.

## Infinite branching obstruction

The small incompatible branching graph consisting of:

- an exponent-`1` self-loop;
- an exponent-`1` edge followed by an exponent-`2` return;

contains the cycle family

\[
w_r=[1]^{r+1}\mathbin{+\!\!+}[2],\qquad r\ge0.
\]

Put \(k=r+1\). Exact affine composition gives

\[
C_{w_r}=3^{k+1}-2^{k+1},
\]

\[
3^{L_{w_r}}-2^{A_{w_r}}
  =3^{k+1}-2^{k+2},
\]

and therefore

\[
q_{w_r}
=-\frac{3^{k+1}-2^{k+1}}
        {3^{k+1}-2^{k+2}}.
\]

Let \(a_k=(3/2)^{k+1}>2\). Then

\[
q_{w_r}=-\frac{a_k-1}{a_k-2}
       =-1-\frac1{a_k-2}.
\]

Since \(a_k\) is strictly increasing, these fixed points are all distinct and
converge to `-1`. The graph therefore contains infinitely many incompatible
cycle boundaries even though it has only two control nodes.

Under the current certificate semantics, a finite library of scalar affine
labels cannot provide a closed trace for every one of these cycles. The
phenomenon is the graph form of the already identified family
`[1]^r ++ [2]`.

## Decision

The following routes are now rejected:

1. increase a finite spectral/residue matrix until it is treated as universal;
2. deepen the exact residue trie breadth-first;
3. merge residuals using only local affine/valuation signatures;
4. use the fixed traces `n+1`, `n+5`, and `n+7`;
5. attach one dynamically compatible scalar affine trace to every node of a
   genuinely branching residual SCC.

Compatible affine traces remain valuable as:

- exact lasso certificates;
- constructive bounds on periodic phantom shadowing;
- edge-local progress checks inside a cycle-coherent SCC;
- a fast algebraic rejection test for proposed control graphs.

They do not remove the aperiodic obstruction. A further Collatz-relevant
advance would need a non-scalar global resource that survives changes among
infinitely many rational phantom boundaries, or a first-barrier theorem that
forces descent without naming those boundaries individually.

The rational action of the exponent semigroup is therefore the remaining
object, not a larger finite transition table.

## Reproduction

```bash
python3 scripts/phantom_taxonomy/affine_trace_graph_solver.py
lake build CollatzShadowing.AffineTraceGraph
```
