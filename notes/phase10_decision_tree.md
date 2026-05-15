# Phase 10 Decision Tree

Date: 2026-05-14

Status: operational go/no-go tree.  This is a management artifact for
the mathematical program, not a theorem.

## 1. Current Root State

```text
Gate 10.B is open.
```

No natural infinite operator/projection interpretation has been
established for `full_T` / `FULL_{T,j}`.

The strongest exact-projection branch is currently unsupported.

## 2. Branch A: Analytic Operator Program

Branch A is now split into two sub-branches:

```text
A0: existing FULL branch on PhaseState.
A1: refined low-residue branch on (PhaseState, t mod 2^10).
```

`A0` is the only branch currently aligned with the existing Lean
`TransferMatrix V` objects.  The active interpretation is now
`A0-averaged`: the phase matrix is an averaged finite-rank quotient, not
an exact projection of the source-cell kernel.  `A1` is a research
branch motivated by source-collapse diagnostics; it requires
destination-refined data before it can become a square spectral
operator.

Continue Branch A only if the next work produces all of:

1. a defined infinite phase space `X`;
2. a killed labelled kernel `K`;
3. a chosen operator orientation: `U_K`, `L_K`, or `P_K^*`;
4. a Banach pair `B_s`, `B_w`;
5. a finite approximation scheme `E_N`, `I_N`, or equivalent;
6. a named mixed-norm approximation target;
7. a plan for local tail or exceptional-mass control.

Minimal acceptable target:

```text
|| U - I_N K_N E_N ||_{B_s -> B_w} <= epsilon_N
```

or the corresponding statement for `L_K` / `P_K^*`.

Without this, Branch A remains only heuristic diagnostics.

## 3. Branch A Early Continue Criteria

The analytic branch remains plausible if future diagnostics and
definitions support:

- `A_phase_block(B)` decreases under larger blocks in repeated windows;
- `A_label_bounded(B,L)` is lower-order relative to phase movement or
  decreases after a principled refinement;
- `DeltaTail_global(L)` remains summable-looking under larger `T` and
  larger prefix windows;
- `DeltaTail_local(L)` is either uniformly controlled or controlled by
  an explicit exceptional-mass/drift mechanism;
- terminal/killed boundary effects do not dominate the weak norm;
- true 2-adic child-cylinder oscillation is either decreasing, or is
  replaced by a different symbolic/countable-state regularity
  mechanism;
- a specialist can identify a non-artificial Banach pair.

These are continue criteria, not proof criteria.

## 4. Branch A Early Kill Criteria

Downgrade Branch A if any of the following persists after the norm is
fixed:

- no canonical infinite `K` can be defined;
- finite kernels depend essentially on arbitrary prefix windows;
- 2-adic child-cylinder oscillation remains nondecreasing in full
  labels after adequate tail sampling, and no enlarged phase space
  explains it;
- no projection/compression/Galerkin/Ulam interpretation can be stated;
- `A_phase_block(B)` stops decreasing or decreases only on selected
  cherry-picked windows;
- `A_label_bounded(B,L)` remains bounded away from zero for fixed
  retained cutoff without a regularity mechanism;
- `DeltaTail_local_max(L)` remains large on weakly significant cells and
  no exceptional-mass argument exists;
- all drift weights are overfitted diagnostics rather than mathematical
  functions;
- Hennion compactness fails for every natural candidate space;
- Keller-Liverani mixed-norm convergence cannot be formulated.

Current warning:

```text
DeltaTail_local_max(5) = 1
```

on the current `T15_B32_j64` error-budget report.  This does not kill
Branch A by itself, but it blocks uniform-tail arguments.

Additional warning from the first genuine 2-adic child-cylinder tests:

```text
T15_d2_tail4 full-label mean TV:
0.0486132 -> 0.0487704 -> 0.0509391
```

This pressures the naive `Z_2` martingale-variation branch.  It does
not yet kill Branch A, but it raises the priority of enlarged symbolic
states, countable episode graphs, or the finite-rank fallback.

Countervailing positive signal:

```text
T15_d2_tail3 source_v2_odd = 2|3:
mass = 0.0625,
mean full-over-phase excess = 0.120621,
contribution = 0.456409.
```

Thus the excess-label obstruction is structurally concentrated enough
to justify one more enlarged-state/drift test before downgrading Branch
A.

The signal survives a lighter `T = 16` run:

```text
source_v2_odd = 2|3:
mass = 0.0625,
mean full-over-phase excess = 0.152130,
contribution = 0.492200.
```

