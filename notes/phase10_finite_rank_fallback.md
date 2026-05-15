# Phase 10 Finite-Rank Fallback

Date: 2026-05-13

Status: fallback theorem-design note.  This note does not claim a proof
of the Collatz conjecture, Conjecture 6, an infinite-operator spectral
gap, or convergence of finite matrices to an infinite operator.

Related files:

- `lean/CollatzShadowing/Bound.lean`
- `lean/CollatzShadowing/Generated/K16S16KDeterministicCW.lean`
- `scripts/phantom_taxonomy/deterministic_residue_transfer.py`
- `scripts/phantom_taxonomy/deterministic_k16_s16_residue_manifest.json`
- `scripts/phantom_taxonomy/deterministic_k16_s16_residue_transfer_summary.md`
- `scripts/phantom_taxonomy/deterministic_k16_s16_residue_K_cw_certificate.json`
- `scripts/phantom_taxonomy/deterministic_k16_s16_residue_exact_cw_certificate.md`
- `notes/phase10_finite_rank_note_outline.md`
- `lean/TODO.md`

## 1. Purpose

Gate 10.B may fail: the finite matrices may not be projections,
compressions, Galerkin approximants, or Ulam discretizations of a
canonical infinite transfer operator.

If that happens, Phase 10 should still have an honest output:

```text
a certified finite-rank / finite-residue-cell contraction statement
for a declared finite shadowing model.
```

The fallback must be advertised only within its finite scope.

## 2. Existing certified baseline

The current deterministic baseline is:

```text
lean/CollatzShadowing/Generated/K16S16KDeterministicCW.lean
```

It imports a deterministic finite residue-cell `(K,b)` certificate
generated from:

```text
scripts/phantom_taxonomy/deterministic_k16_s16_residue_K_cw_certificate.json
```

Finite state space:

```text
K16S16KDeterministicState = Fin 37.
```

The generated state labels are:

```text
K10:b1, K10:b2, ..., K16:b1, K3:b1, ..., K9:b2.
```

The matrix orientation in the generated Lean file is incoming:

```text
M(dst,src) = transition probability from source src to destination dst.
```

The imported finite matrix has:

- `37` macro-states;
- `182` nonzero internal edge types;
- alpha `3/4`;
- max-ratio node `K11:b2`;
- exact max ratio

```text
90833233962213 / 129559208330288 < 3/4.
```

The Lean file proves:

```text
k16s16KDeterministicMaxRatio_lt_alpha
k16s16KDeterministicFiniteCWCertificate
k16s16KDeterministicGeneratedSpectralRadiusBound
```

The last theorem states the finite spectral-radius bound for the
realified generated matrix:

```text
spectralRadius R (nnrealMatrixToReal k16s16KDeterministicMatrix)
  <= (k16s16KDeterministicAlphaNNReal : R>=0inf).
```

## 3. What is already theorem/certificate

Certified in Lean:

- the exact rational inequality

```text
90833233962213 * 4 < 3 * 129559208330288;
```

- positivity of the generated CW vector on `Fin 37`;
- per-row cleared-denominator inequalities;
- a `FiniteCWCertificate` for the generated 37-state matrix;
- the Mathlib spectral-radius bound for the realified finite matrix.

Verified by Python before Lean generation:

- the deterministic residue-cell enumeration;
- the exact JSON CW certificate;
- sensitivity checks at `lift_bits = 5` and `lift_bits = 6`, with exact
  max ratios

```text
7332495524923 / 10616480126384  ~= 0.690671054590,
64869145309473 / 97226913303232 ~= 0.667193301788.
```

These sensitivity checks are not yet separate Lean imports unless
generated/imported explicitly.

## 4. What this does not certify

The K16 deterministic finite-rank certificate does not certify:

- a statement for all Collatz trajectories;
- convergence as `K0 -> infinity`;
- convergence as `lift_bits -> infinity`;
- a spectral gap for an infinite transfer operator;
- a Lasota-Yorke inequality;
- Keller-Liverani stability;
- a proof of Conjecture 6;
- a proof that the Phase 10 analytic program works.

It certifies only the declared finite deterministic residue-cell model.

## 5. Candidate finite-rank theorem statement

The paper-facing fallback statement should have the following shape.

```text
Theorem candidate (finite deterministic residue-cell contraction).

Fix K0 = 16, scc_rank = 1, lift_bits = 4, max_steps = 1000, and the
declared deterministic residue-cell construction from
deterministic_residue_transfer.py.  Let M_K,b be the resulting 37-state
substochastic transition matrix on the compressed macro-state space
(K,b), with incoming orientation.

There exists a positive vector v in R_{>0}^{37} such that

  (M_K,b v)_i <= (3/4) v_i

for every row i.  Consequently the finite real matrix M_K,b has

  spectralRadius(M_K,b) <= 3/4.
```

The proof is finite:

