/-
Generated finite A0 return-branch data for the Phase-10 weak branch.

Source JSON:
  scripts/spectral_program/collatz_126_current_A0_v2lt8_A0_return_branch_affine_probe_branches.json

Generated from the script-126 sampled branch extraction.  These rows say:
for each sampled point in a row, the observed return satisfies

  source_t = q*u+r,
  next_t   = a*u+b,
  delta    = bitLength(next_t) - bitLength(source_t).

The fields `refinedQ/refinedR/refinedA/refinedB` further refine the
source progression so that the sampled finite destination state is fixed:

  source_t = refinedQ*v+refinedR,
  next_t   = refinedA*v+refinedB.

The auxiliary word-cylinder table records the exact 2-adic cylinder
arithmetic for the distinct valuation words visible in this sampled
extraction, plus the affine no-drop prefix check.  This is stronger than
a sample check for the valuation word, but it still does not certify the
global "first return" condition of the shadowing automaton.

This file records sampled finite branch data only.  It does not prove
that the return label persists for every `u`, and it does not prove the
Phase-10 low-v2 limit.
-/

import CollatzShadowing.WeakBridge

set_option linter.style.longLine false

namespace CollatzShadowing
namespace Generated

/-- One sampled A0 return branch after residue reparameterization. -/
structure A0ReturnBranch where
  phase : String
  dst : String
  step : Nat
  word : List Nat
  sampleCount : Nat
  q : Nat
  r : Nat
  a : Nat
  b : Nat
  dstV2 : Nat
  dstOdd : Nat
  dstH : Nat
  stateModBits : Nat
  uResidueMod : Nat
  uResidue : Nat
  refinedQ : Nat
  refinedR : Nat
  refinedA : Nat
  refinedB : Nat
  formulaFailures : Nat
  deltaFailures : Nat
  refinedFormulaFailures : Nat
  refinedStateFailures : Nat
  exactOnSamples : Bool
  deriving Repr, DecidableEq

/--
Sampled `v2 < 8` return branches from script 126.

Rows with no sampled returns are not represented here; they contribute no
return branch to this finite extraction table.
-/
def a0ReturnBranchesV2Lt8 : List A0ReturnBranch :=
  [
    { phase := "0|3|0", dst := "0|3|1", step := 6,
      word := [1, 1, 2, 1, 1, 1], sampleCount := 64,
      q := 128, r := 3, a := 729, b := 19,
      dstV2 := 0, dstOdd := 3, dstH := 1,
      stateModBits := 2, uResidueMod := 4, uResidue := 0,
      refinedQ := 512, refinedR := 3, refinedA := 2916, refinedB := 19,
      formulaFailures := 0, deltaFailures := 0,
      refinedFormulaFailures := 0, refinedStateFailures := 0, exactOnSamples := true },
    { phase := "0|3|1", dst := "0|3|2", step := 6,
      word := [1, 1, 2, 1, 1, 1], sampleCount := 64,
      q := 128, r := 3, a := 729, b := 19,
      dstV2 := 0, dstOdd := 3, dstH := 2,
      stateModBits := 2, uResidueMod := 4, uResidue := 0,
      refinedQ := 512, refinedR := 3, refinedA := 2916, refinedB := 19,
      formulaFailures := 0, deltaFailures := 0,
      refinedFormulaFailures := 0, refinedStateFailures := 0, exactOnSamples := true },
    { phase := "0|3|2", dst := "0|3|3", step := 6,
      word := [1, 1, 2, 1, 1, 1], sampleCount := 64,
      q := 128, r := 3, a := 729, b := 19,
      dstV2 := 0, dstOdd := 3, dstH := 3,
      stateModBits := 2, uResidueMod := 4, uResidue := 0,
      refinedQ := 512, refinedR := 3, refinedA := 2916, refinedB := 19,
      formulaFailures := 0, deltaFailures := 0,
      refinedFormulaFailures := 0, refinedStateFailures := 0, exactOnSamples := true },
    { phase := "0|3|3", dst := "0|3|0", step := 6,
      word := [1, 1, 2, 1, 1, 1], sampleCount := 64,
      q := 128, r := 3, a := 729, b := 19,
      dstV2 := 0, dstOdd := 3, dstH := 0,
      stateModBits := 2, uResidueMod := 4, uResidue := 0,
      refinedQ := 512, refinedR := 3, refinedA := 2916, refinedB := 19,
      formulaFailures := 0, deltaFailures := 0,
      refinedFormulaFailures := 0, refinedStateFailures := 0, exactOnSamples := true },
    { phase := "2|3|0", dst := "0|3|1", step := 4,
      word := [1, 1, 2, 1], sampleCount := 64,
      q := 32, r := 12, a := 81, b := 31,
      dstV2 := 0, dstOdd := 3, dstH := 1,
      stateModBits := 2, uResidueMod := 4, uResidue := 0,
      refinedQ := 128, refinedR := 12, refinedA := 324, refinedB := 31,
      formulaFailures := 0, deltaFailures := 0,
      refinedFormulaFailures := 0, refinedStateFailures := 0, exactOnSamples := true },
    { phase := "2|3|1", dst := "0|3|2", step := 4,
      word := [1, 1, 2, 1], sampleCount := 64,
      q := 32, r := 12, a := 81, b := 31,
      dstV2 := 0, dstOdd := 3, dstH := 2,
      stateModBits := 2, uResidueMod := 4, uResidue := 0,
      refinedQ := 128, refinedR := 12, refinedA := 324, refinedB := 31,
      formulaFailures := 0, deltaFailures := 0,
      refinedFormulaFailures := 0, refinedStateFailures := 0, exactOnSamples := true },
    { phase := "2|3|2", dst := "0|3|3", step := 4,
      word := [1, 1, 2, 1], sampleCount := 64,
      q := 32, r := 12, a := 81, b := 31,
      dstV2 := 0, dstOdd := 3, dstH := 3,
      stateModBits := 2, uResidueMod := 4, uResidue := 0,
      refinedQ := 128, refinedR := 12, refinedA := 324, refinedB := 31,
      formulaFailures := 0, deltaFailures := 0,
      refinedFormulaFailures := 0, refinedStateFailures := 0, exactOnSamples := true },
    { phase := "2|3|3", dst := "0|3|0", step := 4,
      word := [1, 1, 2, 1], sampleCount := 64,
      q := 32, r := 12, a := 81, b := 31,
      dstV2 := 0, dstOdd := 3, dstH := 0,
      stateModBits := 2, uResidueMod := 4, uResidue := 0,
      refinedQ := 128, refinedR := 12, refinedA := 324, refinedB := 31,
      formulaFailures := 0, deltaFailures := 0,
      refinedFormulaFailures := 0, refinedStateFailures := 0, exactOnSamples := true },
    { phase := "3|1|0", dst := "3|1|1", step := 9,
      word := [1, 1, 2, 1, 1, 1, 2, 2, 1], sampleCount := 64,
      q := 4096, r := 8, a := 19683, b := 40,
      dstV2 := 3, dstOdd := 1, dstH := 1,
      stateModBits := 5, uResidueMod := 32, uResidue := 0,
      refinedQ := 131072, refinedR := 8, refinedA := 629856, refinedB := 40,
      formulaFailures := 0, deltaFailures := 0,
      refinedFormulaFailures := 0, refinedStateFailures := 0, exactOnSamples := true },
    { phase := "3|1|1", dst := "3|1|2", step := 9,
      word := [1, 1, 2, 1, 1, 1, 2, 2, 1], sampleCount := 64,
      q := 4096, r := 8, a := 19683, b := 40,
      dstV2 := 3, dstOdd := 1, dstH := 2,
      stateModBits := 5, uResidueMod := 32, uResidue := 0,
      refinedQ := 131072, refinedR := 8, refinedA := 629856, refinedB := 40,
      formulaFailures := 0, deltaFailures := 0,
      refinedFormulaFailures := 0, refinedStateFailures := 0, exactOnSamples := true },
    { phase := "3|1|2", dst := "3|1|3", step := 9,
      word := [1, 1, 2, 1, 1, 1, 2, 2, 1], sampleCount := 64,
      q := 4096, r := 8, a := 19683, b := 40,
      dstV2 := 3, dstOdd := 1, dstH := 3,
      stateModBits := 5, uResidueMod := 32, uResidue := 0,
      refinedQ := 131072, refinedR := 8, refinedA := 629856, refinedB := 40,
      formulaFailures := 0, deltaFailures := 0,
      refinedFormulaFailures := 0, refinedStateFailures := 0, exactOnSamples := true },
    { phase := "3|1|3", dst := "3|1|0", step := 9,
      word := [1, 1, 2, 1, 1, 1, 2, 2, 1], sampleCount := 64,
      q := 4096, r := 8, a := 19683, b := 40,
      dstV2 := 3, dstOdd := 1, dstH := 0,
      stateModBits := 5, uResidueMod := 32, uResidue := 0,
      refinedQ := 131072, refinedR := 8, refinedA := 629856, refinedB := 40,
      formulaFailures := 0, deltaFailures := 0,
      refinedFormulaFailures := 0, refinedStateFailures := 0, exactOnSamples := true },
    { phase := "5|1|0", dst := "1|1|1", step := 10,
      word := [1, 1, 2, 1, 1, 1, 2, 3, 2, 1], sampleCount := 64,
      q := 32768, r := 32, a := 59049, b := 58,
      dstV2 := 1, dstOdd := 1, dstH := 1,
      stateModBits := 3, uResidueMod := 8, uResidue := 0,
      refinedQ := 262144, refinedR := 32, refinedA := 472392, refinedB := 58,
      formulaFailures := 0, deltaFailures := 0,
      refinedFormulaFailures := 0, refinedStateFailures := 0, exactOnSamples := true },
    { phase := "5|1|1", dst := "1|1|2", step := 10,
      word := [1, 1, 2, 1, 1, 1, 2, 3, 2, 1], sampleCount := 64,
      q := 32768, r := 32, a := 59049, b := 58,
      dstV2 := 1, dstOdd := 1, dstH := 2,
      stateModBits := 3, uResidueMod := 8, uResidue := 0,
      refinedQ := 262144, refinedR := 32, refinedA := 472392, refinedB := 58,
      formulaFailures := 0, deltaFailures := 0,
      refinedFormulaFailures := 0, refinedStateFailures := 0, exactOnSamples := true },
    { phase := "5|1|2", dst := "1|1|3", step := 10,
      word := [1, 1, 2, 1, 1, 1, 2, 3, 2, 1], sampleCount := 64,
      q := 32768, r := 32, a := 59049, b := 58,
      dstV2 := 1, dstOdd := 1, dstH := 3,
      stateModBits := 3, uResidueMod := 8, uResidue := 0,
      refinedQ := 262144, refinedR := 32, refinedA := 472392, refinedB := 58,
      formulaFailures := 0, deltaFailures := 0,
      refinedFormulaFailures := 0, refinedStateFailures := 0, exactOnSamples := true },
    { phase := "5|1|3", dst := "1|1|0", step := 10,
      word := [1, 1, 2, 1, 1, 1, 2, 3, 2, 1], sampleCount := 64,
      q := 32768, r := 32, a := 59049, b := 58,
      dstV2 := 1, dstOdd := 1, dstH := 0,
      stateModBits := 3, uResidueMod := 8, uResidue := 0,
      refinedQ := 262144, refinedR := 32, refinedA := 472392, refinedB := 58,
      formulaFailures := 0, deltaFailures := 0,
      refinedFormulaFailures := 0, refinedStateFailures := 0, exactOnSamples := true }
  ]

