# Exact Rational CW Certificates for the Empirical K0=16 SCC

These certificates strengthen the empirical Phase 7.6 bound table by
removing floating-point dependence from the matrix inequality.  The
matrices are still empirical, because their transition probabilities
come from the sampled orbit harness.  Given those matrices, however,
the checks below are exact rational verifications of

```text
(P v)_i <= (89/100) * v_i
```

for positive integer vectors `v` stored in the JSON certificate files.

| view | states | certificate | exact max ratio | decimal |
|---|---:|---|---:|---:|
| raw node | 1240 | `orbit_harness_k16_s16_scc_node_cw_certificate.json` | `439764459109/496636575879` | 0.885485444423 |
| `(K,L,b)` | 76 | `orbit_harness_k16_s16_scc_KL_cw_certificate.json` | `88036787882257/99446226949575` | 0.885270266985 |
| `(K,b)` | 37 | `orbit_harness_k16_s16_scc_K_cw_certificate.json` | `136756256754601/154382162832639` | 0.885829387575 |

Verification commands:

```bash
python3 scripts/phantom_taxonomy/scc_cw_certificate.py --verify scripts/phantom_taxonomy/orbit_harness_k16_s16_scc_node_cw_certificate.json
python3 scripts/phantom_taxonomy/scc_cw_certificate.py --verify scripts/phantom_taxonomy/orbit_harness_k16_s16_scc_KL_cw_certificate.json
python3 scripts/phantom_taxonomy/scc_cw_certificate.py --verify scripts/phantom_taxonomy/orbit_harness_k16_s16_scc_K_cw_certificate.json
```

All three return `status=OK`.
