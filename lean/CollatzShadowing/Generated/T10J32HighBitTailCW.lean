/-
Generated numerical spectral certificate boundary for the high-bit matrix.

Source CSV: `../scripts/phantom_taxonomy/high_bit_tail_edges_T10_j32.csv`
Target T: 10
j_count: 32
Alpha: 97/2000 = 0.0485

This module records the paper-facing Lean statement for Phase 8.7.  The
integer Collatz-Wielandt vector and the exact rational row checks are
produced by `scripts/phantom_taxonomy/lean_t10j32_cw.py`; expanding all
224 row certificates directly in Lean is currently too slow for the
local Mathlib kernel, so the checked external certificate is imported at
this boundary as a single trusted generated fact.
-/

import CollatzShadowing.Generated.T10J32HighBitTail

namespace CollatzShadowing
namespace Generated

open scoped ENNReal NNReal

/-- Alpha used by the `T = 10`, `j = 32` certificate: `97/2000 = 0.0485`. -/
def t10j32HighBitTailAlpha : ProbabilityEntry where
  numerator := 97
  denominator := 2000
  denominator_pos := by decide

/-- Alpha as an `NNReal`. -/
noncomputable def t10j32HighBitTailAlphaNNReal : NNReal :=
  t10j32HighBitTailAlpha.toNNReal

/--
Trusted generated certificate boundary for the exact rational
Collatz-Wielandt check on the imported `T = 10`, `j = 32` full matrix.

The corresponding Python generator constructs a positive integer vector
and verifies every cleared rational row inequality exactly before this
Lean fact is exposed.
-/
axiom t10j32HighBitTailCWCertificate :
    CWCertificate t10j32HighBitTailFull
      (onesBasis 13)
      t10j32HighBitTailAlphaNNReal

/--
Paper Section 7 numerical certificate: the real spectral radius of the
generated full `T = 10`, `j = 32` matrix is at most `97/2000 = 0.0485`.
-/
theorem t10j32HighBitTailSpectralRadiusBound :
    spectralRadius ℝ (nnrealMatrixToReal t10j32HighBitTailFull) ≤
      (t10j32HighBitTailAlphaNNReal : ℝ≥0∞) :=
  spectralRadius_le_of_CWCertificate
    t10j32HighBitTailFull
    (onesBasis 13)
    t10j32HighBitTailAlphaNNReal
    t10j32HighBitTailCWCertificate

/-- The same bound stated with the literal rational `97/2000`. -/
theorem t10j32HighBitTailSpectralRadiusBound_97_2000 :
    spectralRadius ℝ (nnrealMatrixToReal t10j32HighBitTailFull) ≤
      (((97 : NNReal) / (2000 : NNReal)) : ℝ≥0∞) := by
  simpa [t10j32HighBitTailAlphaNNReal, t10j32HighBitTailAlpha,
    ProbabilityEntry.toNNReal] using t10j32HighBitTailSpectralRadiusBound

end Generated
end CollatzShadowing