/-- Total sampled branch rows imported from script 126. -/
def a0ReturnBranchesV2Lt8RowCount : Nat :=
  16

/-- Sum of sampled formula/delta failure counters in the imported rows. -/
def a0ReturnBranchesV2Lt8FailureTotal : Nat :=
  a0ReturnBranchesV2Lt8.foldl
    (fun acc br =>
      acc + br.formulaFailures + br.deltaFailures
        + br.refinedFormulaFailures + br.refinedStateFailures
        + if br.exactOnSamples then 0 else 1)
    0

/--
Internal consistency checks for the imported branch rows:

* the valuation word length equals the observed return step;
* the target slope equals `3^step`;
* the source denominator/residue modulus equals `2^(sum word)`.
* the destination-refined progression is the expected residue
  subprogression of the valuation-word branch.

These are arithmetic checks on the imported rows, not a proof that the
same branch persists outside the sampled points.
-/
def a0ReturnBranchesV2Lt8ScaleFailureTotal : Nat :=
  a0ReturnBranchesV2Lt8.foldl
    (fun acc br =>
      acc
        + (if br.word.length = br.step then 0 else 1)
        + (if br.a = 3 ^ br.step then 0 else 1)
        + (if br.q = 2 ^ br.word.sum then 0 else 1)
        + (if br.stateModBits = br.dstV2 + 2 then 0 else 1)
        + (if br.uResidueMod = 2 ^ br.stateModBits then 0 else 1)
        + (if br.refinedQ = br.q * br.uResidueMod then 0 else 1)
        + (if br.refinedR = br.q * br.uResidue + br.r then 0 else 1)
        + (if br.refinedA = br.a * br.uResidueMod then 0 else 1)
        + (if br.refinedB = br.a * br.uResidue + br.b then 0 else 1))
    0

theorem a0ReturnBranchesV2Lt8_length :
    a0ReturnBranchesV2Lt8.length = a0ReturnBranchesV2Lt8RowCount := by
  norm_num [a0ReturnBranchesV2Lt8, a0ReturnBranchesV2Lt8RowCount]

theorem a0ReturnBranchesV2Lt8_sample_checks_zero :
    a0ReturnBranchesV2Lt8FailureTotal = 0 := by
  norm_num [a0ReturnBranchesV2Lt8FailureTotal, a0ReturnBranchesV2Lt8]

theorem a0ReturnBranchesV2Lt8_scale_checks_zero :
    a0ReturnBranchesV2Lt8ScaleFailureTotal = 0 := by
  norm_num [a0ReturnBranchesV2Lt8ScaleFailureTotal, a0ReturnBranchesV2Lt8]

/--
Exact word-cylinder arithmetic for the distinct sampled `v2 < 8` return
words in script 126.

`wordResidue mod 2^wordModBits` is the exact odd-source cylinder for the
valuation word.  In the A0 coordinate `n = targetResidue + 2^8*t`, this
induces `t = tWordResidue mod 2^tWordModBits`.  The listed branch
progression `t = q*u+r` implies that congruence.

This table does not prove that the branch is the first return; it only
certifies the valuation-word cylinder, the source split arithmetic, and
the affine no-drop prefix check for the listed branch shapes.
-/
structure A0WordCylinder where
  word : List Nat
  q : Nat
  r : Nat
  wordModBits : Nat
  wordResidue : Nat
  tWordModBits : Nat
  tWordResidue : Nat
  wordCongruenceFailures : Nat
  dropAffineFailures : Nat
  branchImpliesWordCongruence : Bool
  noDropCertificateRows : Nat
  arithmeticCertificateRows : Nat
  deriving Repr, DecidableEq

def a0WordCylindersV2Lt8 : List A0WordCylinder :=
  [
    { word := [1, 1, 2, 1, 1, 1], q := 128, r := 3,
      wordModBits := 8, wordResidue := 103,
      tWordModBits := 0, tWordResidue := 0,
      wordCongruenceFailures := 0, dropAffineFailures := 0,
      branchImpliesWordCongruence := true, noDropCertificateRows := 4,
      arithmeticCertificateRows := 4 },
    { word := [1, 1, 2, 1], q := 32, r := 12,
      wordModBits := 6, wordResidue := 39,
      tWordModBits := 0, tWordResidue := 0,
      wordCongruenceFailures := 0, dropAffineFailures := 0,
      branchImpliesWordCongruence := true, noDropCertificateRows := 4,
      arithmeticCertificateRows := 4 },
    { word := [1, 1, 2, 1, 1, 1, 2, 2, 1], q := 4096, r := 8,
      wordModBits := 13, wordResidue := 2151,
      tWordModBits := 5, tWordResidue := 8,
      wordCongruenceFailures := 0, dropAffineFailures := 0,
      branchImpliesWordCongruence := true, noDropCertificateRows := 4,
      arithmeticCertificateRows := 4 },
    { word := [1, 1, 2, 1, 1, 1, 2, 3, 2, 1], q := 32768, r := 32,
      wordModBits := 16, wordResidue := 8295,
      tWordModBits := 8, tWordResidue := 32,
      wordCongruenceFailures := 0, dropAffineFailures := 0,
      branchImpliesWordCongruence := true, noDropCertificateRows := 4,
      arithmeticCertificateRows := 4 }
  ]

def a0WordCylindersV2Lt8FailureTotal : Nat :=
  a0WordCylindersV2Lt8.foldl
    (fun acc row =>
      acc
        + row.wordCongruenceFailures
        + row.dropAffineFailures
        + (if row.branchImpliesWordCongruence then 0 else 1)
        + (if row.noDropCertificateRows = row.arithmeticCertificateRows then 0 else 1)
        + (if row.wordModBits = row.word.sum + 1 then 0 else 1)
        + (if row.q = 2 ^ row.word.sum then 0 else 1)
        + (if row.q % (2 ^ row.tWordModBits) = 0 then 0 else 1)
        + (if row.r % (2 ^ row.tWordModBits) = row.tWordResidue then 0 else 1))
    0

def a0WordCylindersV2Lt8ArithmeticRows : Nat :=
  a0WordCylindersV2Lt8.foldl
    (fun acc row => acc + row.arithmeticCertificateRows)
    0

theorem a0WordCylindersV2Lt8_failure_total_zero :
    a0WordCylindersV2Lt8FailureTotal = 0 := by
  norm_num [a0WordCylindersV2Lt8FailureTotal, a0WordCylindersV2Lt8]

theorem a0WordCylindersV2Lt8_arithmetic_rows :
    a0WordCylindersV2Lt8ArithmeticRows = a0ReturnBranchesV2Lt8RowCount := by
  norm_num [a0WordCylindersV2Lt8ArithmeticRows, a0WordCylindersV2Lt8,
    a0ReturnBranchesV2Lt8RowCount]

