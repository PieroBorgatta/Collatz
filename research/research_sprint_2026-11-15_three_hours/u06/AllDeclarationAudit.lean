/-
Audit every compiled declaration in the QuadraticOccupation module,
including definitions, generated declarations and encoded-private helpers.
Only standard logical axioms are allowed. Dependencies are inspected
transitively. This is a pinned local audit, not an independent-kernel replay.
-/
import CollatzShadowing.QuadraticOccupation
import Lean

open Lean Elab Command

namespace QuadraticOccupationLocalAudit

private def modules : Array String := #["CollatzShadowing.QuadraticOccupation"]

private def belongs (name : Name) : Bool :=
  let s := name.toString
  modules.any fun m => s.startsWith (m ++ ".") || s.startsWith ("_private." ++ m ++ ".")

private def allowed (name : Name) : Bool :=
  name == `propext || name == `Classical.choice || name == `Quot.sound

private def run : CommandElabM Unit := do
  let env := (← getEnv).setExporting false
  let roots ← env.constants.foldM (init := (#[] : Array Name)) fun roots name _ => do
    return if belongs name then roots.push name else roots
  unless roots.size > 0 do
    throwError "No new-module declarations found"
  let roots := roots.qsort fun a b => a.toString < b.toString
  for m in modules do
    unless roots.any (fun n => n.toString.startsWith (m ++ ".")) do
      throwError "No public declarations found for {m}"
  for root in roots do
    let axioms ← Lean.collectAxioms root
    for ax in axioms do
      unless allowed ax do
        throwError "Unexpected axiom in {root}: {ax}"
    logInfo m!"QUADRATIC_ROOT: PASS {root}; axioms: {axioms.toList}"
  let privateCount := (roots.filter fun n => n.toString.startsWith "_private.").size
  logInfo m!"QUADRATIC_AUDIT: PASS; declarations: {roots.size}; encoded-private: {privateCount}; modules: {modules.size}"

set_option maxHeartbeats 0 in
run_cmd run

end QuadraticOccupationLocalAudit
