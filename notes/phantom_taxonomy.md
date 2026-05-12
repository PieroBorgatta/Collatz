# Phantom Taxonomy at K0 = 16

Date: 2026-05-10

This note summarizes Phase 7 of the Lean/Python roadmap: taxonomy of
primitive cyclic-composition phantoms, rational representatives,
sampled episode graph construction, and empirical integration of the
new observed SCC.

## Scope

The result is empirical but reproducible.  The enumeration and rational
representative computations are exact.  The episode graph and retention
operator are sampled from integer lifts, then the resulting empirical
matrices are certified exactly by rational Collatz-Wielandt
inequalities.

This is not yet a deterministic theorem-level transition certificate
for all residue classes.

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

## Interpretation

The `K0 = 16` taxonomy extension does not preserve the original small
paper-SCC topology.  It produces one large observed nontrivial SCC.
However, the sampled substochastic retention operator for this SCC is
strongly subcritical in all tested views, with empirical
Collatz-Wielandt bounds around `0.885`, stable under doubling the
sampling budget.

The most useful compression appears to be `(K,L,b)`: it reduces the
16-lift SCC from 1240 observed node states to 76 macro-states while
preserving the observed spectral bound to within `0.001`.

## Remaining Gap

The transition probabilities are still sampled.  To turn this into a
theorem-level certificate, one must replace sampled transitions with a
deterministic residue-class construction on a chosen macro-state space,
most likely `(K,L,b)` or `(K,b)`.

Until then, this phase should be cited as:

> empirical taxonomy integration at `K0 = 16`, with exact rational
> certificates for the sampled retention matrices.