/-- Summary of a complete finite dyadic-prefix script-126 run. -/
structure A0PrefixBranchSummary where
  prefixBits : Nat
  totalSamples : Nat
  returnSamples : Nat
  dropSamples : Nat
  valuationTailSamples : Nat
  stepTailSamples : Nat
  branchRows : Nat
  branchSampleCountTotal : Nat
  branchSampleCountCoverageFailures : Nat
  exactFailures : Nat
  nonintegerBranches : Nat
  wordCongruenceFailures : Nat
  dropAffineFailures : Nat
  noDropCertificateRows : Nat
  branchWordCertificateFailures : Nat
  arithmeticCertificateRows : Nat
  refinedFormulaFailures : Nat
  refinedStateFailures : Nat
  labelPrefixIntegralityFailures : Nat
  labelIntermediateVisibleFailures : Nat
  labelIntermediateTargetVisibleFailures : Nat
  labelIntermediateCompetingVisibleFailures : Nat
  labelIntermediateTargetVisiblePrefixes : Nat
  labelIntermediateCompetingVisiblePrefixes : Nat
  labelIntermediateVisibleK10C1Failures : Nat
  labelIntermediateVisibleK11C1Failures : Nat
  labelIntermediateVisibleK12C1Failures : Nat
  labelIntermediateVisibleK12C2Failures : Nat
  labelIntermediateVisibleK20C1Failures : Nat
  labelIntermediateProbeTotal : Nat
  labelIntermediateProbeCandidateSelected : Nat
  labelIntermediateProbeTargetSelected : Nat
  labelIntermediateProbeCompetingSelected : Nat
  labelIntermediateProbeNoneSelected : Nat
  labelIntermediateProbeSameStepReturn : Nat
  labelIntermediateProbeEarlyTargetReturn : Nat
  labelIntermediateProbeNoReturnByFinal : Nat
  labelIntermediateProbeTerminalByFinal : Nat
  labelIntermediateMultiprobeTotal : Nat
  labelIntermediateMultiprobeSameStepReturn : Nat
  labelIntermediateMultiprobeEarlyTargetReturn : Nat
  labelIntermediateMultiprobeNoReturnByFinal : Nat
  labelIntermediateMultiprobeTerminalByFinal : Nat
  labelIntermediateTargetMultiprobeTotal : Nat
  labelIntermediateTargetMultiprobeSameStepReturn : Nat
  labelIntermediateTargetMultiprobeEarlyTargetReturn : Nat
  labelIntermediateTargetMultiprobeNoReturnByFinal : Nat
  labelIntermediateTargetMultiprobeTerminalByFinal : Nat
  labelIntermediateMultiprobeNoReturnK10C1 : Nat
  labelIntermediateMultiprobeNoReturnK11C1 : Nat
  labelIntermediateMultiprobeNoReturnK12C1 : Nat
  labelIntermediateMultiprobeNoReturnK12C2 : Nat
  labelIntermediateMultiprobeNoReturnK20C1 : Nat
  labelIntermediateMultiprobeNoReturnExtendedLaterTarget : Nat
  labelIntermediateMultiprobeNoReturnExtendedTerminal : Nat
  labelIntermediateMultiprobeNoReturnExtendedUnresolved : Nat
  labelIntermediateMultiprobeNoReturnLaterTargetMinDelta : Nat
  labelIntermediateMultiprobeNoReturnLaterTargetMaxDelta : Nat
  labelIntermediateMultiprobeNoReturnContinuationSupported : Nat
  labelIntermediateMultiprobeNoReturnContinuationIntegralityFailures : Nat
  labelIntermediateMultiprobeNoReturnContinuationNoDropFailures : Nat
  labelIntermediateMultiprobeNoReturnActualPrefixMatches : Nat
  labelIntermediateMultiprobeNoReturnActualSuffixTargetWordMatches : Nat
  labelIntermediateMultiprobeNoReturnActualContinuationSupported : Nat
  labelIntermediateMultiprobeNoReturnActualContinuationIntegralityFailures : Nat
  labelIntermediateMultiprobeNoReturnActualContinuationNoDropFailures : Nat
  labelIntermediateMultiprobeNoReturnActualRefinedContinuationSupported : Nat
  labelIntermediateMultiprobeNoReturnActualRefinedContinuationFailures : Nat
  labelIntermediateMultiprobeNoReturnActualRefinedExtraBitsMin : Nat
  labelIntermediateMultiprobeNoReturnActualRefinedExtraBitsMax : Nat
  labelIntermediateCompetingNoLaterTargetIntersections : Nat
  labelIntermediateCompetingLaterTargetIntersections : Nat
  labelIntermediateTargetPersistentVisibility : Nat
  labelIntermediateTargetMissingPriorVisibility : Nat
  labelIntermediateTargetNoPriorCompetingIntersections : Nat
  labelIntermediateTargetPriorCompetingIntersections : Nat
  labelIntermediateTargetHighLiftCovered : Nat
  labelIntermediateTargetLowOnlyVisible : Nat
  labelFinalTargetLowFailures : Nat
  labelFinalTargetHighLiftFailures : Nat
  labelFinalTargetHighLiftMinModBits : Nat
  labelFinalTargetHighLiftMaxModBits : Nat
  labelFinalCompetingFailures : Nat
  labelSplitResolutionCertificate : Nat
  labelStatusProvedConstantTargetB1 : Nat
  labelStatusTargetHighLiftBoundary : Nat
  labelStatusBlockedLabelCongruence : Nat
  labelStatusBlockedPrefixIntegrality : Nat
  highLiftContinuationSupportedRows : Nat
  highLiftContinuationStepDeltaMin : Nat
  highLiftContinuationStepDeltaMax : Nat
  highLiftContinuationIntegralityFailures : Nat
  highLiftContinuationNoDropFailures : Nat
  deriving Repr, DecidableEq

/--
Complete finite-prefix branch extraction summaries for `v2 < 8`,
odd residues `{1,3}`, and `h < 4`.