The first direct interaction-weight test is mixed-to-negative for
uniform drift:

```text
coefficient 1 on source_v2_odd = 2|3:
p95 = 0.155199,
max = 2.63334,
fraction >= 1 = 0.000366211.
```

Thus a drift-weight branch now requires an exceptional-mass mechanism.
Without that mechanism, prefer an enlarged symbolic/countable state or
the finite-rank fallback over a simple weighted sup norm.

The exceptional cells for coefficient `1` are not cleanly the weighted
bad stratum itself; the worst source phase is `v2=1|odd=1`, with ratio
`2.63334`.  This makes the simple drift-weight branch less attractive
than an enlarged symbolic model.

The enlarged symbolic branch now has a concrete continue criterion:

```text
bad component = { odd = 3 and v2 in {0,2} }.
```

This component has mass `0.3125` and captures `0.742956` of
full-over-phase excess at `T15` depth `2`, and `0.767081` at `T16`
depth `1`.  The complement has p95 `0` in both tests.  Continue Branch A
only if the bad component can be modelled internally or routed to a
finite-rank/exceptional subsystem.

The follow-up component transition budget over `0 < t < 2^21` gives:

```text
good row budget = 0.017746872,
bad row budget  = 0.058940144,
G -> B weighted fraction among good returns = 0.30797407.
```

Thus the split supports a block-kernel branch, not a
`good + tiny isolated bad error` branch.  Continue only if the next
formal model treats the four blocks `K_GG`, `K_GB`, `K_BG`, `K_BB`
explicitly or gives a principled finite-rank/exceptional replacement
for `K_bad`.

Do not switch automatically to the narrower `v2=2 and odd=3` rule:
that core has bad row budget `0.20995882` on `T15_j32`.  Do not switch
automatically to the broader `odd=3 or v2=2` rule either: it marks about
`0.5625` of sources as bad and has `G->B` weighted fraction about
`0.559896`.  The current middle split is the best provisional
compromise, not a theorem.

The component block-Cauchy diagnostic is a continue signal for weak
Branch A: weighted good/bad row `L1` mean decreases
`0.012046521 -> 0.0095367816 -> 0.0074155295` as block size grows
`8 -> 16 -> 32`.  It is not a continue signal for a uniform branch,
because p95 and max drift remain visible.

New caution: the `B=16`, `j=64` multipair run has worsening pair means
`0.009535642 -> 0.013903232 -> 0.018206286` for pairs
`0->16`, `16->32`, `32->48`.  Continue Branch A only if the next
formulation uses a genuine averaged/mixed norm or a better high-bit
limit convention; do not claim ordinary adjacent-block Cauchy
convergence.

The prefix/Cesaro check is a stronger continue signal:

```text
16->32 mean = 0.004767821,
32->64 mean = 0.0037076395,
64->128 mean = 0.0027624646.
```

Thus the next Branch-A formulation should prioritize prefix-average
block kernels.  If prefix averages fail at larger windows, switch the
analytic branch to collaborator review or finite-rank fallback.

The retained full-label lift also improves but remains nonzero:

```text
64->128 label-excess mean = 0.0029977961,
64->128 label-excess p95  = 0.015625,
64->128 label-excess p99  = 0.03125.
```

Continue Branch A only if this retained-label term is included in the
mixed norm or controlled by a genuine labelled-kernel regularity
argument.

The martingale Banach-pair attempt now has a sharper diagnostic.  Script
`112` reads script-`100` child-cylinder TV as a finite proxy for
martingale increments `||d_n K||_1`.  On the current `T=15` windows:

```text
phase increments, depths 0..3:
0.0425999 -> 0.0418446 -> 0.0410719 -> 0.0408087

full increments, depths 0..3:
0.0526182 -> 0.0544645 -> 0.0575895 -> 0.0606241

delta increments, depths 0..3:
0.0413820 -> 0.0452396 -> 0.0502739 -> 0.0549879
```

The follow-up `T15_d4_tail1` run keeps the same `64` high-bit lift
budget and adds one 2-adic depth:

```text
phase increments, depths 0..4:
0.0425999 -> 0.0418446 -> 0.0410719 -> 0.0408087 -> 0.0389357

full increments, depths 0..4:
0.0526182 -> 0.0544645 -> 0.0575895 -> 0.0606241 -> 0.0648212

delta increments, depths 0..4:
0.0413820 -> 0.0452396 -> 0.0502739 -> 0.0549879 -> 0.0600595
```

This blocks any near-term claim that an exponential martingale
variation norm is naturally contracting.  Continue the Banach-pair
branch only as a decomposed norm program, not as a full-label BV claim.

