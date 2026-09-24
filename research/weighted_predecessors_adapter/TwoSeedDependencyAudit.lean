/-
SPDX-License-Identifier: Apache-2.0
Dependency audit for Piero Borgatta's finite-two-seed predecessor development.
Produced with AI assistance, 2026-09-24.
-/

import TwoSeedDensity
import Lean

/-!
# Complete dependency audit for the modular finite-two-seed theorem

This audit imports `TwoSeedDensity` as a module. It traverses every reachable
declaration type and available body using `Environment.find?`, including
private helpers and third-party declarations, without a module/name filter.
Run it from the assembled external project's Lake environment after building
the adapter modules; the audit source itself may be given as an absolute path.

The old non-returning census is allowed. The old unbounded seed choosers are
not: the public quantitative theorem must reach the new bounded-pair lemma
and the same-image non-return argument. The only permitted axioms are the
three standard Lean axioms listed below.

These checks inspect the actual named dependency graph. They are not an
independent kernel checker, an audit of every imported analytic argument, or
a proof that every referenced lemma is logically indispensable.
-/

open Lean Elab Command

namespace TwoSeedDependencyAudit

private def lastComponentIs (name : Name) (last : String) : Bool :=
  match name with
  | .str _ s => s == last
  | _ => false

private def forbidden (name : Name) : Bool :=
  lastComponentIs name "exists_bound_predecessor_no_return" ||
    lastComponentIs name "exists_large_nonreturning_predecessor_in_residue"

private def isStandardAxiom (name : Name) : Bool :=
  name == `propext || name == `Classical.choice || name == `Quot.sound

private def run : CommandElabM Unit := do
  let env := (← getEnv).setExporting false
  let root :=
    `Erdos1135.ND.PositiveDensity.TwoSeedDensity.generalTarget_predecessors_explicit_lower_bound
  let required :=
    #[`Erdos1135.ND.PositiveDensity.TwoSeedNonreturn.exists_bounded_nonreturning_predecessor_in_residue,
      `Erdos1135.ND.PositiveDensity.TwoSeedNonreturn.noReturn_or_noReturn_of_same_image]
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

  logInfo m!"TWO_SEED_DEPENDENCY_AUDIT: PASS"
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
  logInfo m!"build scope: imported TwoSeedDensity module; no assembled verification bundle"

set_option maxHeartbeats 0 in
run_cmd run

end TwoSeedDependencyAudit

#print axioms Erdos1135.ND.PositiveDensity.TwoSeedDensity.generalTarget_predecessors_explicit_lower_bound