These are finite-prefix enumerations only.  They do not assert an
infinite residue-class partition.
-/
def a0CompletePrefixSummariesV2Lt8 : List A0PrefixBranchSummary :=
  [
    { prefixBits := 12, totalSamples := 16320, returnSamples := 1652,
      dropSamples := 14548, valuationTailSamples := 120, stepTailSamples := 0,
      branchRows := 860, branchSampleCountTotal := 1652,
      branchSampleCountCoverageFailures := 0,
      exactFailures := 0, nonintegerBranches := 0,
      wordCongruenceFailures := 0, dropAffineFailures := 0,
      noDropCertificateRows := 860, branchWordCertificateFailures := 0,
      arithmeticCertificateRows := 860,
      refinedFormulaFailures := 0, refinedStateFailures := 0,
      labelPrefixIntegralityFailures := 0,
      labelIntermediateVisibleFailures := 216,
      labelIntermediateTargetVisibleFailures := 12,
      labelIntermediateCompetingVisibleFailures := 204,
      labelIntermediateTargetVisiblePrefixes := 12,
      labelIntermediateCompetingVisiblePrefixes := 204,
      labelIntermediateVisibleK10C1Failures := 0,
      labelIntermediateVisibleK11C1Failures := 156,
      labelIntermediateVisibleK12C1Failures := 48,
      labelIntermediateVisibleK12C2Failures := 12,
      labelIntermediateVisibleK20C1Failures := 0,
      labelIntermediateProbeTotal := 216,
      labelIntermediateProbeCandidateSelected := 216,
      labelIntermediateProbeTargetSelected := 12,
      labelIntermediateProbeCompetingSelected := 204,
      labelIntermediateProbeNoneSelected := 0,
      labelIntermediateProbeSameStepReturn := 216,
      labelIntermediateProbeEarlyTargetReturn := 0,
      labelIntermediateProbeNoReturnByFinal := 0,
      labelIntermediateProbeTerminalByFinal := 0,
      labelIntermediateMultiprobeTotal := 1728,
      labelIntermediateMultiprobeSameStepReturn := 1728,
      labelIntermediateMultiprobeEarlyTargetReturn := 0,
      labelIntermediateMultiprobeNoReturnByFinal := 0,
      labelIntermediateMultiprobeTerminalByFinal := 0,
      labelIntermediateTargetMultiprobeTotal := 96,
      labelIntermediateTargetMultiprobeSameStepReturn := 96,
      labelIntermediateTargetMultiprobeEarlyTargetReturn := 0,
      labelIntermediateTargetMultiprobeNoReturnByFinal := 0,
      labelIntermediateTargetMultiprobeTerminalByFinal := 0,
      labelIntermediateMultiprobeNoReturnK10C1 := 0,
      labelIntermediateMultiprobeNoReturnK11C1 := 0,
      labelIntermediateMultiprobeNoReturnK12C1 := 0,
      labelIntermediateMultiprobeNoReturnK12C2 := 0,
      labelIntermediateMultiprobeNoReturnK20C1 := 0,
      labelIntermediateMultiprobeNoReturnExtendedLaterTarget := 0,
      labelIntermediateMultiprobeNoReturnExtendedTerminal := 0,
      labelIntermediateMultiprobeNoReturnExtendedUnresolved := 0,
      labelIntermediateMultiprobeNoReturnLaterTargetMinDelta := 0,
      labelIntermediateMultiprobeNoReturnLaterTargetMaxDelta := 0,
      labelIntermediateMultiprobeNoReturnContinuationSupported := 0,
      labelIntermediateMultiprobeNoReturnContinuationIntegralityFailures := 0,
      labelIntermediateMultiprobeNoReturnContinuationNoDropFailures := 0,
      labelIntermediateMultiprobeNoReturnActualPrefixMatches := 0,
      labelIntermediateMultiprobeNoReturnActualSuffixTargetWordMatches := 0,
      labelIntermediateMultiprobeNoReturnActualContinuationSupported := 0,
      labelIntermediateMultiprobeNoReturnActualContinuationIntegralityFailures := 0,
      labelIntermediateMultiprobeNoReturnActualContinuationNoDropFailures := 0,
      labelIntermediateMultiprobeNoReturnActualRefinedContinuationSupported := 0,
      labelIntermediateMultiprobeNoReturnActualRefinedContinuationFailures := 0,
      labelIntermediateMultiprobeNoReturnActualRefinedExtraBitsMin := 0,
      labelIntermediateMultiprobeNoReturnActualRefinedExtraBitsMax := 0,
      labelIntermediateCompetingNoLaterTargetIntersections := 204,
      labelIntermediateCompetingLaterTargetIntersections := 0,
      labelIntermediateTargetPersistentVisibility := 0,
      labelIntermediateTargetMissingPriorVisibility := 12,
      labelIntermediateTargetNoPriorCompetingIntersections := 12,
      labelIntermediateTargetPriorCompetingIntersections := 0,
      labelIntermediateTargetHighLiftCovered := 12,
      labelIntermediateTargetLowOnlyVisible := 0,
      labelFinalTargetLowFailures := 0,
      labelFinalTargetHighLiftFailures := 860,
      labelFinalTargetHighLiftMinModBits := 7,
      labelFinalTargetHighLiftMaxModBits := 7,
      labelFinalCompetingFailures := 0,
      labelSplitResolutionCertificate := 860,
      labelStatusProvedConstantTargetB1 := 0,
      labelStatusTargetHighLiftBoundary := 656,
      labelStatusBlockedLabelCongruence := 204,
      labelStatusBlockedPrefixIntegrality := 0,
      highLiftContinuationSupportedRows := 860,
      highLiftContinuationStepDeltaMin := 6,
      highLiftContinuationStepDeltaMax := 6,
      highLiftContinuationIntegralityFailures := 0,
      highLiftContinuationNoDropFailures := 0 },
    { prefixBits := 13, totalSamples := 32640, returnSamples := 3352,
      dropSamples := 29040, valuationTailSamples := 240, stepTailSamples := 8,
      branchRows := 1564, branchSampleCountTotal := 3352,
      branchSampleCountCoverageFailures := 0,
      exactFailures := 0, nonintegerBranches := 0,
      wordCongruenceFailures := 0, dropAffineFailures := 0,
      noDropCertificateRows := 1564, branchWordCertificateFailures := 0,
      arithmeticCertificateRows := 1564,
      refinedFormulaFailures := 0, refinedStateFailures := 0,
      labelPrefixIntegralityFailures := 0,
      labelIntermediateVisibleFailures := 376,
      labelIntermediateTargetVisibleFailures := 16,
      labelIntermediateCompetingVisibleFailures := 360,
      labelIntermediateTargetVisiblePrefixes := 16,
      labelIntermediateCompetingVisiblePrefixes := 360,
      labelIntermediateVisibleK10C1Failures := 0,
      labelIntermediateVisibleK11C1Failures := 268,
      labelIntermediateVisibleK12C1Failures := 92,
      labelIntermediateVisibleK12C2Failures := 16,
      labelIntermediateVisibleK20C1Failures := 0,
      labelIntermediateProbeTotal := 376,
      labelIntermediateProbeCandidateSelected := 376,
      labelIntermediateProbeTargetSelected := 16,
      labelIntermediateProbeCompetingSelected := 360,
      labelIntermediateProbeNoneSelected := 0,
      labelIntermediateProbeSameStepReturn := 376,
      labelIntermediateProbeEarlyTargetReturn := 0,
      labelIntermediateProbeNoReturnByFinal := 0,
      labelIntermediateProbeTerminalByFinal := 0,
      labelIntermediateMultiprobeTotal := 3008,
      labelIntermediateMultiprobeSameStepReturn := 3008,
      labelIntermediateMultiprobeEarlyTargetReturn := 0,
      labelIntermediateMultiprobeNoReturnByFinal := 0,
      labelIntermediateMultiprobeTerminalByFinal := 0,
      labelIntermediateTargetMultiprobeTotal := 128,
      labelIntermediateTargetMultiprobeSameStepReturn := 128,
      labelIntermediateTargetMultiprobeEarlyTargetReturn := 0,
      labelIntermediateTargetMultiprobeNoReturnByFinal := 0,
      labelIntermediateTargetMultiprobeTerminalByFinal := 0,
      labelIntermediateMultiprobeNoReturnK10C1 := 0,
      labelIntermediateMultiprobeNoReturnK11C1 := 0,
      labelIntermediateMultiprobeNoReturnK12C1 := 0,
      labelIntermediateMultiprobeNoReturnK12C2 := 0,
      labelIntermediateMultiprobeNoReturnK20C1 := 0,
      labelIntermediateMultiprobeNoReturnExtendedLaterTarget := 0,
      labelIntermediateMultiprobeNoReturnExtendedTerminal := 0,
      labelIntermediateMultiprobeNoReturnExtendedUnresolved := 0,
      labelIntermediateMultiprobeNoReturnLaterTargetMinDelta := 0,
      labelIntermediateMultiprobeNoReturnLaterTargetMaxDelta := 0,
      labelIntermediateMultiprobeNoReturnContinuationSupported := 0,
      labelIntermediateMultiprobeNoReturnContinuationIntegralityFailures := 0,
      labelIntermediateMultiprobeNoReturnContinuationNoDropFailures := 0,
      labelIntermediateMultiprobeNoReturnActualPrefixMatches := 0,
      labelIntermediateMultiprobeNoReturnActualSuffixTargetWordMatches := 0,
      labelIntermediateMultiprobeNoReturnActualContinuationSupported := 0,
      labelIntermediateMultiprobeNoReturnActualContinuationIntegralityFailures := 0,
      labelIntermediateMultiprobeNoReturnActualContinuationNoDropFailures := 0,
      labelIntermediateMultiprobeNoReturnActualRefinedContinuationSupported := 0,
      labelIntermediateMultiprobeNoReturnActualRefinedContinuationFailures := 0,
      labelIntermediateMultiprobeNoReturnActualRefinedExtraBitsMin := 0,
      labelIntermediateMultiprobeNoReturnActualRefinedExtraBitsMax := 0,
      labelIntermediateCompetingNoLaterTargetIntersections := 360,
      labelIntermediateCompetingLaterTargetIntersections := 0,
      labelIntermediateTargetPersistentVisibility := 0,
      labelIntermediateTargetMissingPriorVisibility := 16,
      labelIntermediateTargetNoPriorCompetingIntersections := 16,
      labelIntermediateTargetPriorCompetingIntersections := 0,
      labelIntermediateTargetHighLiftCovered := 16,
      labelIntermediateTargetLowOnlyVisible := 0,
      labelFinalTargetLowFailures := 0,
      labelFinalTargetHighLiftFailures := 1564,
      labelFinalTargetHighLiftMinModBits := 7,
      labelFinalTargetHighLiftMaxModBits := 7,
      labelFinalCompetingFailures := 0,
      labelSplitResolutionCertificate := 1564,
      labelStatusProvedConstantTargetB1 := 0,
      labelStatusTargetHighLiftBoundary := 1212,
      labelStatusBlockedLabelCongruence := 352,
      labelStatusBlockedPrefixIntegrality := 0,
      highLiftContinuationSupportedRows := 1564,
      highLiftContinuationStepDeltaMin := 6,
      highLiftContinuationStepDeltaMax := 6,
      highLiftContinuationIntegralityFailures := 0,
      highLiftContinuationNoDropFailures := 0 },
    { prefixBits := 14, totalSamples := 65280, returnSamples := 6748,
      dropSamples := 58040, valuationTailSamples := 484, stepTailSamples := 8,
      branchRows := 2868, branchSampleCountTotal := 6748,
      branchSampleCountCoverageFailures := 0,
      exactFailures := 0, nonintegerBranches := 0,
      wordCongruenceFailures := 0, dropAffineFailures := 0,
      noDropCertificateRows := 2868, branchWordCertificateFailures := 0,
      arithmeticCertificateRows := 2868,
      refinedFormulaFailures := 0, refinedStateFailures := 0,
      labelPrefixIntegralityFailures := 0,
      labelIntermediateVisibleFailures := 744,
      labelIntermediateTargetVisibleFailures := 64,
      labelIntermediateCompetingVisibleFailures := 680,
      labelIntermediateTargetVisiblePrefixes := 64,
      labelIntermediateCompetingVisiblePrefixes := 680,
      labelIntermediateVisibleK10C1Failures := 8,
      labelIntermediateVisibleK11C1Failures := 472,
      labelIntermediateVisibleK12C1Failures := 200,
      labelIntermediateVisibleK12C2Failures := 64,
      labelIntermediateVisibleK20C1Failures := 0,
      labelIntermediateProbeTotal := 744,
      labelIntermediateProbeCandidateSelected := 744,
      labelIntermediateProbeTargetSelected := 64,
      labelIntermediateProbeCompetingSelected := 680,
      labelIntermediateProbeNoneSelected := 0,
      labelIntermediateProbeSameStepReturn := 744,
      labelIntermediateProbeEarlyTargetReturn := 0,
      labelIntermediateProbeNoReturnByFinal := 0,
      labelIntermediateProbeTerminalByFinal := 0,
      labelIntermediateMultiprobeTotal := 5952,
      labelIntermediateMultiprobeSameStepReturn := 5944,
      labelIntermediateMultiprobeEarlyTargetReturn := 0,
      labelIntermediateMultiprobeNoReturnByFinal := 8,
      labelIntermediateMultiprobeTerminalByFinal := 0,
      labelIntermediateTargetMultiprobeTotal := 512,
      labelIntermediateTargetMultiprobeSameStepReturn := 512,
      labelIntermediateTargetMultiprobeEarlyTargetReturn := 0,
      labelIntermediateTargetMultiprobeNoReturnByFinal := 0,
      labelIntermediateTargetMultiprobeTerminalByFinal := 0,
      labelIntermediateMultiprobeNoReturnK10C1 := 0,
      labelIntermediateMultiprobeNoReturnK11C1 := 0,
      labelIntermediateMultiprobeNoReturnK12C1 := 8,
      labelIntermediateMultiprobeNoReturnK12C2 := 0,
      labelIntermediateMultiprobeNoReturnK20C1 := 0,
      labelIntermediateMultiprobeNoReturnExtendedLaterTarget := 8,
      labelIntermediateMultiprobeNoReturnExtendedTerminal := 0,
      labelIntermediateMultiprobeNoReturnExtendedUnresolved := 0,
      labelIntermediateMultiprobeNoReturnLaterTargetMinDelta := 6,
      labelIntermediateMultiprobeNoReturnLaterTargetMaxDelta := 6,
      labelIntermediateMultiprobeNoReturnContinuationSupported := 0,
      labelIntermediateMultiprobeNoReturnContinuationIntegralityFailures := 8,
      labelIntermediateMultiprobeNoReturnContinuationNoDropFailures := 0,
      labelIntermediateMultiprobeNoReturnActualPrefixMatches := 8,
      labelIntermediateMultiprobeNoReturnActualSuffixTargetWordMatches := 8,
      labelIntermediateMultiprobeNoReturnActualContinuationSupported := 0,
      labelIntermediateMultiprobeNoReturnActualContinuationIntegralityFailures := 8,
      labelIntermediateMultiprobeNoReturnActualContinuationNoDropFailures := 0,
      labelIntermediateMultiprobeNoReturnActualRefinedContinuationSupported := 8,
      labelIntermediateMultiprobeNoReturnActualRefinedContinuationFailures := 0,
      labelIntermediateMultiprobeNoReturnActualRefinedExtraBitsMin := 4,
      labelIntermediateMultiprobeNoReturnActualRefinedExtraBitsMax := 4,
      labelIntermediateCompetingNoLaterTargetIntersections := 680,
      labelIntermediateCompetingLaterTargetIntersections := 0,
      labelIntermediateTargetPersistentVisibility := 0,
      labelIntermediateTargetMissingPriorVisibility := 64,
      labelIntermediateTargetNoPriorCompetingIntersections := 64,
      labelIntermediateTargetPriorCompetingIntersections := 0,
      labelIntermediateTargetHighLiftCovered := 64,
      labelIntermediateTargetLowOnlyVisible := 0,
      labelFinalTargetLowFailures := 0,
      labelFinalTargetHighLiftFailures := 2868,
      labelFinalTargetHighLiftMinModBits := 7,
      labelFinalTargetHighLiftMaxModBits := 7,
      labelFinalCompetingFailures := 0,
      labelSplitResolutionCertificate := 2868,
      labelStatusProvedConstantTargetB1 := 0,
      labelStatusTargetHighLiftBoundary := 2176,
      labelStatusBlockedLabelCongruence := 692,
      labelStatusBlockedPrefixIntegrality := 0,
      highLiftContinuationSupportedRows := 2868,
      highLiftContinuationStepDeltaMin := 6,
      highLiftContinuationStepDeltaMax := 6,
      highLiftContinuationIntegralityFailures := 0,
      highLiftContinuationNoDropFailures := 0 }
  ]

