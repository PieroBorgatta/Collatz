/-
Standalone maximum-envelope prototype. Not imported by the main library.

Only exact positive odd unit seeds are allowed. The empty word supplies
weight one. Finiteness above one gives a genuinely attained maximum; it
does not give an algorithm for excluding unknown small ancestors.

No density, canonical inverse law, optimal profile theorem, or Collatz
conclusion is imported. AI-assisted: Codex with Piero Borgatta, 2026-11-16.
-/

import CollatzShadowing.BoundedSlopeCatalogue
import Mathlib.Data.Finset.Max
import Lean

namespace MaxEnvelopePrototype

open CollatzShadowing CollatzShadowing.WeightedVisits CollatzShadowing.RootPoolBudget

/-- Positive odd integers not divisible by three. -/
def IsUnitSeed (u : ℕ) : Prop := 0 < u ∧ Odd u ∧ u % 3 ≠ 0

/-- A genuine word from a positive odd unit seed to the target. -/
def Admissible (n : ℕ) (w : List ℕ) : Prop :=
  ∃ u : ℕ, IsUnitSeed u ∧ SyracuseWordMatchesFrom w u ∧ evalSyracuseWord w u = n

private noncomputable def candidates (n : ℕ) : Finset (List ℕ) := by
  classical
  exact (CollatzShadowing.BoundedSlopeCatalogue.catalogue_finite n
    (by norm_num : (0 : ℚ) < 1)).toFinset.filter (Admissible n)

private theorem mem_candidates {n : ℕ} {w : List ℕ} :
    w ∈ candidates n ↔ Admissible n w ∧ 1 ≤ wordWeight w := by
  classical
  let hf := CollatzShadowing.BoundedSlopeCatalogue.catalogue_finite n
    (by norm_num : (0 : ℚ) < 1)
  change (w ∈ hf.toFinset.filter (Admissible n)) ↔ _
  rw [Finset.mem_filter, hf.mem_toFinset]
  constructor
  · rintro ⟨hcat, hadm⟩
    obtain ⟨u, hu, hm, he, hweight⟩ := hcat
    exact ⟨hadm, by simpa using hweight⟩
  · rintro ⟨hadm, hweight⟩
    obtain ⟨u, hu, hm, he⟩ := hadm
    exact ⟨⟨u, hu.1, hm, he, by simpa using hweight⟩, ⟨u, hu, hm, he⟩⟩

private noncomputable def weights (n : ℕ) : Finset ℚ := by
  classical
  exact insert 1 ((candidates n).image wordWeight)

private theorem weights_nonempty (n : ℕ) : (weights n).Nonempty := by
  classical
  exact ⟨1, by simp only [weights, Finset.mem_insert, true_or]⟩

/-- The arithmetic maximum. Baseline one is used also at invalid targets;
all substantive attainment statements require a valid target. -/
noncomputable def envelope (n : ℕ) : ℚ := (weights n).max' (weights_nonempty n)

theorem one_le_envelope (n : ℕ) : 1 ≤ envelope n := by
  classical
  exact (weights n).le_max' 1 (by simp only [weights, Finset.mem_insert, true_or])

/-- Every genuine word is dominated, including words of weight below one. -/
theorem wordWeight_le_envelope {n : ℕ} {w : List ℕ} (hw : Admissible n w) :
    wordWeight w ≤ envelope n := by
  classical
  by_cases hlarge : 1 ≤ wordWeight w
  · have hc := mem_candidates.mpr ⟨hw, hlarge⟩
    apply (weights n).le_max' (wordWeight w)
    exact Finset.mem_insert_of_mem (Finset.mem_image.mpr ⟨w, hc, rfl⟩)
  · exact (le_of_lt (lt_of_not_ge hlarge)).trans (one_le_envelope n)

/-- A valid target has a genuine word attaining the envelope, with an actual
positive odd unit source, even when the target is periodic. -/
theorem exists_maximizing_word {n : ℕ} (hn : IsUnitSeed n) :
    ∃ w : List ℕ, Admissible n w ∧ wordWeight w = envelope n := by
  classical
  have hmem := (weights n).max'_mem (weights_nonempty n)
  change envelope n ∈ weights n at hmem
  rw [weights, Finset.mem_insert] at hmem
  rcases hmem with hone | himage
  · refine ⟨[], ⟨n, hn, trivial, rfl⟩, ?_⟩
    simp [wordWeight, hone]
  · obtain ⟨w, hw, heq⟩ := Finset.mem_image.mp himage
    exact ⟨w, (mem_candidates.mp hw).1, heq⟩