Script `113` gives the current decomposed target:

```text
phase martingale variation
+ structured label-excess correction
+ weak substochastic loss/status control.
```

Current split-budget warning:

```text
T15 depth 2: phase = 0.0410719, label-excess = 0.0165176,
             status/loss = 0.0292443.
T16 depth 1: phase = 0.0443541, label-excess = 0.0193176,
             status/loss = 0.0337435.
```

The phase term is the main obstruction because it is large and nearly
flat.  The label-excess term is more promising because
`source_odd_3_or_v2_2` captures about `0.808025` of the `T15` depth-2
full-over-phase excess and about `0.829186` of the `T16` depth-1 excess,
with complement p95 `0` in both cases.

New Branch-A criterion: do not proceed toward Hennion/Keller-Liverani
until either the phase martingale increment decays at larger genuine
2-adic depths, or a structural theorem explains why this flat phase
component is not part of the strong variation that enters LY.

Script `114` checks whether the phase obstruction can be isolated like
the label-excess obstruction.  Current answer: no.  At the best tested
structural split, the dominant phase contributor is a broad half-space:

```text
T15 depth 2, source_v2 = 0:
mass = 0.5, contribution = 0.686721, complement mean = 0.0257339.

T16 depth 1, source_v2 = 0:
mass = 0.5, contribution = 0.688173, complement mean = 0.0276616.
```

This means "finite-rank bad-label correction + LY on the complement" is
not enough.  Continue Branch A only if the phase term receives a
structural theorem, a new quotient/operator, or a proof that it is weak
variation rather than strong variation.

Script `115` gives the first plausible repair of that negative
diagnosis.  The phase obstruction is not a small bad set, but it is
largely a low destination mode.  On `T15_d4_tail1`, projection to
destination capped valuation `dst_v2` captures an increasing fraction of
phase-TV:

```text
depth 0: capture = 0.882872, residual mean = 0.00498962
depth 1: capture = 0.892471, residual mean = 0.00449950
depth 2: capture = 0.907563, residual mean = 0.00379658
depth 3: capture = 0.925382, residual mean = 0.00304508
depth 4: capture = 0.934651, residual mean = 0.00254440
```

This reopens a narrow Banach route:

```text
U = U Pi_v2 + U Q_v2              (observable/Koopman side),
U Pi_v2 finite-rank/low-mode,
U Q_v2 subject to LY.
```

Continue toward LY only for this projected residual branch.  Do not
claim that the original unprojected phase variation contracts.

Script `116` then tests whether this low-mode repair survives an actual
lift inside the destination `v2` fibers.  Current answer: not with the
obvious canonical lifts.  On `T15_d2_tail3`:

```text
depth 2:
proxy_residual        = 0.00379658,
pair_pooled_residual  = 0.00440467,
global_pooled_residual = 0.0416961,
source_pooled_residual = 0.0197842,
uniform_residual      = 0.0416970.
```

The pair-dependent lift is encouraging but not canonical.  A global
lift fails, and even a finite `source PhaseState`-conditioned lift is
too large and increasing on depths `0..2`.  Therefore Branch A can
continue only if a richer source-refined but still compact/finite-rank
lift is defined, or if a new quotient makes the `dst_v2` fiber law
canonical.

The first richer source-refined attempt has now been tested and is
negative for the simple family

```text
(source PhaseState, r mod 2^k),  k = 0,2,4,6,8.
```

On `T15_d2_tail3`, depth `2`, the best tested source-refined residual is

```text
source_refined_b8_residual = 0.0196251,
pair_pooled_residual       = 0.00440467.
```

Thus low residue bits do not close the projected LY branch.  Continue
analytic work only if the next step is a genuinely new quotient,
signed-kernel/Galerkin interpretation, or proof that the pair-dependent
lift is legitimate.  Do not spend more effort merely increasing `k` in
this same source-refinement family.

Current `A0/A1` decision rule:

```text
Keep A0-averaged as the only conditional analytic branch still aligned
with existing FULL/Lean objects, but not as the no-collaborator lead.
Keep A1 as secondary unless refined-square drift becomes competitive
with A0 or a Banach norm explains the larger drift constant.
```

Current finite evidence:

```text
A0 phase-only square drift at T12:
0.00138619007 -> 0.00109704799 -> 0.000647069352.

A1 rlo10 square drift at T12:
0.0152083349 -> 0.0135561906 -> 0.0129098735.
```