/-- Total failure counters across the imported complete-prefix summaries. -/
def a0CompletePrefixSummariesV2Lt8FailureTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row =>
      acc + row.exactFailures + row.nonintegerBranches
        + row.wordCongruenceFailures + row.dropAffineFailures
        + row.branchWordCertificateFailures
        + row.refinedFormulaFailures + row.refinedStateFailures
        + row.labelPrefixIntegralityFailures
        + row.labelFinalTargetLowFailures
        + row.labelFinalCompetingFailures
        + row.highLiftContinuationIntegralityFailures
        + row.highLiftContinuationNoDropFailures)
    0

/--
Open label-gate congruence counts.

These are not arithmetic failures.  `labelIntermediateVisibleFailures`
counts congruence classes on which an intermediate prefix may acquire a
phantom label and must be split or controlled.  `labelFinalTargetHighLiftFailures`
counts congruence classes on which the final target can lift from
`b = 1` to `b >= 2`.
-/
def a0CompletePrefixSummariesV2Lt8LabelOpenTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row =>
      acc + row.labelIntermediateVisibleFailures
        + row.labelFinalTargetHighLiftFailures)
    0

def a0CompletePrefixSummariesV2Lt8LabelStatusCoverageFailureTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row =>
      acc +
        if row.labelStatusProvedConstantTargetB1
            + row.labelStatusTargetHighLiftBoundary
            + row.labelStatusBlockedLabelCongruence
            + row.labelStatusBlockedPrefixIntegrality
          = row.branchRows then 0 else 1)
    0

def a0CompletePrefixSummariesV2Lt8IntermediateTargetVisibleTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row => acc + row.labelIntermediateTargetVisibleFailures)
    0

def a0CompletePrefixSummariesV2Lt8IntermediateCompetingVisibleTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row => acc + row.labelIntermediateCompetingVisibleFailures)
    0

def a0CompletePrefixSummariesV2Lt8IntermediateSplitFailureTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row =>
      acc
        + (if row.labelIntermediateTargetVisibleFailures
              + row.labelIntermediateCompetingVisibleFailures
            = row.labelIntermediateVisibleFailures then 0 else 1)
        + (if row.labelIntermediateTargetVisiblePrefixes
              + row.labelIntermediateCompetingVisiblePrefixes
            = row.labelIntermediateVisibleFailures then 0 else 1))
    0

def a0CompletePrefixSummariesV2Lt8IntermediateK10C1VisibleTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row => acc + row.labelIntermediateVisibleK10C1Failures)
    0

def a0CompletePrefixSummariesV2Lt8IntermediateK11C1VisibleTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row => acc + row.labelIntermediateVisibleK11C1Failures)
    0

def a0CompletePrefixSummariesV2Lt8IntermediateK12C1VisibleTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row => acc + row.labelIntermediateVisibleK12C1Failures)
    0

def a0CompletePrefixSummariesV2Lt8IntermediateK12C2VisibleTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row => acc + row.labelIntermediateVisibleK12C2Failures)
    0

def a0CompletePrefixSummariesV2Lt8IntermediateK20C1VisibleTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row => acc + row.labelIntermediateVisibleK20C1Failures)
    0

def a0CompletePrefixSummariesV2Lt8IntermediateRecordSplitFailureTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row =>
      acc +
        if row.labelIntermediateVisibleK10C1Failures
            + row.labelIntermediateVisibleK11C1Failures
            + row.labelIntermediateVisibleK12C1Failures
            + row.labelIntermediateVisibleK12C2Failures
            + row.labelIntermediateVisibleK20C1Failures
          = row.labelIntermediateVisibleFailures then 0 else 1)
    0

def a0CompletePrefixSummariesV2Lt8IntermediateProbeTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row => acc + row.labelIntermediateProbeTotal)
    0

def a0CompletePrefixSummariesV2Lt8IntermediateProbeFailureTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row =>
      acc
        + (if row.labelIntermediateProbeTotal
            = row.labelIntermediateVisibleFailures then 0 else 1)
        + (if row.labelIntermediateProbeCandidateSelected
            = row.labelIntermediateProbeTotal then 0 else 1)
        + (if row.labelIntermediateProbeTargetSelected
              + row.labelIntermediateProbeCompetingSelected
              + row.labelIntermediateProbeNoneSelected
            = row.labelIntermediateProbeTotal then 0 else 1)
        + (if row.labelIntermediateProbeSameStepReturn
              + row.labelIntermediateProbeEarlyTargetReturn
              + row.labelIntermediateProbeNoReturnByFinal
              + row.labelIntermediateProbeTerminalByFinal
            = row.labelIntermediateProbeTotal then 0 else 1)
        + row.labelIntermediateProbeEarlyTargetReturn
        + row.labelIntermediateProbeNoReturnByFinal
        + row.labelIntermediateProbeTerminalByFinal)
    0

def a0CompletePrefixSummariesV2Lt8IntermediateCompetingNoLaterTargetTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row => acc + row.labelIntermediateCompetingNoLaterTargetIntersections)
    0

def a0CompletePrefixSummariesV2Lt8IntermediateMultiprobeTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row => acc + row.labelIntermediateMultiprobeTotal)
    0

def a0CompletePrefixSummariesV2Lt8IntermediateMultiprobeEarlyTargetTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row => acc + row.labelIntermediateMultiprobeEarlyTargetReturn)
    0

def a0CompletePrefixSummariesV2Lt8IntermediateMultiprobeNoReturnByFinalTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row => acc + row.labelIntermediateMultiprobeNoReturnByFinal)
    0

def a0CompletePrefixSummariesV2Lt8IntermediateMultiprobeNoReturnK12C1Total : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row => acc + row.labelIntermediateMultiprobeNoReturnK12C1)
    0

def a0CompletePrefixSummariesV2Lt8IntermediateMultiprobeNoReturnExtendedLaterTargetTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row => acc + row.labelIntermediateMultiprobeNoReturnExtendedLaterTarget)
    0

def a0CompletePrefixSummariesV2Lt8IntermediateMultiprobeNoReturnExtendedFailureTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row =>
      acc
        + (if row.labelIntermediateMultiprobeNoReturnK10C1 = 0 then 0 else 1)
        + (if row.labelIntermediateMultiprobeNoReturnK11C1 = 0 then 0 else 1)
        + (if row.labelIntermediateMultiprobeNoReturnK12C2 = 0 then 0 else 1)
        + (if row.labelIntermediateMultiprobeNoReturnK20C1 = 0 then 0 else 1)
        + (if row.labelIntermediateMultiprobeNoReturnK12C1
            = row.labelIntermediateMultiprobeNoReturnByFinal then 0 else 1)
        + (if row.labelIntermediateMultiprobeNoReturnExtendedLaterTarget
            = row.labelIntermediateMultiprobeNoReturnByFinal then 0 else 1)
        + row.labelIntermediateMultiprobeNoReturnExtendedTerminal
        + row.labelIntermediateMultiprobeNoReturnExtendedUnresolved
        + (if row.labelIntermediateMultiprobeNoReturnByFinal = 0 then 0
          else
            (if row.labelIntermediateMultiprobeNoReturnLaterTargetMinDelta = 6
              then 0 else 1)
            + (if row.labelIntermediateMultiprobeNoReturnLaterTargetMaxDelta = 6
              then 0 else 1)))
    0