private theorem weight_mul_source_le {u n : ℕ} {w : List ℕ}
    (hu : 0 < u) (hm : SyracuseWordMatchesFrom w u)
    (he : evalSyracuseWord w u = n) : wordWeight w * (u : ℚ) ≤ n := by
  have hn : 0 < n := by
    rw [← he, evalSyracuseWord_eq_iterate_of_matches w u hm]
    exact orbit_pos hu _
  have hu' : (0 : ℚ) < u := by exact_mod_cast hu
  have hn' : (0 : ℚ) < n := by exact_mod_cast hn
  have hp := reciprocalWeight_le_initial hu hm
  rw [reciprocalWeight, he] at hp
  simpa only [one_mul] using (div_le_div_iff₀ hn' hu').mp hp

theorem envelope_le_target {n : ℕ} (hn : IsUnitSeed n) : envelope n ≤ n := by
  obtain ⟨w, ⟨u, hu, hm, he⟩, hmax⟩ := exists_maximizing_word hn
  have hp := weight_mul_source_le hu.1 hm he
  rw [hmax] at hp
  have hule : (1 : ℚ) ≤ u := by exact_mod_cast hu.1
  have hF := one_le_envelope n
  nlinarith

/-- The positive source of any maximizing word is at most n/F(n). -/
theorem optimal_source_bound {u n : ℕ} {w : List ℕ}
    (hu : 0 < u) (hm : SyracuseWordMatchesFrom w u)
    (he : evalSyracuseWord w u = n) (hmax : wordWeight w = envelope n) :
    (u : ℚ) ≤ (n : ℚ) / envelope n := by
  have hF : (0 : ℚ) < envelope n := lt_of_lt_of_le (by norm_num) (one_le_envelope n)
  apply (le_div_iff₀ hF).mpr
  have hp := weight_mul_source_le hu hm he
  rw [hmax] at hp
  simpa only [mul_comm] using hp

/-- The envelope is the least numerical majorant of all genuine word gains.
This is not yet an edge-by-edge max-supersolution theorem. -/
theorem envelope_le_of_word_majorant {n : ℕ} (hn : IsUnitSeed n) {b : ℚ}
    (hb : ∀ w : List ℕ, Admissible n w → wordWeight w ≤ b) : envelope n ≤ b := by
  obtain ⟨w, hw, hmax⟩ := exists_maximizing_word hn
  rw [← hmax]
  exact hb w hw

end MaxEnvelopePrototype

open Lean Elab Command

namespace MaxEnvelopePrototypeAudit

private def belongs (name : Name) : Bool :=
  let s := name.toString
  s.startsWith "MaxEnvelopePrototype." ||
    (s.startsWith "_private." && (s.splitOn ".MaxEnvelopePrototype.").length > 1)