Thus `A1` is not killed, because it decreases, but it is not currently
the lead analytic branch.  Under the no-collaborator route, the next
go/no-go judgment is internal and conservative: unless `A0-averaged`
receives a proof-quality weak approximation framework, Branch A is
paused as conditional background.

## 5. Branch B: Finite-Rank Fallback

Branch B is already theorem-producing for production K16:

```text
M v <= (3/4) v
```

for the declared 37-state deterministic residue-cell `(K,b)` matrix,
with exact Lean verification.

Continue Branch B if:

- Gate 10.B remains unresolved;
- the analytic branch would need collaborator validation but none is
  being pursued;
- a finite-rank computational note is desired regardless of Branch A;
- K20 production extension becomes feasible with a declared production
  SCC.

## 6. Branch B Kill Criteria

Do not promote Branch B beyond its finite scope if:

- the finite residue-cell model is not defined cleanly in prose;
- generated artifacts cannot be reproduced from a manifest;
- sensitivity checks are presented as a limit theorem;
- K20 smoke is described as production;
- finite spectral-radius bounds are used as evidence for an infinite
  spectral gap without Gate 10.B.

## 7. Collaboration Criteria

Current route: no collaborator.  This section is retained only as an
archived escalation path, not as an active dependency.

Ask for specialist collaboration if:

- `A0-averaged` is plausible but its approximation status is unclear;
- local tails require a nonstandard drift/tightness argument;
- countable Markov shift/Sarig hypotheses look possible but unverified;
- Hennion compactness is unclear;
- Keller-Liverani might apply but the mixed norm is not standard.

Collaborator profile:

```text
transfer operators for open systems or countable Markov shifts,
with Hennion/Keller-Liverani and symbolic Banach-space experience.
```

## 8. Stop Criteria

Stop analytic Phase 10 and write the finite-rank note if:

1. no collaborator review is being pursued and no internal proof
   validates `A0-averaged`;
2. the only available spaces make `K` unbounded;
3. local tails cannot be controlled uniformly or by exceptional mass;
4. finite kernels have no stable high-bit limit;
5. the `A0-averaged` finite-rank interpretation remains unvalidated,
   non-canonical, or normless;
6. `A1` refined-square drift stays too large for any plausible weak
   norm;
7. the phase martingale increment remains flat at larger genuine
   2-adic depths and no reduced/enriched operator removes it from the
   LY strong norm;
8. the `Q_v2` residual from the low-mode projection stops decaying or
   cannot be represented by a canonical projection/lift in the operator
   framework;
9. the only small `Q_v2` residual remains pair-dependent, with global,
   finite-source-conditioned, and low-residue source-refined lifts
   staying comparable to the original phase obstruction.

This would not be a failure of the project.  It would mean the honest
deliverable is finite-rank rather than analytic.

## 9. Publication Routing

### v4 route

Use if:

- the finite-rank certificate is presented as the main rigorous
  addition; or
- Gate 10.B is later made coherent by an internal proof-quality
  framework;
- no spectral claims are made beyond proved hypotheses in either case.

### Companion analytic note

Use if:

- the operator/norm framework is promising but too conditional for v4;
- a collaborator is involved;
- the output is a formal program with partial estimates, not a theorem.

### Coauthored paper

Use if:

- a specialist supplies or verifies a genuine Banach-space/projection
  theorem;
- Hennion or Keller-Liverani hypotheses become checkable.

### Finite-rank computational note

Use if:

- Gate 10.B fails or stalls;
- K16 finite theorem is the main rigorous deliverable;
- K20 is either promoted to production or kept as a clearly labelled
  smoke appendix.

## 10. Current Recommendation

Current best decision:

```text
Reopen A0 only in the narrow Haar-conditional-expectation sense:
X = Z_2 x H, killed forward kernel U_s, and conditional expectation
onto sigma(PhaseState).
Do not invoke Hennion or Keller-Liverani without a new proof-quality
operator/norm bridge.
Make Branch B the active no-collaborator Phase-10 deliverable.
Keep A1 as an archived secondary diagnostic, not a claim.
Do not commit to the naive Z_2 martingale space without a new mechanism;
the only live Banach route is the decomposed martingale pair:
finite `dst_v2` low mode plus residual phase variation plus structured
label-excess plus weak loss control.
The tested `dst_v2` low-mode route is currently blocked at the lift
stage, so the next analytic move must reduce the operator/quotient
itself rather than add another local metric.
```

The relevant A0 bridge is now
`notes/phase10_gate10B_conditional_closure.md`.  It is a conditional
Gate-10.B closure attempt, not a spectral theorem.