def a0CompletePrefixSummariesV2Lt8IntermediateMultiprobeNoReturnContinuationIntegralityFailureTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row => acc
      + row.labelIntermediateMultiprobeNoReturnContinuationIntegralityFailures)
    0

def a0CompletePrefixSummariesV2Lt8IntermediateMultiprobeNoReturnActualPrefixMatchTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row => acc
      + row.labelIntermediateMultiprobeNoReturnActualPrefixMatches)
    0

def a0CompletePrefixSummariesV2Lt8IntermediateMultiprobeNoReturnActualSuffixTargetWordMatchTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row => acc
      + row.labelIntermediateMultiprobeNoReturnActualSuffixTargetWordMatches)
    0

def a0CompletePrefixSummariesV2Lt8IntermediateMultiprobeNoReturnActualContinuationIntegralityFailureTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row => acc
      + row.labelIntermediateMultiprobeNoReturnActualContinuationIntegralityFailures)
    0

def a0CompletePrefixSummariesV2Lt8IntermediateMultiprobeNoReturnActualRefinedSupportedTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row => acc
      + row.labelIntermediateMultiprobeNoReturnActualRefinedContinuationSupported)
    0

def a0CompletePrefixSummariesV2Lt8IntermediateMultiprobeNoReturnActualRefinedFailureTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row => acc
      + row.labelIntermediateMultiprobeNoReturnActualRefinedContinuationFailures)
    0

def a0CompletePrefixSummariesV2Lt8IntermediateMultiprobeNoReturnActualRefinedCheckFailureTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row =>
      acc
        + (if row.labelIntermediateMultiprobeNoReturnActualPrefixMatches
            = row.labelIntermediateMultiprobeNoReturnByFinal then 0 else 1)
        + (if row.labelIntermediateMultiprobeNoReturnActualSuffixTargetWordMatches
            = row.labelIntermediateMultiprobeNoReturnByFinal then 0 else 1)
        + (if row.labelIntermediateMultiprobeNoReturnActualRefinedContinuationSupported
            = row.labelIntermediateMultiprobeNoReturnByFinal then 0 else 1)
        + row.labelIntermediateMultiprobeNoReturnActualRefinedContinuationFailures
        + row.labelIntermediateMultiprobeNoReturnContinuationNoDropFailures
        + row.labelIntermediateMultiprobeNoReturnActualContinuationNoDropFailures
        + (if row.labelIntermediateMultiprobeNoReturnByFinal = 0 then 0
          else
            (if row.labelIntermediateMultiprobeNoReturnActualRefinedExtraBitsMin = 4
              then 0 else 1)
            + (if row.labelIntermediateMultiprobeNoReturnActualRefinedExtraBitsMax = 4
              then 0 else 1)))
    0

def a0CompletePrefixSummariesV2Lt8IntermediateTargetMultiprobeTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row => acc + row.labelIntermediateTargetMultiprobeTotal)
    0

def a0CompletePrefixSummariesV2Lt8IntermediateTargetMultiprobeFailureTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row =>
      acc
        + (if row.labelIntermediateTargetMultiprobeTotal
            = 8 * row.labelIntermediateTargetVisibleFailures then 0 else 1)
        + (if row.labelIntermediateTargetMultiprobeSameStepReturn
            = row.labelIntermediateTargetMultiprobeTotal then 0 else 1)
        + row.labelIntermediateTargetMultiprobeEarlyTargetReturn
        + row.labelIntermediateTargetMultiprobeNoReturnByFinal
        + row.labelIntermediateTargetMultiprobeTerminalByFinal)
    0

def a0CompletePrefixSummariesV2Lt8IntermediateCompetingLaterTargetTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row => acc + row.labelIntermediateCompetingLaterTargetIntersections)
    0

def a0CompletePrefixSummariesV2Lt8IntermediateCompetingLaterTargetFailureTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row =>
      acc
        + (if row.labelIntermediateCompetingNoLaterTargetIntersections
              + row.labelIntermediateCompetingLaterTargetIntersections
            = row.labelIntermediateCompetingVisibleFailures then 0 else 1)
        + row.labelIntermediateCompetingLaterTargetIntersections)
    0

def a0CompletePrefixSummariesV2Lt8IntermediateTargetPersistentVisibilityTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row => acc + row.labelIntermediateTargetPersistentVisibility)
    0

def a0CompletePrefixSummariesV2Lt8IntermediateTargetMissingPriorVisibilityTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row => acc + row.labelIntermediateTargetMissingPriorVisibility)
    0

def a0CompletePrefixSummariesV2Lt8IntermediateTargetNoPriorCompetingIntersectionTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row => acc + row.labelIntermediateTargetNoPriorCompetingIntersections)
    0

def a0CompletePrefixSummariesV2Lt8IntermediateTargetPriorCompetingIntersectionTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row => acc + row.labelIntermediateTargetPriorCompetingIntersections)
    0

def a0CompletePrefixSummariesV2Lt8IntermediateTargetHighLiftCoveredTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row => acc + row.labelIntermediateTargetHighLiftCovered)
    0

def a0CompletePrefixSummariesV2Lt8IntermediateTargetLowOnlyVisibleTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row => acc + row.labelIntermediateTargetLowOnlyVisible)
    0

def a0CompletePrefixSummariesV2Lt8IntermediateTargetVisibilityStructureFailureTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row =>
      acc
        + row.labelIntermediateTargetPersistentVisibility
        + (if row.labelIntermediateTargetMissingPriorVisibility
            = row.labelIntermediateTargetVisibleFailures then 0 else 1)
        + (if row.labelIntermediateTargetNoPriorCompetingIntersections
            = row.labelIntermediateTargetVisibleFailures then 0 else 1)
        + row.labelIntermediateTargetPriorCompetingIntersections
        + (if row.labelIntermediateTargetHighLiftCovered
            = row.labelIntermediateTargetVisibleFailures then 0 else 1)
        + row.labelIntermediateTargetLowOnlyVisible)
    0

def a0CompletePrefixSummariesV2Lt8HighLiftModBitsFailureTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row =>
      acc
        + (if row.labelFinalTargetHighLiftMinModBits = 7 then 0 else 1)
        + (if row.labelFinalTargetHighLiftMaxModBits = 7 then 0 else 1))
    0

def a0CompletePrefixSummariesV2Lt8HighLiftContinuationFailureTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row =>
      acc
        + (if row.highLiftContinuationSupportedRows = row.branchRows then 0 else 1)
        + (if row.highLiftContinuationStepDeltaMin = 6 then 0 else 1)
        + (if row.highLiftContinuationStepDeltaMax = 6 then 0 else 1))
    0

def a0CompletePrefixSummariesV2Lt8LabelSplitResolutionCertificateTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row => acc + row.labelSplitResolutionCertificate)
    0

def a0CompletePrefixSummariesV2Lt8BranchRowsTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row => acc + row.branchRows)
    0

def a0CompletePrefixSummariesV2Lt8ReturnSamplesTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row => acc + row.returnSamples)
    0

def a0CompletePrefixSummariesV2Lt8TotalSamplesTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row => acc + row.totalSamples)
    0

def a0CompletePrefixSummariesV2Lt8DropSamplesTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row => acc + row.dropSamples)
    0

def a0CompletePrefixSummariesV2Lt8ValuationTailSamplesTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row => acc + row.valuationTailSamples)
    0

def a0CompletePrefixSummariesV2Lt8StepTailSamplesTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row => acc + row.stepTailSamples)
    0

def a0CompletePrefixSummariesV2Lt8BranchSampleCountTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row => acc + row.branchSampleCountTotal)
    0

def a0CompletePrefixSummariesV2Lt8BranchSampleCoverageFailureTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row =>
      acc
        + row.branchSampleCountCoverageFailures
        + (if row.branchSampleCountTotal = row.returnSamples then 0 else 1))
    0

noncomputable def a0CompletePrefixSummariesV2Lt8ReturnPartitionSummary :
    WeakBridge.LabelSplit.ReturnPartitionSummary :=
  { returnSamples := a0CompletePrefixSummariesV2Lt8ReturnSamplesTotal,
    coveredReturnSamples := a0CompletePrefixSummariesV2Lt8BranchSampleCountTotal,
    coverageFailures := a0CompletePrefixSummariesV2Lt8BranchSampleCoverageFailureTotal }

noncomputable def a0CompletePrefixSummariesV2Lt8ReturnPartitionSummaryFailure : Nat :=
  WeakBridge.LabelSplit.returnPartitionFailure
    a0CompletePrefixSummariesV2Lt8ReturnPartitionSummary

noncomputable def a0CompletePrefixSummariesV2Lt8OutcomeSummary :
    WeakBridge.LabelSplit.OutcomeSummary :=
  { totalSamples := a0CompletePrefixSummariesV2Lt8TotalSamplesTotal,
    returnSamples := a0CompletePrefixSummariesV2Lt8ReturnSamplesTotal,
    coveredReturnSamples := a0CompletePrefixSummariesV2Lt8BranchSampleCountTotal,
    dropSamples := a0CompletePrefixSummariesV2Lt8DropSamplesTotal,
    valuationTailSamples := a0CompletePrefixSummariesV2Lt8ValuationTailSamplesTotal,
    stepTailSamples := a0CompletePrefixSummariesV2Lt8StepTailSamplesTotal,
    returnCoverageFailures := a0CompletePrefixSummariesV2Lt8BranchSampleCoverageFailureTotal }

