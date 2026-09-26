/- Strict named-root axiom audit; not an independent kernel checker. -/
import CollatzShadowing.SiblingBasins
import Lean

open Lean Elab Command

namespace SiblingDependencyAudit

private def allowed (name : Name) : Bool :=
  name == `propext || name == `Classical.choice || name == `Quot.sound

private def roots : Array Name :=
  #[`CollatzShadowing.SiblingBasins.sibling_ne_orbit,
    `CollatzShadowing.SiblingBasins.iterate_sibling_succ,
    `CollatzShadowing.SiblingBasins.sibling_no_positive_return,
    `CollatzShadowing.SiblingBasins.sibling_index_eq_of_reaches,
    `CollatzShadowing.SiblingBasins.basins_pairwise_disjoint,
    `CollatzShadowing.SiblingBasins.sum_weight_predecessors_le,
    `CollatzShadowing.SiblingBasins.sum_card_predecessors_le,
    `CollatzShadowing.SiblingBasins.canonicalSibling_step,
    `CollatzShadowing.SiblingBasins.lt_canonicalSibling,
    `CollatzShadowing.SiblingBasins.canonicalSibling_le,
    `CollatzShadowing.SiblingBasins.canonicalSibling_odd,
    `CollatzShadowing.SiblingBasins.canonicalSibling_not_dvd_three,
    `CollatzShadowing.SiblingBasins.canonicalSibling_spec,
    `CollatzShadowing.SiblingBasins.canonical_sum_weight_predecessors_le]

private def run : CommandElabM Unit := do
  let env := (← getEnv).setExporting false
  for root in roots do
    unless (env.find? root).isSome do
      throwError "Missing audited theorem: {root}"
    let axioms ← Lean.collectAxioms root
    for ax in axioms do
      unless allowed ax do
        throwError "Unexpected axiom in {root}: {ax}"
    logInfo m!"SIBLING_ROOT_AUDIT: PASS {root}; axioms: {axioms.toList}"
  logInfo m!"SIBLING_DEPENDENCY_AUDIT: PASS; roots: {roots.size}"

set_option maxHeartbeats 0 in
run_cmd run

end SiblingDependencyAudit
