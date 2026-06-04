# Phase 10 A0 Low-v2 Mechanism Probe

Date: 2026-05-25

Status: finite diagnostic for TODO `10.M` / A0W2.  This is not a proof.

## Context

After script `117`, the high-`v2` source-tail mass is an exact count:

```text
mu_N(v2 >= R) <= 2^-R.
```

The remaining A0 proof target is therefore:

```text
for every fixed R, prove D_N(v2 < R) -> 0.
```

## Script 118: Phase-by-Phase Decay

Command:

```text
python3 scripts/spectral_program/118_A0_low_v2_phase_decay_probe.py \
  --output-tag current_A0
```

Outputs:

```text
scripts/spectral_program/collatz_118_current_A0_A0_low_v2_phase_decay_probe_report.md
scripts/spectral_program/collatz_118_current_A0_A0_low_v2_phase_decay_probe_phase_fits.csv
scripts/spectral_program/collatz_118_current_A0_A0_low_v2_phase_decay_probe_latest_phase_rows.csv
```

Threshold low-`v2` fits:

```text
R=4:  alpha 0.611642619
R=6:  alpha 0.618811958
R=8:  alpha 0.599275586
R=10: alpha 0.595091262
R=12: alpha 0.597682614
R=14: alpha 0.595226457
```

For `v2 < 8`, the median per-phase alpha is:

```text
median low phase alpha = 0.6112066004
```

The latest dominant low phases are the expected mass families:

```text
0|3|h, 1|3|h, 0|1|h, 2|1|h.
```

The slowest fitted low phases in the current data are:

```text
7|3|h: alpha 0.2298668295
7|1|h: alpha 0.3420981079
6|1|h: alpha 0.4064120870
3|1|h: alpha 0.4142787183
```

These are slower but have much smaller latest contribution than the
dominant mass phases.

## Script 119: Return-Depth Mechanism

Command:

```text
.venv/bin/python scripts/spectral_program/119_A0_low_v2_return_depth_probe.py \
  --output-tag T14_j64_128_sample
```

Outputs:

```text
scripts/spectral_program/collatz_119_T14_j64_128_sample_A0_low_v2_return_depth_probe_report.md
scripts/spectral_program/collatz_119_T14_j64_128_sample_A0_low_v2_return_depth_probe_phase_summary.csv
scripts/spectral_program/collatz_119_T14_j64_128_sample_A0_low_v2_return_depth_probe_bin_summary.csv
```

Tested representative phases:

```text
0|3|0, 1|3|0, 3|1|0, 7|3|0.
```

For all four:

```text
prefix_l1 / half_l1 = 0.5
```

This confirms that the script-`111` prefix drift is exactly ordinary
dyadic block discrepancy:

```text
K_[0,2N) - K_[0,N) = (1/2) * (K_[N,2N) - K_[0,N)).
```

The largest drift pieces are not long-return tails.  They are mostly
medium-depth returns:

```text
step 11-25,
delta 0 or delta 1-3.
```

Example: for the slow phase `7|3|0`, the dominant piece is:

```text
step 11-25:
  prefix L1 piece = 0.003610610962
  half L1 piece   = 0.007221221924
```

The long-depth bins are small in this sample.

## Interpretation

The low-`v2` problem is not primarily a rare-tail problem.  The high-`v2`
mass tail is already exact, and long return-depth tails do not dominate
the sampled low-`v2` drift.

The remaining mechanism is dyadic discrepancy of bounded/medium-depth
return signatures over adjacent high-bit blocks.

The next proof target should be a residue-period or dependency-depth
lemma:

```text
bounded-depth return signatures have vanishing dyadic block discrepancy
inside each fixed source phase.
```

If such a lemma holds uniformly enough, then:

```text
D_N(v2 < R) -> 0
```

follows for fixed `R`, and script `117` supplies the `R -> infinity`
tail step.

## Next Diagnostic

Measure dependency depth directly:

```text
For fixed source phase and bounded return bin,
find the smallest m such that the destination/weight signature is
stable on t mod 2^m up to small exceptions.
```

If the exceptional mass of signatures requiring depth `> m` decays as
`m -> infinity`, this becomes a plausible proof route.

## Script 120: Dependency-Depth Check

Command:

```text
.venv/bin/python scripts/spectral_program/120_A0_dependency_depth_probe.py \
  --output-tag T14_j128_sample
```

Outputs:

```text
scripts/spectral_program/collatz_120_T14_j128_sample_A0_dependency_depth_probe_report.md
scripts/spectral_program/collatz_120_T14_j128_sample_A0_dependency_depth_probe_by_depth.csv
```

Tested phases:

```text
0|3|0, 7|3|0.
```

The simple finite-period hypothesis is not supported in this direct form.
For phase `0|3|0`, return-phase majority error decreases with depth:

```text
m=8:   count error 0.712411342, singleton 0
m=12:  count error 0.410966196, singleton 0
m=16:  count error 0.247757128, singleton 0.202980411
m=20:  count error 0.046751945, singleton 0.389220953
```

For the medium-return subset of `0|3|0`, the picture is worse:

