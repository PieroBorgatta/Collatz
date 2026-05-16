# Finite-Rank Computational Note Outline

Date: 2026-05-13

Status: outline for a standalone finite-rank computational note.  This
is not an analytic Phase-10 theorem and does not claim an infinite
transfer operator, a spectral gap, Conjecture 6, or the Collatz
conjecture.

Current route: no-collaborator Phase 10.  This outline is now the active
main deliverable; `A0-averaged` remains background or appendix material
unless a proof-quality operator/norm bridge is supplied internally.

## 1. Proposed Title

```text
A Certified Finite-Rank Collatz-Wielandt Bound for a Deterministic
Residue-Cell Shadowing Model
```

Alternative shorter title:

```text
A Lean-Checked Finite-Rank Collatz-Wielandt Certificate
```

## 2. Scope Statement

The note proves a finite statement only:

```text
For the declared K0 = 16 deterministic residue-cell model, compressed
to the 37-state (K,b) macro-state space, the generated substochastic
matrix M admits a positive Collatz-Wielandt vector v with

  M v <= (3/4) v.

Consequently the finite real matrix has spectral radius <= 3/4.
```

The note does not prove:

- any statement for all Collatz trajectories;
- convergence as `K0 -> infinity`;
- convergence as `lift_bits -> infinity`;
- an infinite transfer-operator spectral gap;
- the Phase-10 analytic program;
- Conjecture 6.

## 3. Mathematical Objects

### 3.1 Input graph

The production baseline uses the `K0 = 16`, `S16`, SCC-rank-1 source
set from the previous phantom-taxonomy pipeline.

Files:

```text
scripts/phantom_taxonomy/phantom_representatives_k3_16.csv
scripts/phantom_taxonomy/orbit_harness_k16_s16_scc_nodes.csv
```

Prose definition for the note:

```text
S16 is the finite list of raw phantom-taxonomy source nodes whose
sampled orbit-harness graph belongs to SCC rank 1 after restricting to
representatives with K <= 16 and the declared S16 sampling rule.  Each
raw source node has the form w:b, where w is a phantom representative
key from phantom_representatives_k3_16.csv and b is the monitored
2-adic depth parameter recorded in orbit_harness_k16_s16_scc_nodes.csv.
Only rows with scc_rank = 1 are admitted as production source nodes.
```

This definition is intentionally finite.  It does not assert that `S16`
is canonical in an infinite limit; it only declares the source set of
the certified finite model.

### 3.2 Deterministic residue-cell enumeration

Generator:

```text
scripts/phantom_taxonomy/deterministic_residue_transfer.py
```

Production parameters:

```text
max_k       = 16
scc_rank    = 1
lift_bits   = 4
max_steps   = 1000
compression = (K,b)
```

Verified production counts:

```text
raw SCC source nodes       = 1240
finite residue cells       = 19840
canonical source cells     = 17671
shadowed initial cells     = 2169
no-initial cells           = 0
budget exits               = 0
internal SCC transitions   = 17176
exits below start          = 495
```

Every source row in the coverage CSV should sum to `2^lift_bits`.

For each raw source node `w:b`, the deterministic enumeration subdivides
the monitored congruence class into

```text
0 <= t < 2^lift_bits.
```

Writing `A_w` for the total parity length of representative `w`, the
corresponding starting integer is

```text
n0 = q_w mod 2^(b A_w + 1) + t * 2^(b A_w + 1).
```

The generator first asks whether the best monitored phantom hit at
`n0` is exactly the declared source node `w:b`.  If a finer or stronger
monitored phantom owns `n0`, the class is counted as
`shadowed_initial` and is not a source event.  Otherwise the class is
canonical and is traced deterministically until:

- the orbit hits a distinct monitored node inside the declared SCC;
- the orbit hits a monitored node outside the declared SCC;
- the odd Syracuse orbit drops below `n0`;
- or the step budget is reached.

For production K16 there are no budget classes.  Classes that drop below
start are substochastic exits, not internal transitions.

