# Phantom Taxonomy at K0 = 16

Date: 2026-05-10
Updated: 2026-05-13

This note summarizes Phase 7 of the Lean/Python roadmap: taxonomy of
primitive cyclic-composition phantoms, rational representatives,
sampled episode graph construction, and empirical integration of the
new observed SCC.  The 2026-05-13 follow-up closes the deterministic
finite residue-cell transition gap for the declared `K0 = 16` scope.

## Scope

The original Phase-7 result was empirical but reproducible.  The
enumeration and rational representative computations are exact.  The
first episode graph and retention operator were sampled from integer
lifts, then the resulting empirical matrices were certified exactly by
rational Collatz-Wielandt inequalities.

Follow-up `F.1` replaces that sampled transition step, for the declared
finite residue-cell scope, with deterministic enumeration of every
residue cell attached to the observed `K0 = 16` SCC source states.  The
certified macro-state space is `(K,b)`.

## 7.1 Necklace Counts

Script: `scripts/phantom_taxonomy/necklace_counts.py`

The primitive cyclic-composition count is computed by Mobius inversion:

```text
M(K, ell) = (1/ell) * sum_{d | gcd(K, ell)}
              mu(d) * binom(K/d - 1, ell/d - 1).
```

Verification:

- direct canonical-rotation enumeration agrees with the formula for
  all `3 <= K <= 10`;
- the displayed `R(K)` values for `K = 3..20` reproduce Chang's table;
- output table: `scripts/phantom_taxonomy/necklace_counts_k3_20.csv`.

## 7.2 Rational Representatives

Script: `scripts/phantom_taxonomy/phantom_representatives.py`

For each expansive primitive cyclic composition
`w = (a_0, ..., a_{L-1})`, the script computes

```text
S_w(n) = (3^L n + C_w) / 2^A,
q_w = C_w / (2^A - 3^L).
```

Outputs:

- `scripts/phantom_taxonomy/phantom_representatives_k3_16.csv`
- `scripts/phantom_taxonomy/phantom_representatives_k3_20.csv`

Exact checks:

- `(2^A - 3^L) q_w = C_w`;
- `S_w(q_w) = q_w`;
- denominator of `q_w` is odd;
- per-`K` representative counts match `M_expanding`.

## 7.3 Orbit Harness

Script: `scripts/phantom_taxonomy/orbit_harness.py`

The harness samples integer lifts

```text
n = q_w mod 2^(bA+1) + t * 2^(bA+1)
```

then traces the odd Syracuse map and records monitored phantom hits.

Smoke outputs:

- `scripts/phantom_taxonomy/orbit_harness_k10_*`
- `scripts/phantom_taxonomy/orbit_harness_k16_smoke_*`

## 7.4 K0 = 16 SCC Run

Primary run:

```bash
python3 scripts/phantom_taxonomy/orbit_harness.py \
  --representatives scripts/phantom_taxonomy/phantom_representatives_k3_16.csv \
  --max-k 16 --b-max 2 --samples 8 --max-steps 1000 \
  --out-prefix scripts/phantom_taxonomy/orbit_harness_k16_full
```

Summary:

- 19952 traced orbits;
- all stopped below start within the step budget;
- 212324 episode events;
- 5041 observed directed edge types;
- 2401 observed nodes with at least one edge;
- one nontrivial SCC of size 1222.

Report:

- `notes/phantom_taxonomy_k16_scc_report.md`
- full SCC node list:
  `scripts/phantom_taxonomy/orbit_harness_k16_full_scc_nodes.csv`

Outcome: case (b).  A new large taxonomy SCC is observed, so the
`K0=20` no-new-SCC branch is not the immediate path.

## 7.6 Empirical Integration

Scripts:

- `scripts/phantom_taxonomy/scc_transfer_summary.py`
- `scripts/phantom_taxonomy/scc_collatz_wielandt.py`
- `scripts/phantom_taxonomy/scc_cw_certificate.py`
- `scripts/phantom_taxonomy/compare_cw_tables.py`

The SCC was integrated into empirical substochastic retention matrices.
Three views were tested:

- raw node labels;
- macro-state `(K,L,b)`;
- macro-state `(K,b)`.

At 8 dense lifts/source:

| view | states | CW upper |
|---|---:|---:|
| raw node | 1222 | 0.884991533363 |
| `(K,L,b)` | 72 | 0.884858364322 |
| `(K,b)` | 35 | 0.885502907588 |

At 16 dense lifts/source:

| view | states | CW upper |
|---|---:|---:|
| raw node | 1240 | 0.885485445971 |
| `(K,L,b)` | 76 | 0.885270267025 |
| `(K,b)` | 37 | 0.885829387560 |

