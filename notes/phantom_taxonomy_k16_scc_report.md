# Augmented Phantom Taxonomy SCC Report

Input edge CSV: `scripts/phantom_taxonomy/orbit_harness_k16_full_edges.csv`

- Nodes with at least one observed edge: 2401
- Directed observed edge types: 5041
- Nontrivial SCCs: 1
- Largest nontrivial SCC size: 1222

## Paper-SCC Comparison

The paper §8 SCC is expressed in empirical cycle labels `(k,c,b)`,
whereas this Phase-7 taxonomy graph is expressed in primitive
cyclic-composition labels `(K,L,word,b)`. Exact comparison is only
possible when a taxonomy representative has the same rational `q_w`
as one of the listed empirical representatives.

Recognized empirical representatives present in the observed graph:

- `K9:L7:w1-1-1-1-1-2-2:b1` -> paper empirical k=12 cycle 1
- `K9:L7:w1-1-1-1-1-2-2:b2` -> paper empirical k=12 cycle 1

## Nontrivial SCCs

### SCC 1

- Size: 1222
- Internal edge types: 3857
- Internal observed transition weight: 182961
- Sample nodes:

  - `K10:L7:w1-1-1-1-1-1-4:b1`
  - `K10:L7:w1-1-1-1-1-2-3:b1`
  - `K10:L7:w1-1-1-1-1-3-2:b1`
  - `K10:L7:w1-1-1-1-2-1-3:b1`
  - `K10:L7:w1-1-1-1-2-2-2:b1`
  - `K10:L7:w1-1-1-1-2-2-2:b2`
  - `K10:L7:w1-1-1-1-3-1-2:b1`
  - `K10:L7:w1-1-1-2-1-1-3:b1`
  - `K10:L7:w1-1-1-2-1-1-3:b2`
  - `K10:L7:w1-1-1-2-1-2-2:b1`
  - `K10:L7:w1-1-1-2-2-1-2:b1`
  - `K10:L7:w1-1-1-3-1-1-2:b1`