### 3.3 Certified finite matrix

Certified matrix:

```text
scripts/phantom_taxonomy/deterministic_k16_s16_residue_K_edges.csv
```

Summary:

```text
states                       = 37
nonzero internal edge types  = 182
source events                = 17671
internal hits                = 17176
exits                        = 495
retention mass               = 0.971988
rho diagnostic               = 0.701094388677
```

The decimal `rho diagnostic` is not the certificate.  The certificate is
the exact Collatz-Wielandt inequality.

### 3.3.1 Reader-facing `(K,b)` compression

The raw deterministic model has one row for each canonical residue
source cell.  The certified theorem compresses those rows to the
macro-state

```text
(K,b),
```

where `K` records the representative class/complexity level used by the
phantom-taxonomy pipeline and `b` records the monitored 2-adic depth.
The compression forgets the representative key `w` but retains the two
coordinates used in the K16 production certificate.  Thus the certified
matrix is not the full raw source-cell transition matrix; it is the
declared 37-state finite quotient used by the theorem.

No claim is made here that `(K,b)` is an asymptotically complete state
coordinate.  It is only the finite state space of the certified model.

### 3.4 Orientation

The Lean matrix is incoming:

```text
M(dst,src) = probability from source src to destination dst.
```

The finite CW theorem is stated for this exact matrix orientation.  The
note must not identify this with a Ruelle/preimage convention unless a
transpose convention is explicitly introduced.

## 4. Exact Certificate

Certificate file:

```text
scripts/phantom_taxonomy/deterministic_k16_s16_residue_K_cw_certificate.json
```

Verification command:

```text
python3 scripts/phantom_taxonomy/scc_cw_certificate.py \
  --verify scripts/phantom_taxonomy/deterministic_k16_s16_residue_K_cw_certificate.json
```

Current verified output:

```text
alpha=3/4
max_ratio=90833233962213/129559208330288
max_node=K11:b2
status=OK
```

Headline exact inequality:

```text
90833233962213 / 129559208330288 < 3/4.
```

Equivalent cleared-denominator inequality:

```text
4 * 90833233962213 < 3 * 129559208330288.
```

Finite Collatz-Wielandt proof paragraph:

```text
Let M be the declared finite nonnegative substochastic matrix, with the
incoming convention fixed above.  Suppose v has strictly positive
coordinates and M v <= alpha v coordinatewise.  For the weighted sup
norm ||x||_v = max_i |x_i| / v_i, positivity gives
||M x||_v <= alpha ||x||_v for all x.  Hence the operator norm of M in
this finite-dimensional norm is at most alpha, and therefore
rho(M) <= alpha.  In the K16 certificate alpha = 3/4, and the generated
Lean module checks the coordinatewise rational inequalities exactly.
```

## 5. Lean Boundary

Lean file:

```text
lean/CollatzShadowing/Generated/K16S16KDeterministicCW.lean
```

Lean theorem names to cite:

```text
k16s16KDeterministicMaxRatio_lt_alpha
k16s16KDeterministicVectorNat_pos
k16s16KDeterministicFiniteCWCertificate
k16s16KDeterministicGeneratedSpectralRadiusBound
```

Build command:

```text
lake build CollatzShadowing.Generated.K16S16KDeterministicCW
```

Current verification:

```text
Build completed successfully (3302 jobs).
```

Reverified locally on 2026-05-15 after the projected-LY lift tests:

```text
python verifier: status=OK,
max_ratio=90833233962213/129559208330288,
max_node=K11:b2.

Lean build: Build completed successfully (3302 jobs).
```

Stable artifact convention:

```text
The theorem statement cites the generated Lean module and the exact CW
JSON certificate as fixed finite artifacts.  The generator is part of
the reproducibility record, but the finite theorem does not depend on
claiming a canonical infinite generation process.
```

## 6. Suggested Paper Structure

