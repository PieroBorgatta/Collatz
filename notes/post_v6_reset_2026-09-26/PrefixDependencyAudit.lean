/-
Kernel dependency audit for the exact dyadic-prefix certificate theorem.
Run from the project's lean directory after building PrefixOptimality:

  lake env lean ../notes/post_v6_reset_2026-09-26/PrefixDependencyAudit.lean

Expected foundational axioms, when used: propext, Classical.choice,
Quot.sound. No Collatz hypothesis, custom axiom, sorryAx or native_decide.
This audit does not claim convergence or estimates for the exact tower.
-/
import CollatzShadowing.PrefixOptimality
import Lean

open Lean Elab Command

namespace PrefixDependencyAudit

private def allowed (name : Name) : Bool :=
  name == `propext || name == `Classical.choice || name == `Quot.sound

private def roots : Array Name :=
  #[`CollatzShadowing.PrefixOptimality.iterate_lift,
    `CollatzShadowing.PrefixOptimality.J_eq_of_modEq,
    `CollatzShadowing.PrefixOptimality.f_lift_flips_parity,
    `CollatzShadowing.PrefixOptimality.all_one_suffix_attained,
    `CollatzShadowing.PrefixOptimality.prefixMaximum_exact,
    `CollatzShadowing.PrefixOptimality.certificate_iff_maximum_le,
    `CollatzShadowing.PrefixOptimality.certificate_iff_zeros,
    `CollatzShadowing.PrefixOptimality.counterexample_before_threshold,
    `CollatzShadowing.PrefixOptimality.prefixMaximum_eq_actual_add_remaining_zeros,
    `CollatzShadowing.PrefixOptimality.exists_certifying_precision_iff]

private def run : CommandElabM Unit := do
  let env := (← getEnv).setExporting false
  for root in roots do
    unless (env.find? root).isSome do
      throwError "Missing audited theorem: {root}"
    let axioms ← Lean.collectAxioms root
    for ax in axioms do
      unless allowed ax do
        throwError "Unexpected axiom in {root}: {ax}"
    logInfo m!"PREFIX_ROOT_AUDIT: PASS {root}; axioms: {axioms.toList}"
  logInfo m!"PREFIX_AUDIT: PASS; roots: {roots.size}"

set_option maxHeartbeats 0 in
run_cmd run

end PrefixDependencyAudit

#print axioms CollatzShadowing.PrefixOptimality.iterate_lift
#print axioms CollatzShadowing.PrefixOptimality.J_eq_of_modEq
#print axioms CollatzShadowing.PrefixOptimality.f_lift_flips_parity
#print axioms CollatzShadowing.PrefixOptimality.all_one_suffix_attained
#print axioms CollatzShadowing.PrefixOptimality.prefixMaximum_exact
#print axioms CollatzShadowing.PrefixOptimality.certificate_iff_maximum_le
#print axioms CollatzShadowing.PrefixOptimality.certificate_iff_zeros
#print axioms CollatzShadowing.PrefixOptimality.counterexample_before_threshold
#print axioms CollatzShadowing.PrefixOptimality.prefixMaximum_eq_actual_add_remaining_zeros
#print axioms CollatzShadowing.PrefixOptimality.exists_certifying_precision_iff

#check CollatzShadowing.PrefixOptimality.prefixMaximum_exact
#check CollatzShadowing.PrefixOptimality.certificate_iff_zeros

-- The inputs and endpoints are the actual natural shortcut dynamics.
example (x k : ℕ) :
    CollatzShadowing.PrefixOptimality.J x (k + 1) =
      CollatzShadowing.PrefixOptimality.J x k +
        (CollatzShadowing.ShortcutCoverage.T^[k] x) % 2 :=
  CollatzShadowing.PrefixOptimality.J_succ x k