```text
m=8:   count error 0.735467386, singleton 0
m=14:  count error 0.621122862, singleton 0.106905158
m=18:  count error 0.256938037, singleton 0.765021584
m=20:  count error 0.102633260, singleton 0.743848074
```

For the sparse slow phase `7|3|0`, error also falls mainly when cells are
small:

```text
return phase m=18: count error 0.214128035, singleton 0.600000000
return phase m=20: count error 0.066225166, singleton 0.529220779
```

## Updated Interpretation

The naive bounded-depth local-constancy lemma is probably false or too weak:
bounded/medium-depth return signatures are not determined by a small fixed
number of low 2-adic bits before the sample cells become sparse.

So the proof route should pivot from:

```text
finite residue-period determinism
```

to:

```text
2-adic discrepancy / Walsh-Haar cancellation for bounded-depth signatures.
```

This is still compatible with `D_N(v2 < R) -> 0`, but the mechanism is
mixing/cancellation over dyadic blocks rather than exact periodicity at a
small modulus.

The next diagnostic should compute the Walsh spectrum of the dominant
low-`v2` drift signals.  If high Walsh levels carry small total energy,
then dyadic block discrepancy can be attacked spectrally.

## Script 121: Walsh-Haar Spectrum

Command:

```text
.venv/bin/python scripts/spectral_program/121_A0_walsh_haar_probe.py \
  --output-tag T14_j128_sample
```

Outputs:

```text
scripts/spectral_program/collatz_121_T14_j128_sample_A0_walsh_haar_probe_report.md
scripts/spectral_program/collatz_121_T14_j128_sample_A0_walsh_haar_probe_by_scale.csv
```

The root Haar coefficient reproduces the script-`119` half-block
discrepancy.  For `return/phase`:

```text
phase    samples   root half L1     prefix L1
0|3|0    524288    0.000413223985   0.000206611992
7|3|0    4096      0.007874965668   0.003937482834
```

The energy distribution is not low-frequency smooth.  The finest Haar
levels carry most of the `L2` energy:

```text
0|3|0 return/phase:
  block size 2: L2 share 0.499915736
  block size 4: L2 share 0.250365838
  root:         L2 share 0.0000004697

7|3|0 return/phase:
  block size 2: L2 share 0.502945743
  block size 4: L2 share 0.249721893
  root:         L2 share 0.000351503
```

Thus the signal is highly oscillatory at fine scales, but the coarse/root
coefficient is tiny.  This is good news for prefix-drift decay, but it also
means the proof route is not a standard smoothness/low-frequency theorem.

The correct target is narrower:

```text
prove decay of the top dyadic Haar coefficient
for fixed low-v2 source phases,
without needing small total high-frequency energy.
```

Equivalently, prove dyadic block discrepancy decay:

```text
|| average over [0,N) - average over [N,2N) ||_1 -> 0.
```

This is exactly the A0W2/10.M content.

## Script 122: Top-Haar Decay Summary

Command:

```text
python3 scripts/spectral_program/122_A0_top_haar_decay_summary.py \
  --output-tag current_A0
```

Outputs:

```text
scripts/spectral_program/collatz_122_current_A0_A0_top_haar_decay_summary_report.md
scripts/spectral_program/collatz_122_current_A0_A0_top_haar_decay_summary_phase_fits.csv
scripts/spectral_program/collatz_122_current_A0_A0_top_haar_decay_summary_threshold_fits.csv
scripts/spectral_program/collatz_122_current_A0_A0_top_haar_decay_summary_case_points.csv
```

This script does not retrace orbits.  It rewrites the existing
script-`111` A0 phase-strata data in the proof-facing Haar language:

```text
root_haar_l1(N) = ||mean_[N,2N) - mean_[0,N)||_1
                = 2 * prefix_row_l1(N).
```

The threshold exponents are therefore numerically the same as in
script `118`, but the mathematical object has changed from a generic
drift feature to the top dyadic block-discrepancy coefficient.

Threshold top-Haar fits:

```text
v2 < 4:  alpha 0.6116426187, latest root component 0.0004701730001
v2 < 6:  alpha 0.6188119578, latest root component 0.0004878383379
v2 < 8:  alpha 0.5992755856, latest root component 0.0005326722352
v2 < 10: alpha 0.5950912623, latest root component 0.0005525503968
v2 < 12: alpha 0.5976826136, latest root component 0.0005636666702
v2 < 14: alpha 0.5952264566, latest root component 0.0005687926729
```

The latest total root-Haar drift is:

```text
total_root_haar_D = 0.0005715489444
```

Thus the low-`v2` cutoff `v2 < 8` already accounts for about:

```text
0.9319800875
```

of the latest total root drift.

The theorem-oriented reduction is now:

```text
For every fixed low-v2 phase p,
  root_haar_l1_p(N) -> 0.

Since {p : v2(p) < R} is finite for fixed R,
  D_N(v2 < R) -> 0.
```

Together with the exact high-`v2` source-tail count from script `117`,
this is the cleanest current A0 weak-bridge route.  It is still not a
Collatz proof: the missing item is a structural dyadic discrepancy lemma
explaining why those top Haar coefficients vanish.