1. Introduction and finite scope.
2. Definition of the deterministic residue-cell shadowing model.
3. Construction of the finite substochastic `(K,b)` matrix.
4. Collatz-Wielandt finite certificate.
5. Lean formalization boundary.
6. Sensitivity checks.
7. Limitations and relation to Phase 10.
8. Reproducibility manifest.

## 6.1 Paper-Facing Draft Text

This draft block is intentionally finite in scope.  It can be used as a
standalone computational note, a v4 section, or a supplementary note.

### Finite Model

We fix the finite data used by the production K16 deterministic
residue-cell run:

```text
max_k       = 16,
scc_rank    = 1,
lift_bits   = 4,
max_steps   = 1000,
compression = (K,b).
```

The source list is the rank-1 SCC node set in
`orbit_harness_k16_s16_scc_nodes.csv`, with representatives read from
`phantom_representatives_k3_16.csv`.  A raw source state is a pair
`w:b`, where `w` is a phantom representative and `b` is the monitored
2-adic depth.  For each such source state the deterministic residue-cell
enumeration subdivides the declared congruence class into
`2^lift_bits` finite residue subclasses.  Each subclass is then
classified as one of:

- canonical source class;
- shadowed initial class;
- no-initial class;
- internal transition inside the declared SCC;
- external transition;
- drop below the starting integer;
- step-budget exit.

For the production K16 run the manifest records:

```text
raw SCC source nodes       = 1240
finite residue cells       = 19840
canonical source cells     = 17671
shadowed initial cells     = 2169
no-initial cells           = 0
budget exits               = 0
internal SCC transitions   = 17176
exits below start          = 495
```

Only canonical source classes contribute source mass to the finite
transition matrix.  Drop-below-start classes are treated as
substochastic loss.  The production theorem is therefore a theorem about
this declared finite killed model, not about all Collatz orbits.

### Matrix Construction

The production certificate compresses the raw deterministic source-cell
data to the 37-state macro-space `(K,b)`.  The certified matrix is the
rational substochastic matrix

```text
M(dst,src) = count(src -> dst) / source_events(src),
```

with incoming orientation: destination index first, source index second.
For K16 the matrix has:

```text
states                       = 37
nonzero internal edge types  = 182
source events                = 17671
internal hits                = 17176
exits                        = 495
retention mass               = 0.971988...
```

The decimal spectral-radius diagnostic produced by the scripts is not
the certificate.  The certificate is the exact Collatz-Wielandt
inequality described below.

### Theorem

Finite K16 deterministic residue-cell certificate.

Let `M` be the 37-state rational substochastic matrix produced by the
K16 deterministic residue-cell construction above, compressed to
`(K,b)` and interpreted with incoming orientation.  Then there exists a
strictly positive vector `v in R_{>0}^{37}` such that

```text
M v <= (3/4) v
```

coordinatewise.  Consequently the realified finite matrix satisfies

```text
spectralRadius(M) <= 3/4.
```

In the generated certificate, the largest row ratio is attained at
`K11:b2` and is exactly

```text
90833233962213 / 129559208330288 < 3/4.
```

Equivalently:

```text
4 * 90833233962213 < 3 * 129559208330288.
```

### Proof

The proof is finite.  The generator writes the rational matrix and a
positive integer Collatz-Wielandt vector.  The generated Lean module
checks positivity of every coordinate of the vector and checks all
coordinate inequalities exactly after clearing denominators.

The abstract step is the standard finite Collatz-Wielandt argument.  If
`v_i > 0` and `M v <= alpha v`, define the weighted sup norm

```text
||x||_v = max_i |x_i| / v_i.
```

For a nonnegative matrix `M`, the coordinatewise inequality implies

```text
||M x||_v <= alpha ||x||_v.
```

Thus the operator norm of `M` in this finite-dimensional norm is at most
`alpha`, and the spectral radius is at most `alpha`.  In the K16
certificate `alpha = 3/4`.

The Lean boundary is:

```text
CollatzShadowing/Generated/K16S16KDeterministicCW.lean
```