The maximum drift between the two sampling budgets is less than
`0.0005`.

Stability report:

- `scripts/phantom_taxonomy/orbit_harness_k16_cw_stability.md`

## Exact Rational Certificates for the Empirical Matrices

For the 16-lift run, JSON certificates verify exact rational
inequalities

```text
(P v)_i <= (89/100) * v_i
```

for positive integer vectors `v`.

| view | states | exact max ratio |
|---|---:|---:|
| raw node | 1240 | `439764459109/496636575879` |
| `(K,L,b)` | 76 | `88036787882257/99446226949575` |
| `(K,b)` | 37 | `136756256754601/154382162832639` |

Certificate summary:

- `scripts/phantom_taxonomy/orbit_harness_k16_s16_scc_exact_cw_certificates.md`

Certificate files:

- `scripts/phantom_taxonomy/orbit_harness_k16_s16_scc_node_cw_certificate.json`
- `scripts/phantom_taxonomy/orbit_harness_k16_s16_scc_KL_cw_certificate.json`
- `scripts/phantom_taxonomy/orbit_harness_k16_s16_scc_K_cw_certificate.json`

## F.1 Deterministic Residue-Cell Closure

Script:

- `scripts/phantom_taxonomy/deterministic_residue_transfer.py`

The deterministic follow-up enumerates every finite residue subclass in
the declared scope:

```text
0 <= t < 2^4,
n0 = q_w mod 2^(b A_w + 1) + t * 2^(b A_w + 1).
```

For each raw SCC source state `(w,b)`, the script first verifies that
the canonical monitored hit at `n0` is the requested source.  Cells
owned by a stronger overlapping monitored class are counted as
shadowed.  The remaining canonical source cells are traced
deterministically until the next distinct monitored hit or until the
odd Syracuse orbit drops below its start.

Coverage:

| item | count |
|---|---:|
| raw SCC source nodes | 1240 |
| finite residue cells/source | 16 |
| total finite residue cells checked | 19840 |
| canonical source cells | 17671 |
| shadowed initial cells | 2169 |
| no-initial cells | 0 |
| budget exits | 0 |
| internal SCC transitions | 17176 |
| exits below start | 495 |

Deterministic transfer diagnostics:

| view | states | nonzero edge types | source events | retention mass | rho diagnostic |
|---|---:|---:|---:|---:|---:|
| raw node | 1240 | 1631 | 17671 | 0.971988 | 0.614114751961 |
| `(K,L,b)` | 76 | 300 | 17671 | 0.971988 | 0.682396808590 |
| `(K,b)` | 37 | 182 | 17671 | 0.971988 | 0.701094388677 |

The certified matrix is the `(K,b)` compression.  Its exact
Collatz-Wielandt certificate verifies

```text
(P v)_i <= (3/4) * v_i
```

with exact maximum ratio

```text
90833233962213/129559208330288 ≈ 0.701094388680.
```

Artifacts:

- `scripts/phantom_taxonomy/deterministic_k16_s16_residue_K_edges.csv`
- `scripts/phantom_taxonomy/deterministic_k16_s16_residue_source_coverage.csv`
- `scripts/phantom_taxonomy/deterministic_k16_s16_residue_manifest.json`
- `scripts/phantom_taxonomy/deterministic_k16_s16_residue_transfer_summary.md`
- `scripts/phantom_taxonomy/deterministic_k16_s16_residue_K_cw_certificate.json`
- `scripts/phantom_taxonomy/deterministic_k16_s16_residue_exact_cw_certificate.md`

## Interpretation

The `K0 = 16` taxonomy extension does not preserve the original small
paper-SCC topology.  It produces one large observed nontrivial SCC.
The original sampled substochastic retention operator for this SCC is
strongly subcritical in all tested views, with empirical
Collatz-Wielandt bounds around `0.885`, stable under doubling the
sampling budget.  The deterministic finite residue-cell follow-up gives
a stronger `(K,b)` certified bound below `3/4` in the declared finite
scope.

The most useful compression appears to be `(K,L,b)`: it reduces the
16-lift SCC from 1240 observed node states to 76 macro-states while
preserving the observed spectral bound to within `0.001`.

For the deterministic finite residue-cell certificate, the retained
certified compression is `(K,b)`, because the exact CW pipeline closes
there cleanly with the bound `3/4`.

## Residual Scope Note

The previous sampled-transition gap is closed for the declared finite
residue-cell scope.  This should still not be overstated as a symbolic
infinite residue-class theorem beyond that declared finite quotient.

This phase should now be cited as:

> deterministic finite residue-cell taxonomy integration at `K0 = 16`,
> with an exact rational `(K,b)` Collatz-Wielandt certificate.
