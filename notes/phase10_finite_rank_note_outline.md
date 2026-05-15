# Finite-Rank Computational Note Outline

Date: 2026-05-13

Status: outline for a standalone finite-rank computational note.  This
is not an analytic Phase-10 theorem and does not claim an infinite
transfer operator, a spectral gap, Conjecture 6, or the Collatz
conjecture.

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

## 6. Suggested Paper Structure

1. Introduction and finite scope.
2. Definition of the deterministic residue-cell shadowing model.
3. Construction of the finite substochastic `(K,b)` matrix.
4. Collatz-Wielandt finite certificate.
5. Lean formalization boundary.
6. Sensitivity checks.
7. Limitations and relation to Phase 10.
8. Reproducibility manifest.

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

## 10. Relationship to Phase 10

If Gate 10.B succeeds, this finite-rank certificate can be a baseline or
appendix.

Under the current reduction, Gate 10.B for the existing `FULL` matrices
means validating the `A0-averaged` interpretation:

```text
K_N^0 is an averaged PhaseState finite-rank quotient,
not an exact projection of the source-cell kernel.
```

If a collaborator rejects that interpretation, or if no Banach weak norm
can make it meaningful, Gate 10.B fails for the analytic branch.  In that
case this finite-rank certificate becomes the cleanest Phase-10 output:

```text
an honest finite theorem with exact arithmetic and Lean verification.
```

That outcome is mathematically respectable.  It is smaller than the
analytic ambition, but it does not rely on unproved projection,
compactness, or perturbation hypotheses.

## 11. Missing Text Before Drafting

The note still needs:

- the exact Lean-generation command or a decision to treat the generated
  Lean file as the stable artifact;
- a manifest/hash table for external reproducibility;
- a clean comparison paragraph distinguishing this finite certificate
  from the Phase-10 `A0-averaged` analytic operator program.