with the paper-facing declarations:

```text
k16s16KDeterministicMaxRatio_lt_alpha
k16s16KDeterministicVectorNat_pos
k16s16KDeterministicFiniteCWCertificate
k16s16KDeterministicGeneratedSpectralRadiusBound
```

The generic spectral-radius bridge is in
`CollatzShadowing/Bound.lean`.

### Sensitivity

The production Lean theorem uses `lift_bits = 4`.  Additional Python
checks at `lift_bits = 5` and `lift_bits = 6` also admit exact
Collatz-Wielandt certificates below `3/4`:

```text
lift_bits = 5:
7332495524923 / 10616480126384 < 3/4.

lift_bits = 6:
64869145309473 / 97226913303232 < 3/4.
```

These checks support robustness for nearby finite refinements.  They do
not prove convergence in `lift_bits`.

### Limitation

This theorem is finite-rank only.  It does not assert that the K16
matrix is a projection, truncation, Galerkin approximation, or Ulam
discretization of a natural infinite transfer operator.  It does not
assert convergence in `K`, in `lift_bits`, or in any 2-adic/cylinder
limit.  It does not imply a spectral gap for Collatz dynamics and does
not prove Conjecture 6 or the Collatz conjecture.  Its value is that,
within the declared deterministic residue-cell shadowing model, the
spectral-radius bound is an exact finite statement with a Lean-checked
Collatz-Wielandt certificate.

## 7. Sensitivity Checks

The production Lean certificate uses `lift_bits = 4`.

Additional non-Lean sensitivity checks:

| lift bits | source cells | canonical cells | exits below start | `(K,b)` edge types | exact max ratio | status |
|---:|---:|---:|---:|---:|---:|---|
| 4 | 19840 | 17671 | 495 | 182 | `90833233962213/129559208330288` | `< 3/4` |
| 5 | 39680 | 35331 | 990 | 190 | `7332495524923/10616480126384` | `< 3/4` |
| 6 | 79360 | 70667 | 1975 | 209 | `64869145309473/97226913303232` | `< 3/4` |

These checks support robustness within nearby finite refinements.  They
do not prove a limit in `lift_bits`.

## 8. K20 Smoke, Clearly Marked

K20 smoke files:

```text
notes/phantom_taxonomy_k20_smoke_scc_report.md
scripts/phantom_taxonomy/deterministic_k20_smoke_residue_transfer_summary.md
scripts/phantom_taxonomy/deterministic_k20_smoke_residue_K_cw_certificate.json
```

Verified smoke output:

```text
alpha=3/4
max_ratio=42001755821431/62996587868160
max_node=K4:b4
status=OK
```

Reverified locally on 2026-05-15 with the Python certificate verifier.

This is useful only as a feasibility signal.  It is not a K20 theorem
because the SCC input is a small sampled smoke graph.

## 9. Production K20 Promotion Checklist

Before K20 can be stated as a theorem candidate:

1. declare a production SCC input, not a smoke SCC;
2. fix the sampling budget and `b` range;
3. rerun SCC extraction and archive the component list;
4. run deterministic residue-cell enumeration on the production SCC;
5. generate permanent edge CSVs and manifest;
6. compute and verify an exact CW certificate;
7. generate a Lean module with a distinct declaration prefix;
8. run `lake build` on the generated module;
9. state explicitly that K20 is not a monotone strengthening of K16
   unless a comparison theorem is proved.

Current blocker, checked on 2026-05-15:

```text
Only K20 smoke artifacts are present locally:
orbit_harness_k20_smoke_*,
deterministic_k20_smoke_*,
notes/phantom_taxonomy_k20_smoke_scc_report.md.
```

There is no declared production K20 SCC input in the current workspace.
Therefore the next K20 step is not "generate a K20 theorem"; it is to
declare and run a production SCC input.  Rerunning the existing K20
pipeline would reproduce the smoke branch, not promote it.

## 10. Relationship to Phase 10

