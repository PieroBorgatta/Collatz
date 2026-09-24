/-
SPDX-License-Identifier: Apache-2.0
Dependency audit for Piero Borgatta's finite-two-seed predecessor development.
Produced with AI assistance, 2026-09-24.
-/

import OptimizedComparison
import Lean

/-!
# Complete dependency audit for the optimized predecessor theorem

Traverse every reachable declaration type and available body, including private
helpers and external libraries. Require the compact seed construction, the
same-image nonreturn argument, the sixth-power mixing conversion, and its
finite conductor budget. Reject both the original unbounded choosers and a
fallback to the preceding wide-seed density theorem. Only the three standard
axioms are permitted. Quantitative comparison roots are audited separately.

This reads the named dependency graph; it is not an independent kernel checker
or an independent review of every imported analytic argument.
-/

open Lean Elab Command

namespace OptimizedDependencyAudit

private def lastComponentIs (name : Name) (last : String) : Bool :=
  match name with
  | .str _ s => s == last
  | _ => false

private def forbidden (name : Name) : Bool :=
  lastComponentIs name "exists_bound_predecessor_no_return" ||
    lastComponentIs name "exists_large_nonreturning_predecessor_in_residue" ||
    name == `Erdos1135.ND.PositiveDensity.TwoSeedNonreturn.exists_bounded_nonreturning_predecessor_in_residue ||
    name == `Erdos1135.ND.PositiveDensity.TwoSeedDensity.predecessor_count_of_mixing ||
    name == `Erdos1135.ND.PositiveDensity.TwoSeedDensity.generalTarget_predecessors_explicit_lower_bound

private def isStandardAxiom (name : Name) : Bool :=
  name == `propext || name == `Classical.choice || name == `Quot.sound

private def run : CommandElabM Unit := do
  let env := (← getEnv).setExporting false
  let root :=
    `Erdos1135.ND.PositiveDensity.OptimizedDensity.generalTarget_predecessors_explicit_lower_bound
  let required :=
    #[`Erdos1135.ND.PositiveDensity.CompactSeedNonreturn.exists_bounded_nonreturning_predecessor_in_residue,
      `Erdos1135.ND.PositiveDensity.TwoSeedNonreturn.noReturn_or_noReturn_of_same_image,
      `Erdos1135.ND.PositiveDensity.OptimizedConductor.scaled_quadratic_mixing,
      `Erdos1135.ND.PositiveDensity.OptimizedConductor.conductor_budget]
  for name in #[root] ++ required do
    unless (env.find? name).isSome do
      throwError "Required declaration not found in the environment: {name}"

  let mut todo : Array Name := #[root]
  let mut seen : NameSet := {}
  let mut visitedAxioms : NameSet := {}
  let mut privateCount : Nat := 0
  let mut bodies : Nat := 0
  let mut edges : Nat := 0
  while !todo.isEmpty do
    let name := todo.back!
    todo := todo.pop
    if seen.contains name then
      continue
    seen := seen.insert name
    if forbidden name then
      throwError "Forbidden unbounded seed dependency reached from '{root}': {name}"
    let some info := env.find? name |
      throwError "Incomplete traversal: reachable declaration not found: {name}"
    if name.toString.startsWith "_private." then
      privateCount := privateCount + 1
    if (info.value? (allowOpaque := true)).isSome then
      bodies := bodies + 1
    match info with
    | .axiomInfo _ =>
      visitedAxioms := visitedAxioms.insert name
      unless isStandardAxiom name do
        throwError "Unexpected axiom reached by direct traversal: {name}"
    | _ => pure ()
    -- Includes types and theorem/opaque/definition bodies, plus the links
    -- supplied by Lean for inductive declarations and recursors.
    let deps := info.getUsedConstantsAsSet.toArray
    edges := edges + deps.size
    todo := todo ++ deps

  for name in required do
    unless seen.contains name do
      throwError "Required new dependency is disconnected from '{root}': {name}"

  let collectedAxioms ← Lean.collectAxioms root
  for ax in collectedAxioms do
    unless isStandardAxiom ax do
      throwError "Unexpected axiom reported by collectAxioms: {ax}"

  let comparisonRoots :=
    #[`Erdos1135.ND.PositiveDensity.OptimizedComparison.public_constants_strictly_improve,
      `Erdos1135.ND.PositiveDensity.OptimizedComparison.old_coefficient_lt,
      `Erdos1135.ND.PositiveDensity.OptimizedComparison.cutoff_lt,
      `Erdos1135.ND.PositiveDensity.OptimizedConductor.conductor_minimal]
  for name in comparisonRoots do
    unless (env.find? name).isSome do
      throwError "Comparison declaration missing: {name}"
    let axioms ← Lean.collectAxioms name
    for ax in axioms do
      unless isStandardAxiom ax do
        throwError "Unexpected comparison axiom in '{name}': {ax}"
    logInfo m!"COMPARISON_AXIOM_AUDIT: PASS {name}; axioms: {axioms.toList}"

  logInfo m!"OPTIMIZED_DEPENDENCY_AUDIT: PASS"
  logInfo m!"root: {root}"
  logInfo m!"reachable declarations inspected: {seen.toArray.size}"
  logInfo m!"private declarations inspected: {privateCount}"
  logInfo m!"declaration bodies inspected: {bodies}"
  logInfo m!"type/body dependency edges inspected: {edges}"
  logInfo m!"required dependencies reached: {required.toList}"
  logInfo m!"forbidden unbounded seed dependencies: absent"
  logInfo m!"axioms reached by complete traversal: {visitedAxioms.toArray.toList}"
  logInfo m!"axioms reported by collectAxioms: {collectedAxioms.toList}"
  logInfo m!"traversal boundary: none; every reachable named declaration inspected"
  logInfo m!"build scope: imported OptimizedDensity module through OptimizedComparison; no assembled verification bundle"

set_option maxHeartbeats 0 in
run_cmd run

end OptimizedDependencyAudit

#print axioms Erdos1135.ND.PositiveDensity.OptimizedDensity.generalTarget_predecessors_explicit_lower_bound

-- Executable smoke checks of the new natural-valued search, not proof substitutes.
#eval do
  let actual := [Erdos1135.ND.PositiveDensity.OptimizedConductor.conductor 0 7,
    Erdos1135.ND.PositiveDensity.OptimizedConductor.conductor 1 0, Erdos1135.ND.PositiveDensity.OptimizedConductor.conductor 1 1,
    Erdos1135.ND.PositiveDensity.OptimizedConductor.conductor 100 1]
  unless actual == [1, 1, 3, 5] do
    throw (IO.userError s!"Unexpected conductor values: {actual}")
  IO.println s!"CONDUCTOR_EXECUTION_SMOKE: PASS {actual}"