noncomputable def a0CompletePrefixSummariesV2Lt8OutcomeDecompositionFailure : Nat :=
  WeakBridge.LabelSplit.outcomeDecompositionFailure
    a0CompletePrefixSummariesV2Lt8OutcomeSummary

def a0CompletePrefixSummariesV2Lt8LabelSplitResolutionCertificateFailureTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row =>
      acc
        + (if row.labelSplitResolutionCertificate = row.branchRows then 0 else 1))
    0

noncomputable def a0CompletePrefixSummariesV2Lt8LabelSplitSummary :
    WeakBridge.LabelSplit.SummaryCounters :=
  { branchRows := a0CompletePrefixSummariesV2Lt8BranchRowsTotal,
    certificateRows := a0CompletePrefixSummariesV2Lt8LabelSplitResolutionCertificateTotal }

noncomputable def a0CompletePrefixSummariesV2Lt8LabelSplitSummaryFailure : Nat :=
  WeakBridge.LabelSplit.summaryFailure
    a0CompletePrefixSummariesV2Lt8LabelSplitSummary

/-- The complete-prefix rows all carry script-126 arithmetic certificates. -/
def a0CompletePrefixSummariesV2Lt8ArithmeticCertificateFailureTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row =>
      acc +
        (if row.arithmeticCertificateRows = row.branchRows then 0 else 1)
        + (if row.noDropCertificateRows = row.branchRows then 0 else 1))
    0

/-- The summary rows account for every enumerated source point. -/
def a0CompletePrefixSummariesV2Lt8CoverageFailureTotal : Nat :=
  a0CompletePrefixSummariesV2Lt8.foldl
    (fun acc row =>
      acc +
        if row.returnSamples + row.dropSamples
            + row.valuationTailSamples + row.stepTailSamples
          = row.totalSamples then 0 else 1)
    0

theorem a0CompletePrefixSummariesV2Lt8_failure_total_zero :
    a0CompletePrefixSummariesV2Lt8FailureTotal = 0 := by
  norm_num [a0CompletePrefixSummariesV2Lt8FailureTotal,
    a0CompletePrefixSummariesV2Lt8]

theorem a0CompletePrefixSummariesV2Lt8_label_open_total :
    a0CompletePrefixSummariesV2Lt8LabelOpenTotal = 6628 := by
  norm_num [a0CompletePrefixSummariesV2Lt8LabelOpenTotal,
    a0CompletePrefixSummariesV2Lt8]

theorem a0CompletePrefixSummariesV2Lt8_label_status_coverage_zero :
    a0CompletePrefixSummariesV2Lt8LabelStatusCoverageFailureTotal = 0 := by
  norm_num [a0CompletePrefixSummariesV2Lt8LabelStatusCoverageFailureTotal,
    a0CompletePrefixSummariesV2Lt8]

theorem a0CompletePrefixSummariesV2Lt8_intermediate_visible_split :
    a0CompletePrefixSummariesV2Lt8IntermediateTargetVisibleTotal = 92
      ∧ a0CompletePrefixSummariesV2Lt8IntermediateCompetingVisibleTotal = 1244
      ∧ a0CompletePrefixSummariesV2Lt8IntermediateSplitFailureTotal = 0 := by
  norm_num [a0CompletePrefixSummariesV2Lt8IntermediateTargetVisibleTotal,
    a0CompletePrefixSummariesV2Lt8IntermediateCompetingVisibleTotal,
    a0CompletePrefixSummariesV2Lt8IntermediateSplitFailureTotal,
    a0CompletePrefixSummariesV2Lt8]

theorem a0CompletePrefixSummariesV2Lt8_intermediate_visible_by_record :
    a0CompletePrefixSummariesV2Lt8IntermediateK10C1VisibleTotal = 8
      ∧ a0CompletePrefixSummariesV2Lt8IntermediateK11C1VisibleTotal = 896
      ∧ a0CompletePrefixSummariesV2Lt8IntermediateK12C1VisibleTotal = 340
      ∧ a0CompletePrefixSummariesV2Lt8IntermediateK12C2VisibleTotal = 92
      ∧ a0CompletePrefixSummariesV2Lt8IntermediateK20C1VisibleTotal = 0
      ∧ a0CompletePrefixSummariesV2Lt8IntermediateRecordSplitFailureTotal = 0 := by
  norm_num [a0CompletePrefixSummariesV2Lt8IntermediateK10C1VisibleTotal,
    a0CompletePrefixSummariesV2Lt8IntermediateK11C1VisibleTotal,
    a0CompletePrefixSummariesV2Lt8IntermediateK12C1VisibleTotal,
    a0CompletePrefixSummariesV2Lt8IntermediateK12C2VisibleTotal,
    a0CompletePrefixSummariesV2Lt8IntermediateK20C1VisibleTotal,
    a0CompletePrefixSummariesV2Lt8IntermediateRecordSplitFailureTotal,
    a0CompletePrefixSummariesV2Lt8]

theorem a0CompletePrefixSummariesV2Lt8_intermediate_probe_same_step :
    a0CompletePrefixSummariesV2Lt8IntermediateProbeTotal = 1336
      ∧ a0CompletePrefixSummariesV2Lt8IntermediateProbeFailureTotal = 0 := by
  norm_num [a0CompletePrefixSummariesV2Lt8IntermediateProbeTotal,
    a0CompletePrefixSummariesV2Lt8IntermediateProbeFailureTotal,
    a0CompletePrefixSummariesV2Lt8]

theorem a0CompletePrefixSummariesV2Lt8_intermediate_multiprobe_no_early :
    a0CompletePrefixSummariesV2Lt8IntermediateMultiprobeTotal = 10688
      ∧ a0CompletePrefixSummariesV2Lt8IntermediateMultiprobeEarlyTargetTotal = 0
      ∧ a0CompletePrefixSummariesV2Lt8IntermediateMultiprobeNoReturnByFinalTotal = 8 := by
  norm_num [a0CompletePrefixSummariesV2Lt8IntermediateMultiprobeTotal,
    a0CompletePrefixSummariesV2Lt8IntermediateMultiprobeEarlyTargetTotal,
    a0CompletePrefixSummariesV2Lt8IntermediateMultiprobeNoReturnByFinalTotal,
    a0CompletePrefixSummariesV2Lt8]

theorem a0CompletePrefixSummariesV2Lt8_intermediate_multiprobe_no_return_extended :
    a0CompletePrefixSummariesV2Lt8IntermediateMultiprobeNoReturnK12C1Total = 8
      ∧ a0CompletePrefixSummariesV2Lt8IntermediateMultiprobeNoReturnExtendedLaterTargetTotal = 8
      ∧ a0CompletePrefixSummariesV2Lt8IntermediateMultiprobeNoReturnExtendedFailureTotal = 0 := by
  norm_num [a0CompletePrefixSummariesV2Lt8IntermediateMultiprobeNoReturnK12C1Total,
    a0CompletePrefixSummariesV2Lt8IntermediateMultiprobeNoReturnExtendedLaterTargetTotal,
    a0CompletePrefixSummariesV2Lt8IntermediateMultiprobeNoReturnExtendedFailureTotal,
    a0CompletePrefixSummariesV2Lt8]

theorem a0CompletePrefixSummariesV2Lt8_intermediate_multiprobe_no_return_actual_refined :
    a0CompletePrefixSummariesV2Lt8IntermediateMultiprobeNoReturnContinuationIntegralityFailureTotal = 8
      ∧ a0CompletePrefixSummariesV2Lt8IntermediateMultiprobeNoReturnActualPrefixMatchTotal = 8
      ∧ a0CompletePrefixSummariesV2Lt8IntermediateMultiprobeNoReturnActualSuffixTargetWordMatchTotal = 8
      ∧ a0CompletePrefixSummariesV2Lt8IntermediateMultiprobeNoReturnActualContinuationIntegralityFailureTotal = 8
      ∧ a0CompletePrefixSummariesV2Lt8IntermediateMultiprobeNoReturnActualRefinedSupportedTotal = 8
      ∧ a0CompletePrefixSummariesV2Lt8IntermediateMultiprobeNoReturnActualRefinedFailureTotal = 0
      ∧ a0CompletePrefixSummariesV2Lt8IntermediateMultiprobeNoReturnActualRefinedCheckFailureTotal = 0 := by
  norm_num [
    a0CompletePrefixSummariesV2Lt8IntermediateMultiprobeNoReturnContinuationIntegralityFailureTotal,
    a0CompletePrefixSummariesV2Lt8IntermediateMultiprobeNoReturnActualPrefixMatchTotal,
    a0CompletePrefixSummariesV2Lt8IntermediateMultiprobeNoReturnActualSuffixTargetWordMatchTotal,
    a0CompletePrefixSummariesV2Lt8IntermediateMultiprobeNoReturnActualContinuationIntegralityFailureTotal,
    a0CompletePrefixSummariesV2Lt8IntermediateMultiprobeNoReturnActualRefinedSupportedTotal,
    a0CompletePrefixSummariesV2Lt8IntermediateMultiprobeNoReturnActualRefinedFailureTotal,
    a0CompletePrefixSummariesV2Lt8IntermediateMultiprobeNoReturnActualRefinedCheckFailureTotal,
    a0CompletePrefixSummariesV2Lt8]