1. deterministic enumeration produces the rational matrix;
2. the generated positive vector is checked positive;
3. all row inequalities are checked exactly after clearing
   denominators;
4. the generic Lean Collatz-Wielandt bridge in `Bound.lean` gives the
   spectral-radius corollary.

### 5.1 Lean-citable theorem package

A paper or standalone note should cite the generated Lean statements in
this order:

1. `k16s16KDeterministicMaxRatio_lt_alpha`;
2. `k16s16KDeterministicVectorNat_pos`;
3. `k16s16KDeterministicFiniteCWCertificate`;
4. `k16s16KDeterministicGeneratedSpectralRadiusBound`.

The first item is the headline rational inequality.  The third item is
the finite Collatz-Wielandt certificate.  The fourth item is the finite
spectral-radius consequence.  None of these statements contains an
infinite transfer operator or an asymptotic limit.

The relevant orientation is:

```text
row/destination i receives mass from source j,
so the generated matrix is M(i,j).
```

This is compatible with the generated finite CW bridge, but it must not
be silently identified with a Ruelle preimage operator.

### 5.2 Minimal standalone theorem bundle

The autonomous finite-rank note should contain exactly four layers.

Layer 1: finite model declaration.

```text
Input SCC source list, representative table, max_k, lift_bits,
max_steps, and compression map to (K,b).
```

Layer 2: deterministic enumeration lemma.

```text
For each raw SCC source state, the generator partitions the finite
lift classes into 2^lift_bits residue subclasses and classifies every
one of them as canonical, shadowed initial, no-initial, budget exit, or
exit below start.
```

For the production K16 certificate, this layer is computationally
verified by the coverage file and manifest:

```text
raw source nodes       = 1240,
total residue cells    = 19840,
canonical source cells = 17671,
shadowed initial cells = 2169,
budget exits           = 0.
```

Layer 3: finite matrix construction.

```text
The (K,b) transition matrix has 37 states, 182 nonzero internal edge
types, 17671 source events, 17176 internal transitions, and 495 exits
below start.
```

Layer 4: exact CW certificate.

```text
There is a positive integer vector v such that M v <= (3/4) v,
verified by exact rational arithmetic and imported into Lean.
```

This bundle is theorem-producing even if Gate 10.B fails, because it
does not need an infinite projection hypothesis.

## 6. Missing pieces for an autonomous note

To make the fallback a standalone finite-rank computational note, the
following must be written explicitly.

Scope definition:

- exact definition of the finite residue-cell model;
- exact meaning of `K0 = 16`, `S16`, `lift_bits = 4`, `scc_rank = 1`;
- exact definition of the compressed `(K,b)` macro-state;
- orientation convention for the matrix.

Reproducibility:

- command line that regenerates the deterministic edge CSVs;
- command line that regenerates the JSON CW certificate;
- command line that regenerates the Lean file;
- hash or manifest of generated artifacts if the note is external.

Known production commands:

```text
python3 scripts/phantom_taxonomy/deterministic_residue_transfer.py \
  --representatives scripts/phantom_taxonomy/phantom_representatives_k3_16.csv \
  --scc-nodes scripts/phantom_taxonomy/orbit_harness_k16_s16_scc_nodes.csv \
  --scc-rank 1 \
  --max-k 16 \
  --lift-bits 4 \
  --max-steps 1000 \
  --out-prefix scripts/phantom_taxonomy/deterministic_k16_s16_residue

python3 scripts/phantom_taxonomy/scc_cw_certificate.py \
  --verify scripts/phantom_taxonomy/deterministic_k16_s16_residue_K_cw_certificate.json

lake build CollatzShadowing.Generated.K16S16KDeterministicCW
```

The note still needs the exact command that generated the Lean import
from the JSON certificate, unless the generated file itself is treated
as the stable artifact and the generator is documented elsewhere.

Mathematical boundary:

- statement that the theorem is finite-rank only;
- statement that sensitivity at `lift_bits = 5,6` is evidence, not a
  theorem for all `lift_bits`;
- statement that no infinite projection is assumed.

Lean boundary:

- cite `k16s16KDeterministicFiniteCWCertificate`;
- cite `k16s16KDeterministicGeneratedSpectralRadiusBound`;
- decide whether to generate Lean files for the sensitivity checks.

## 7. Extension to `K0 = 20`

The extension should not be advertised before it is generated and
checked.  The concrete plan is:

1. rerun deterministic residue-cell enumeration with `--max-k 20`;
2. recompute the SCC or declare the exact finite component being tested;
3. rebuild the compressed `(K,b)` matrix;
4. compute an exact rational CW certificate;
5. verify the JSON certificate independently;
6. generate a Lean import with a distinct declaration prefix;
7. run `lake build` on the generated module;
8. compare the K20 ratio with the K16 ratio without claiming monotonicity
   unless a proof is supplied.

Failure modes:

- the state space grows too much for the current generator;
- no positive CW vector below `3/4` is found;
- sensitivity in `lift_bits` worsens;
- K20 changes the SCC structure in a way that invalidates direct
  comparison with K16.

## 7.1 K20 smoke preflight

A small K20 smoke run was performed only to test feasibility.  It is not
a production certificate and should not be cited as the K20 result.

Sampled SCC smoke command:

```text
python3 scripts/phantom_taxonomy/orbit_harness.py \
  --representatives scripts/phantom_taxonomy/phantom_representatives_k3_20.csv \
  --max-k 20 \
  --b-max 1 \
  --samples 2 \
  --max-steps 1000 \
  --out-prefix scripts/phantom_taxonomy/orbit_harness_k20_smoke
```

Smoke output:

- traced orbits: `32198`;
- all stopped below start within budget;
- event count: `251564`;
- edge types: `21682`.

SCC report:

```text
python3 scripts/phantom_taxonomy/scc_report.py \
  --edges scripts/phantom_taxonomy/orbit_harness_k20_smoke_edges.csv \
  --representatives scripts/phantom_taxonomy/phantom_representatives_k3_20.csv \
  --out notes/phantom_taxonomy_k20_smoke_scc_report.md \
  --components-csv scripts/phantom_taxonomy/orbit_harness_k20_smoke_scc_nodes.csv
```

SCC smoke output:

- observed nodes: `15156`;
- edge types: `21682`;
- nontrivial SCCs: `1`;
- largest SCC size: `5802`.

Deterministic residue-cell smoke on the smoke SCC, compressed to `(K,b)`:

```text
python3 scripts/phantom_taxonomy/deterministic_residue_transfer.py \
  --representatives scripts/phantom_taxonomy/phantom_representatives_k3_20.csv \
  --scc-nodes scripts/phantom_taxonomy/orbit_harness_k20_smoke_scc_nodes.csv \
  --scc-rank 1 \
  --max-k 20 \
  --lift-bits 4 \
  --max-steps 1000 \
  --modes K \
  --out-prefix scripts/phantom_taxonomy/deterministic_k20_smoke_residue
```

Deterministic smoke output:

- raw source nodes: `5802`;
- total residue classes: `92832`;
- canonical source classes: `76038`;
- shadowed initial classes: `16794`;
- budget classes: `0`;
- `(K,b)` states: `38`;
- nonzero internal edge types: `254`;
- source events: `76038`;
- exits: `4807`;
- retention: `0.936782`;
- rho diagnostic: approximately `0.666730647491`.

Exact rational CW smoke check:

```text
python3 scripts/phantom_taxonomy/scc_cw_certificate.py \
  --edge-csv scripts/phantom_taxonomy/deterministic_k20_smoke_residue_K_edges.csv \
  --alpha 3/4 \
  --certificate scripts/phantom_taxonomy/deterministic_k20_smoke_residue_K_cw_certificate.json
```

Verification:

```text
python3 scripts/phantom_taxonomy/scc_cw_certificate.py \
  --verify scripts/phantom_taxonomy/deterministic_k20_smoke_residue_K_cw_certificate.json
```

Result:

```text
max_ratio = 42001755821431 / 62996587868160 < 3/4,
max_node = K4:b4,
status = OK.
```

Interpretation:

- the K20 deterministic pipeline is technically feasible on this smoke
  SCC;
- the `(K,b)` smoke matrix again admits a CW certificate below `3/4`;
- because the SCC input is only a small sampled smoke graph, this is not
  a production K20 finite-rank theorem.

Production K20 still requires at least:

1. a full sampled K20 SCC run with declared `b` and sample budget;
2. a stability comparison across sample budgets;
3. deterministic residue-cell closure on the selected production SCC;
4. generated Lean import with a fresh declaration prefix;
5. a clear statement that K20 does not imply monotone convergence from
   K16 unless separately proved.

Additional K20 promotion criteria:

- the input SCC must be declared as production rather than smoke;
- the deterministic residue-cell summary must have a title and metadata
  matching `K0 = 20`;
- the production certificate must have a distinct Lean module and
  declaration prefix;
- sensitivity checks should be regenerated from permanent artifacts, not
  only temporary files;
- the K20 theorem statement should be parallel to K16 but not presented
  as a monotonic strengthening unless a comparison theorem is proved.

## 8. Publication routing

Use this branch as:

- a baseline section inside v4 if the analytic branch remains coherent;
- a standalone finite-rank computational note if the `A0-averaged`
  interpretation is rejected or Gate 10.B otherwise fails;
- an appendix/certificate archive if a stronger analytic paper is later
  written.

Do not use this branch as evidence for an infinite spectral gap unless
Gate 10.B and the averaged finite-rank convergence hypotheses are
solved.

The standalone-note outline is now separated in:

```text
notes/phase10_finite_rank_note_outline.md
```

That outline is the preferred starting point if Branch B becomes the
main Phase-10 deliverable.
