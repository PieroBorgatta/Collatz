import WeightedVerifiedBundle
import Lean

/-!
# Complete dependency checks on the assembled verification bundle

The imported `WeightedVerifiedBundle` is an assembled verification unit. It
is not claimed to be a successful per-module build of the original library.
This audit traverses every reachable declaration type and available body via
`Environment.find?`, including private helpers and third-party declarations;
it applies no module-index or declaration-name filter to traversal.

The two roots have different requirements. The occupation proof must avoid
the old non-returning-seed route altogether. The finite-two-seed proof may
use the old non-returning census, but must obtain its seed through the new
bounded-pair argument rather than the unknown cycle-height bound.

The checks inspect the actual proof dependency graph. They do not constitute
an independent kernel checker or establish logical indispensability of every
referenced lemma.
-/

open Lean Elab Command

namespace BundleDependencyAudit

private def lastComponentIs (name : Name) (last : String) : Bool :=
  match name with
  | .str _ s => s == last
  | _ => false

private def oldUnboundedChooser (name : Name) : Bool :=
  lastComponentIs name "exists_bound_predecessor_no_return" ||
    lastComponentIs name "exists_large_nonreturning_predecessor_in_residue"

private def oldPublicDensity (name : Name) : Bool :=
  lastComponentIs name "generalTarget_predecessors_positive_lower_density" ||
    name == `CollatzPredecessorDensity.predecessors_positive_lower_density

private def occupationForbidden (name : Name) : Bool :=
  oldUnboundedChooser name || oldPublicDensity name ||
    name.toString.contains "nonreturningSeed"

private def twoSeedForbidden (name : Name) : Bool :=
  oldUnboundedChooser name

private def isStandardAxiom (name : Name) : Bool :=
  name == `propext || name == `Classical.choice || name == `Quot.sound

private def checkRoot
    (label : String) (root : Name)
    (forbidden : Name → Bool) (required : Array Name) : CommandElabM Unit := do
  let env := (← getEnv).setExporting false
  for name in #[root] ++ required do
    unless (env.find? name).isSome do
      throwError "[{label}] Required declaration not found in the environment: {name}"

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
      throwError "[{label}] Forbidden dependency reached from '{root}': {name}"
    let some info := env.find? name |
      throwError "[{label}] Incomplete traversal: reachable declaration not found: {name}"
    if name.toString.startsWith "_private." then
      privateCount := privateCount + 1
    if (info.value? (allowOpaque := true)).isSome then
      bodies := bodies + 1
    match info with
    | .axiomInfo _ =>
      visitedAxioms := visitedAxioms.insert name
      unless isStandardAxiom name do
        throwError "[{label}] Unexpected axiom reached by direct traversal: {name}"
    | _ => pure ()
    -- Includes declaration types and theorem/opaque/definition bodies. For
    -- inductive declarations, constructor and recursor links are included.
    let deps := info.getUsedConstantsAsSet.toArray
    edges := edges + deps.size
    todo := todo ++ deps

  for name in required do
    unless seen.contains name do
      throwError "[{label}] Required new dependency is disconnected from '{root}': {name}"

  let collectedAxioms ← Lean.collectAxioms root
  for ax in collectedAxioms do
    unless isStandardAxiom ax do
      throwError "[{label}] Unexpected axiom reported by collectAxioms: {ax}"

  logInfo m!"BUNDLE_DEPENDENCY_AUDIT [{label}]: PASS"
  logInfo m!"root: {root}"
  logInfo m!"reachable declarations inspected: {seen.toArray.size}"
  logInfo m!"private declarations inspected: {privateCount}"
  logInfo m!"declaration bodies inspected: {bodies}"
  logInfo m!"type/body dependency edges inspected: {edges}"
  logInfo m!"required dependencies reached: {required.toList}"
  logInfo m!"forbidden dependencies: absent"
  logInfo m!"axioms reached by complete traversal: {visitedAxioms.toArray.toList}"
  logInfo m!"axioms reported by collectAxioms: {collectedAxioms.toList}"
  logInfo m!"traversal boundary: none; every reachable named declaration inspected"
  logInfo m!"build scope: assembled WeightedVerifiedBundle, not a per-module library rebuild"

set_option maxHeartbeats 0 in
run_cmd do
  checkRoot "weighted occupation"
    `Erdos1135.ND.PositiveDensity.weighted_predecessors_positive_lower_density
    occupationForbidden
    #[`Erdos1135.ND.PositiveDensity.WeightedPathOccupation.sum_weight_visits_le,
      `Erdos1135.ND.PositiveDensity.weighted_exists_large_predecessor_in_residue]
  checkRoot "finite pair of seeds"
    `Erdos1135.ND.PositiveDensity.TwoSeedDensity.generalTarget_predecessors_explicit_lower_bound
    twoSeedForbidden
    #[`Erdos1135.ND.PositiveDensity.TwoSeedNonreturn.exists_bounded_nonreturning_predecessor_in_residue,
      `Erdos1135.ND.PositiveDensity.TwoSeedNonreturn.noReturn_or_noReturn_of_same_image]

end BundleDependencyAudit

#print axioms Erdos1135.ND.PositiveDensity.weighted_predecessors_positive_lower_density
#print axioms Erdos1135.ND.PositiveDensity.TwoSeedDensity.generalTarget_predecessors_explicit_lower_bound
