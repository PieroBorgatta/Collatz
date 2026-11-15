/- Strict root audit for the shared root-pool budgets, 2026-11-13.
AI-assisted development with Piero Borgatta. Reuses the project's existing
audit convention; this is not an independent kernel replay. -/
import CollatzShadowing.RootPoolBudget
import Lean

open Lean Elab Command

namespace RootPoolBudgetDependencyAudit

private def roots : Array Name :=
  #[`CollatzShadowing.RootPoolBudget.normalizedWeight_nonneg,
    `CollatzShadowing.RootPoolBudget.normalizedWeight_eq_loss,
    `CollatzShadowing.RootPoolBudget.sum_normalizedWeight_le,
    `CollatzShadowing.RootPoolBudget.sum_selected_le,
    `CollatzShadowing.RootPoolBudget.sum_labeled_normalizedWeight_le,
    `CollatzShadowing.RootPoolBudget.normalized_source_fiber_bound,
    `CollatzShadowing.RootPoolBudget.distinct_sources_of_normalized_mass,
    `CollatzShadowing.RootPoolBudget.pool_visit_time_unique,
    `CollatzShadowing.RootPoolBudget.word_eq_of_pool,
    `CollatzShadowing.RootPoolBudget.reciprocalWeight_le_initial,
    `CollatzShadowing.RootPoolBudget.sum_reciprocalWeight_pool_le,
    `CollatzShadowing.RootPoolBudget.sum_labeled_reciprocalWeight_pool_le]

private def run : CommandElabM Unit := do
  let env := (← getEnv).setExporting false
  for root in roots do
    unless (env.find? root).isSome do
      throwError "Missing audited theorem: {root}"
    let axioms ← Lean.collectAxioms root
    for ax in axioms do
      unless ax == `propext || ax == `Classical.choice || ax == `Quot.sound do
        throwError "Unexpected axiom in {root}: {ax}"
    logInfo m!"ROOT_POOL_BUDGET_ROOT_AUDIT: PASS {root}; axioms: {axioms.toList}"
  logInfo m!"ROOT_POOL_BUDGET_AUDIT: PASS; roots: {roots.size}"

set_option maxHeartbeats 0 in
run_cmd run

end RootPoolBudgetDependencyAudit