private def allowed (name : Name) : Bool :=
  name == `propext || name == `Classical.choice || name == `Quot.sound

private def run : CommandElabM Unit := do
  let env := (← getEnv).setExporting false
  let roots ← env.constants.foldM (init := (#[] : Array Name)) fun roots name _ => do
    return if belongs name then roots.push name else roots
  unless roots.size > 0 do
    throwError "No prototype declarations found"
  let roots := roots.qsort fun a b => a.toString < b.toString
  for root in roots do
    let axioms ← Lean.collectAxioms root
    for ax in axioms do
      unless allowed ax do
        throwError "Unexpected axiom in {root}: {ax}"
    logInfo m!"MAX_ENVELOPE_ROOT: PASS {root}; axioms: {axioms.toList}"
  let privateCount := (roots.filter fun n => n.toString.startsWith "_private.").size
  logInfo m!"MAX_ENVELOPE_AUDIT: PASS; declarations: {roots.size}; encoded-private: {privateCount}"

set_option maxHeartbeats 0 in
run_cmd run

end MaxEnvelopePrototypeAudit


/-! Standalone algebraic extension. The frozen core above is copied verbatim. -/
namespace MaxEnvelopeComposition

open MaxEnvelopePrototype CollatzShadowing CollatzShadowing.WeightedVisits

private theorem wordWeight_append (v w : List ℕ) :
    wordWeight (v ++ w) = wordWeight v * wordWeight w := by
  simp only [wordWeight, List.length_append, List.sum_append, pow_add]
  ring

/-- Composing an actual maximizing predecessor of u with any exact word
from u to n gives a genuine candidate for the maximum at n. -/
theorem envelope_composition {u n : ℕ} {w : List ℕ}
    (hu : IsUnitSeed u) (hm : SyracuseWordMatchesFrom w u)
    (he : evalSyracuseWord w u = n) :
    wordWeight w * envelope u ≤ envelope n := by
  obtain ⟨v, ⟨s, hs, hv, hev⟩, hmax⟩ := exists_maximizing_word hu
  have hcomp : Admissible n (v ++ w) := by
    refine ⟨s, hs, SyracuseWordMatchesFrom_append_of_matches v w s hv ?_, ?_⟩
    · simpa only [hev] using hm
    · rw [evalSyracuseWord_append, hev, he]
  have hd := wordWeight_le_envelope hcomp
  rw [wordWeight_append, hmax] at hd
  simpa only [mul_comm] using hd

/-- A seed of any genuinely maximizing word is already at the baseline. -/
theorem maximizing_seed_baseline {u n : ℕ} {w : List ℕ}
    (hu : IsUnitSeed u) (hm : SyracuseWordMatchesFrom w u)
    (he : evalSyracuseWord w u = n) (hmax : wordWeight w = envelope n) :
    envelope u = 1 := by
  have hc := envelope_composition hu hm he
  rw [hmax] at hc
  have hF : (0 : ℚ) < envelope n := lt_of_lt_of_le (by norm_num) (one_le_envelope n)
  have hup : envelope u ≤ 1 := (mul_le_mul_left hF).mp (by
    simpa only [mul_one] using hc)
  exact le_antisymm hup (one_le_envelope u)

/-- Every prefix of an optimal word is calibrated. Validity of the
intermediate endpoint is explicit here; no automatic unit theorem is added. -/
theorem maximizing_prefix_calibrated {u z n : ℕ} {v w : List ℕ}
    (hu : IsUnitSeed u) (hz : IsUnitSeed z)
    (hv : SyracuseWordMatchesFrom v u) (hev : evalSyracuseWord v u = z)
    (hw : SyracuseWordMatchesFrom w z) (hew : evalSyracuseWord w z = n)
    (hmax : wordWeight (v ++ w) = envelope n) : envelope z = wordWeight v := by
  have hlo : wordWeight v ≤ envelope z := wordWeight_le_envelope ⟨u, hu, hv, hev⟩
  have hhi := envelope_composition hz hw hew
  have hpos := wordWeight_pos w
  rw [← hmax, wordWeight_append] at hhi
  have hup : envelope z ≤ wordWeight v := (mul_le_mul_left hpos).mp (by
    simpa only [mul_comm] using hhi)
  exact le_antisymm hup hlo

end MaxEnvelopeComposition

open Lean Elab Command

namespace MaxEnvelopeCompositionAudit

private def belongs (name : Name) : Bool :=
  let s := name.toString
  s.startsWith "MaxEnvelopeComposition." ||
    (s.startsWith "_private." && (s.splitOn ".MaxEnvelopeComposition.").length > 1)

private def allowed (name : Name) : Bool :=
  name == `propext || name == `Classical.choice || name == `Quot.sound

private def run : CommandElabM Unit := do
  let env := (← getEnv).setExporting false
  let roots ← env.constants.foldM (init := (#[] : Array Name)) fun roots name _ => do
    return if belongs name then roots.push name else roots
  unless roots.size > 0 do
    throwError "No prototype declarations found"
  let roots := roots.qsort fun a b => a.toString < b.toString
  for root in roots do
    let axioms ← Lean.collectAxioms root
    for ax in axioms do
      unless allowed ax do
        throwError "Unexpected axiom in {root}: {ax}"
    logInfo m!"MAX_COMPOSITION_ROOT: PASS {root}; axioms: {axioms.toList}"
  let privateCount := (roots.filter fun n => n.toString.startsWith "_private.").size
  logInfo m!"MAX_COMPOSITION_AUDIT: PASS; declarations: {roots.size}; encoded-private: {privateCount}"

set_option maxHeartbeats 0 in
run_cmd run

end MaxEnvelopeCompositionAudit