theorem a0CompletePrefixSummariesV2Lt8_intermediate_target_multiprobe_same_step :
    a0CompletePrefixSummariesV2Lt8IntermediateTargetMultiprobeTotal = 736
      ∧ a0CompletePrefixSummariesV2Lt8IntermediateTargetMultiprobeFailureTotal = 0 := by
  norm_num [a0CompletePrefixSummariesV2Lt8IntermediateTargetMultiprobeTotal,
    a0CompletePrefixSummariesV2Lt8IntermediateTargetMultiprobeFailureTotal,
    a0CompletePrefixSummariesV2Lt8]

theorem a0CompletePrefixSummariesV2Lt8_intermediate_competing_no_later_target :
    a0CompletePrefixSummariesV2Lt8IntermediateCompetingNoLaterTargetTotal = 1244
      ∧ a0CompletePrefixSummariesV2Lt8IntermediateCompetingLaterTargetTotal = 0
      ∧ a0CompletePrefixSummariesV2Lt8IntermediateCompetingLaterTargetFailureTotal = 0 := by
  norm_num [a0CompletePrefixSummariesV2Lt8IntermediateCompetingNoLaterTargetTotal,
    a0CompletePrefixSummariesV2Lt8IntermediateCompetingLaterTargetTotal,
    a0CompletePrefixSummariesV2Lt8IntermediateCompetingLaterTargetFailureTotal,
    a0CompletePrefixSummariesV2Lt8]

theorem a0CompletePrefixSummariesV2Lt8_intermediate_target_visibility_structure :
    a0CompletePrefixSummariesV2Lt8IntermediateTargetPersistentVisibilityTotal = 0
      ∧ a0CompletePrefixSummariesV2Lt8IntermediateTargetMissingPriorVisibilityTotal = 92
      ∧ a0CompletePrefixSummariesV2Lt8IntermediateTargetNoPriorCompetingIntersectionTotal = 92
      ∧ a0CompletePrefixSummariesV2Lt8IntermediateTargetPriorCompetingIntersectionTotal = 0
      ∧ a0CompletePrefixSummariesV2Lt8IntermediateTargetHighLiftCoveredTotal = 92
      ∧ a0CompletePrefixSummariesV2Lt8IntermediateTargetLowOnlyVisibleTotal = 0
      ∧ a0CompletePrefixSummariesV2Lt8IntermediateTargetVisibilityStructureFailureTotal = 0 := by
  norm_num [
    a0CompletePrefixSummariesV2Lt8IntermediateTargetPersistentVisibilityTotal,
    a0CompletePrefixSummariesV2Lt8IntermediateTargetMissingPriorVisibilityTotal,
    a0CompletePrefixSummariesV2Lt8IntermediateTargetNoPriorCompetingIntersectionTotal,
    a0CompletePrefixSummariesV2Lt8IntermediateTargetPriorCompetingIntersectionTotal,
    a0CompletePrefixSummariesV2Lt8IntermediateTargetHighLiftCoveredTotal,
    a0CompletePrefixSummariesV2Lt8IntermediateTargetLowOnlyVisibleTotal,
    a0CompletePrefixSummariesV2Lt8IntermediateTargetVisibilityStructureFailureTotal,
    a0CompletePrefixSummariesV2Lt8]

theorem a0CompletePrefixSummariesV2Lt8_high_lift_mod_bits_seven :
    a0CompletePrefixSummariesV2Lt8HighLiftModBitsFailureTotal = 0 := by
  norm_num [a0CompletePrefixSummariesV2Lt8HighLiftModBitsFailureTotal,
    a0CompletePrefixSummariesV2Lt8]

theorem a0CompletePrefixSummariesV2Lt8_high_lift_continuation_zero :
    a0CompletePrefixSummariesV2Lt8HighLiftContinuationFailureTotal = 0 := by
  norm_num [a0CompletePrefixSummariesV2Lt8HighLiftContinuationFailureTotal,
    a0CompletePrefixSummariesV2Lt8]

theorem a0CompletePrefixSummariesV2Lt8_label_split_resolution_certificate :
    a0CompletePrefixSummariesV2Lt8BranchRowsTotal = 5292
      ∧ a0CompletePrefixSummariesV2Lt8LabelSplitResolutionCertificateTotal = 5292
      ∧ a0CompletePrefixSummariesV2Lt8LabelSplitResolutionCertificateFailureTotal = 0 := by
  norm_num [
    a0CompletePrefixSummariesV2Lt8BranchRowsTotal,
    a0CompletePrefixSummariesV2Lt8LabelSplitResolutionCertificateTotal,
    a0CompletePrefixSummariesV2Lt8LabelSplitResolutionCertificateFailureTotal,
    a0CompletePrefixSummariesV2Lt8]

theorem a0CompletePrefixSummariesV2Lt8_label_split_summary_resolved :
    WeakBridge.LabelSplit.summaryResolved
        a0CompletePrefixSummariesV2Lt8LabelSplitSummary
      ∧ a0CompletePrefixSummariesV2Lt8LabelSplitSummaryFailure = 0 := by
  norm_num [
    a0CompletePrefixSummariesV2Lt8LabelSplitSummary,
    a0CompletePrefixSummariesV2Lt8LabelSplitSummaryFailure,
    a0CompletePrefixSummariesV2Lt8BranchRowsTotal,
    a0CompletePrefixSummariesV2Lt8LabelSplitResolutionCertificateTotal,
    WeakBridge.LabelSplit.summaryResolved,
    WeakBridge.LabelSplit.summaryFailure,
    a0CompletePrefixSummariesV2Lt8]

theorem a0CompletePrefixSummariesV2Lt8_return_partition_summary_resolved :
    a0CompletePrefixSummariesV2Lt8ReturnSamplesTotal = 11752
      ∧ a0CompletePrefixSummariesV2Lt8BranchSampleCountTotal = 11752
      ∧ a0CompletePrefixSummariesV2Lt8BranchSampleCoverageFailureTotal = 0
      ∧ WeakBridge.LabelSplit.returnPartitionResolved
          a0CompletePrefixSummariesV2Lt8ReturnPartitionSummary
      ∧ a0CompletePrefixSummariesV2Lt8ReturnPartitionSummaryFailure = 0 := by
  norm_num [
    a0CompletePrefixSummariesV2Lt8ReturnSamplesTotal,
    a0CompletePrefixSummariesV2Lt8BranchSampleCountTotal,
    a0CompletePrefixSummariesV2Lt8BranchSampleCoverageFailureTotal,
    a0CompletePrefixSummariesV2Lt8ReturnPartitionSummary,
    a0CompletePrefixSummariesV2Lt8ReturnPartitionSummaryFailure,
    WeakBridge.LabelSplit.returnPartitionResolved,
    WeakBridge.LabelSplit.returnPartitionFailure,
    a0CompletePrefixSummariesV2Lt8]

theorem a0CompletePrefixSummariesV2Lt8_outcome_decomposition_resolved :
    a0CompletePrefixSummariesV2Lt8TotalSamplesTotal = 114240
      ∧ a0CompletePrefixSummariesV2Lt8ReturnSamplesTotal = 11752
      ∧ a0CompletePrefixSummariesV2Lt8BranchSampleCountTotal = 11752
      ∧ a0CompletePrefixSummariesV2Lt8DropSamplesTotal = 101628
      ∧ a0CompletePrefixSummariesV2Lt8ValuationTailSamplesTotal = 844
      ∧ a0CompletePrefixSummariesV2Lt8StepTailSamplesTotal = 16
      ∧ WeakBridge.LabelSplit.tailSamples
          a0CompletePrefixSummariesV2Lt8OutcomeSummary = 860
      ∧ WeakBridge.LabelSplit.outcomeAccountedSamples
          a0CompletePrefixSummariesV2Lt8OutcomeSummary = 114240
      ∧ WeakBridge.LabelSplit.outcomeDecompositionResolved
          a0CompletePrefixSummariesV2Lt8OutcomeSummary
      ∧ a0CompletePrefixSummariesV2Lt8OutcomeDecompositionFailure = 0 := by
  norm_num [
    a0CompletePrefixSummariesV2Lt8TotalSamplesTotal,
    a0CompletePrefixSummariesV2Lt8ReturnSamplesTotal,
    a0CompletePrefixSummariesV2Lt8BranchSampleCountTotal,
    a0CompletePrefixSummariesV2Lt8DropSamplesTotal,
    a0CompletePrefixSummariesV2Lt8ValuationTailSamplesTotal,
    a0CompletePrefixSummariesV2Lt8StepTailSamplesTotal,
    a0CompletePrefixSummariesV2Lt8BranchSampleCoverageFailureTotal,
    a0CompletePrefixSummariesV2Lt8OutcomeSummary,
    a0CompletePrefixSummariesV2Lt8OutcomeDecompositionFailure,
    WeakBridge.LabelSplit.tailSamples,
    WeakBridge.LabelSplit.outcomeAccountedSamples,
    WeakBridge.LabelSplit.outcomeDecompositionResolved,
    WeakBridge.LabelSplit.outcomeDecompositionFailure,
    a0CompletePrefixSummariesV2Lt8]

theorem a0CompletePrefixSummariesV2Lt8_coverage_total_zero :
    a0CompletePrefixSummariesV2Lt8CoverageFailureTotal = 0 := by
  norm_num [a0CompletePrefixSummariesV2Lt8CoverageFailureTotal,
    a0CompletePrefixSummariesV2Lt8]

theorem a0CompletePrefixSummariesV2Lt8_arithmetic_certificate_total_zero :
    a0CompletePrefixSummariesV2Lt8ArithmeticCertificateFailureTotal = 0 := by
  norm_num [a0CompletePrefixSummariesV2Lt8ArithmeticCertificateFailureTotal,
    a0CompletePrefixSummariesV2Lt8]

end Generated
end CollatzShadowing
