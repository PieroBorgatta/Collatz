# Gate 10.B Generated FULL Provenance Check

Status: finite provenance check only.  This report does not prove
an infinite operator, spectral gap, Lasota-Yorke inequality,
Hennion, Keller-Liverani, Conjecture 6, or Collatz.

## T10CriticalSymbolic

| field | value |
|---|---:|
| source CSV | `collatz_75_critical_symbolic_edges.csv` |
| target T | 10 |
| rows | 100 |
| source states | 32 |
| normalized mismatches | 0 |
| compatible with A0 Haar conditional reading | `True` |

finite Haar/counting quotient over Z/2^T Z x H, grouped by source PhaseState

## T10J32HighBitTail

| field | value |
|---|---:|
| source CSV | `scripts/phantom_taxonomy/high_bit_tail_edges_T10_j32.csv` |
| target T | 10 |
| j_count | 32 |
| j_count power of two | `True` |
| rows | 1256 |
| source states | 60 |
| normalized mismatches | 0 |
| metadata mismatches | 0 |
| full = core + tail mismatches | 0 |
| compatible with A0 Haar conditional reading | `True` |

high-bit prefix Haar/counting quotient over Z/2^(T+log2(j_count)) Z x H; conditional interpretation applies to full, while core/tail is finite majority bookkeeping

## Interpretation

Both generated FULL matrices pass the finite provenance checks for
the conditional Gate-10.B interpretation.  This supports reading
their full rows as finite Haar/counting conditional expectations
onto source PhaseState.  It does not make PhaseState an exact
sourcewise sufficient statistic, and it does not promote core/tail
majority bookkeeping to an infinite operator decomposition.
