import WeightedPredecessorDensity
import Lean

/-!
# Read-only dependency audit for the weighted predecessor theorem

This command traverses declaration types and proof/definition bodies in the
kernel environment. Local declarations are selected by their owning module
index, not by their declaration-name prefix; private helper declarations are
therefore included. It deliberately stops at third-party module boundaries.

This is a dependency audit, not an independent kernel checker or a proof of
logical indispensability of each dependency. A successful invocation throws
no errors, confirms the new occupation and residue lemmas are connected, and
excludes the old non-returning-seed route and old final theorem.
-/

open Lean Elab Command

namespace WeightedDependencyAudit

private def ownerModule? (env : Environment) (name : Name) : Option Name := do
  let idx ← env.getModuleIdxFor? name
  env.allImportedModuleNames[idx.toNat]?

private def isLocalModule (name : Name) : Bool :=
  let s := name.toString
  s == "Erdos1135" || s.startsWith "Erdos1135." ||
    s.startsWith "Weighted" || s == "CollatzPredecessorDensity"

private def isLocalDecl (env : Environment) (name : Name) : Bool :=
  match ownerModule? env name with
  | some mod => isLocalModule mod
  | none => false

private def lastComponentIs (name : Name) (last : String) : Bool :=
  match name with
  | .str _ s => s == last
  | _ => false

private def findUniquePublicDecl (env : Environment) (last : String) : CommandElabM Name := do
  let candidates := env.constants.fold (init := (#[] : Array Name)) fun acc name _ =>
    if lastComponentIs name last && !name.isInternal then acc.push name else acc
  match candidates.toList with
  | [name] => pure name
  | [] => throwError "Required audit declaration '{last}' was not found"
  | _ => throwError "Audit declaration suffix '{last}' is ambiguous: {candidates.toList}"

private def forbidden (name : Name) : Bool :=
  let s := name.toString
  s.contains "nonreturningSeed" ||
    lastComponentIs name "exists_bound_predecessor_no_return" ||
    lastComponentIs name "exists_large_nonreturning_predecessor_in_residue" ||
    lastComponentIs name "generalTarget_predecessors_positive_lower_density" ||
    name == `CollatzPredecessorDensity.predecessors_positive_lower_density

private def isStandardAxiom (name : Name) : Bool :=
  name == `propext || name == `Classical.choice || name == `Quot.sound

private def run : CommandElabM Unit := do
  let env := (← getEnv).setExporting false
  let root ← findUniquePublicDecl env "weighted_predecessors_positive_lower_density"
  let residue ← findUniquePublicDecl env "weighted_exists_large_predecessor_in_residue"
  let occupation :=
    `Erdos1135.ND.PositiveDensity.WeightedPathOccupation.sum_weight_visits_le
  for name in #[root, residue, occupation] do
    unless isLocalDecl env name do
      throwError "Expected a local imported module owner for '{name}', got {ownerModule? env name}"
    unless (env.checked.get.find? name).isSome do
      throwError "Required declaration '{name}' is absent from the checked kernel environment"

  let mut todo : Array Name := #[root]
  let mut seen : NameSet := {}
  let mut expanded : NameSet := {}
  let mut localModules : NameSet := {}
  let mut frontier : NameSet := {}
  let mut privateCount : Nat := 0
  let mut typeValueEdges : Nat := 0
  while !todo.isEmpty do
    let name := todo.back!
    todo := todo.pop
    if seen.contains name then
      continue
    seen := seen.insert name
    if forbidden name then
      throwError "Forbidden old dependency reached from '{root}': {name}"
    if !isLocalDecl env name then
      frontier := frontier.insert name
      continue
    let some info := env.checked.get.find? name |
      throwError "Cannot inspect local kernel declaration '{name}'"
    expanded := expanded.insert name
    if name.toString.startsWith "_private." then
      privateCount := privateCount + 1
    if let some mod := ownerModule? env name then
      localModules := localModules.insert mod
    -- This API includes types, theorem/opaque bodies, definition bodies,
    -- and the constructor/recursor links of inductive declarations.
    let deps := info.getUsedConstantsAsSet.toArray
    typeValueEdges := typeValueEdges + deps.size
    todo := todo ++ deps

  for required in #[occupation, residue] do
    unless expanded.contains required do
      throwError "Expected new dependency '{required}' was not reached from '{root}'"

  let axioms ← Lean.collectAxioms root
  for ax in axioms do
    unless isStandardAxiom ax do
      throwError "Unexpected axiom in '{root}': {ax}"

  logInfo m!"WEIGHTED_DEPENDENCY_AUDIT: PASS"
  logInfo m!"root: {root}"
  logInfo m!"local declarations expanded: {expanded.toArray.size}"
  logInfo m!"private local declarations expanded: {privateCount}"
  logInfo m!"local owning modules: {localModules.toArray.size}"
  logInfo m!"type/body dependency edges inspected: {typeValueEdges}"
  logInfo m!"third-party/builtin frontier declarations: {frontier.toArray.size}"
  logInfo m!"required occupation dependency reached: {occupation}"
  logInfo m!"required constructive residue dependency reached: {residue}"
  logInfo m!"forbidden old non-returning-seed and old final-theorem dependencies: absent"
  logInfo m!"root axioms: {axioms.toList}"
  logInfo m!"scope: module-owned local transitive proof/type closure; imported third-party bodies not traversed"

set_option maxHeartbeats 0 in
run_cmd run

end WeightedDependencyAudit