If Gate 10.B later succeeds, this finite-rank certificate can be a
baseline or appendix.

Under the current reduction, Gate 10.B for the existing `FULL` matrices
means validating the `A0-averaged` interpretation:

```text
K_N^0 is an averaged PhaseState finite-rank quotient,
not an exact projection of the source-cell kernel.
```

Under the no-collaborator route, Gate 10.B is not being pursued to
analytic closure unless an internal proof-quality operator/norm bridge
is found.  If no Banach weak norm can make the interpretation meaningful,
Gate 10.B fails for the analytic branch.  In that case this finite-rank
certificate is the cleanest Phase-10 output:

```text
an honest finite theorem with exact arithmetic and Lean verification.
```

That outcome is mathematically respectable.  It is smaller than the
analytic ambition, but it does not rely on unproved projection,
compactness, or perturbation hypotheses.

Comparison paragraph for the draft:

```text
The finite-rank certificate and the Phase-10 A0-averaged program answer
different questions.  The certificate is an exact statement about one
declared finite substochastic matrix and a Lean-checked
Collatz-Wielandt vector.  The A0-averaged program asks whether a family
of phase quotients can approximate a natural infinite killed operator
in a weak operator norm.  The former is already rigorous at K16; the
latter remains conditional and is not used to justify the finite
spectral-radius bound.
```

## 11. Reproducibility Manifest

Repository root:

```text
/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz
```

Primary fixed artifacts:

| artifact | lines | sha256 |
|---|---:|---|
| `lean/CollatzShadowing/Generated/K16S16KDeterministicCW.lean` | 2981 | `e5c64ba7c7cf83bae481055cb475384fff9cdeaec17a3d428d2d3b8ea64d1abb` |
| `scripts/phantom_taxonomy/deterministic_k16_s16_residue_manifest.json` | 54 | `57cc39b14b483caa31c720bf0a0adda51937b5301e27dc740c749c07aef66210` |
| `scripts/phantom_taxonomy/deterministic_k16_s16_residue_K_cw_certificate.json` | 1181 | `bad2d1536ce3d3df2c841e98b39b3dbfc7c8374ff5aeeecded28c331dc1546ee` |
| `scripts/phantom_taxonomy/deterministic_k16_s16_residue_K_edges.csv` | 183 | `b2e6980ebaee7fe7e07bb9e4ea9944b51245fd5586b3aa45cf08c75fbc5d7954` |

Generator and verifier:

| artifact | sha256 |
|---|---|
| `scripts/phantom_taxonomy/deterministic_residue_transfer.py` | `b4079f8e8909e5f38f7072ea27527f61893d66a80b38e0023b23d80840018aad` |
| `scripts/phantom_taxonomy/scc_cw_certificate.py` | `41d5e89e36d660a0ca3d611c8dd1fef5fa2500129fc2192c2238b2da5fa4a231` |

Inputs:

| artifact | lines | sha256 |
|---|---:|---|
| `scripts/phantom_taxonomy/phantom_representatives_k3_16.csv` | 1248 | `5098987c65393ab8aab26b85b50f84408a6e230f11886c0f9add0fd37cbdf0ea` |
| `scripts/phantom_taxonomy/orbit_harness_k16_s16_scc_nodes.csv` | 1241 | `31a1136da9802f1e17d94095c9c0b5746756c265a9a832ba74a8c91bb99f5b5c` |

Verification commands:

```text
cd /Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz
python3 scripts/phantom_taxonomy/scc_cw_certificate.py \
  --verify scripts/phantom_taxonomy/deterministic_k16_s16_residue_K_cw_certificate.json
cd lean
lake build CollatzShadowing.Generated.K16S16KDeterministicCW
```

## 12. Remaining Editorial Choices

Section 6.1 now contains a first paper-facing draft block.  Remaining
editorial choices:

- whether to write it as a v4 section, a standalone note, or a
  supplementary computational note;
- how much of the K20 smoke material to include in an appendix;
- whether to include full hash tables in the main text or appendix.
