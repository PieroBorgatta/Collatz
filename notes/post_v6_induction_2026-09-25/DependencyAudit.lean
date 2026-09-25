/- Named theorem dependency audit; not an independent kernel checker. -/
import CollatzShadowing.QuadraticTransfer
import Lean

open Lean Elab Command

namespace DescentTransferAudit

private def allowed (name : Name) : Bool :=
  name == `propext || name == `Classical.choice || name == `Quot.sound

private def roots : Array Name :=
  #[`CollatzShadowing.DescentCertificate.potential_le_initial,
    `CollatzShadowing.DescentCertificate.loss_le_budget,
    `CollatzShadowing.DescentCertificate.potential_lower_bound,
    `CollatzShadowing.DescentCertificate.exists_descent_of_certificate,
    `CollatzShadowing.DescentCertificate.exists_descent_of_budget,
    `CollatzShadowing.QuadraticTransfer.homogeneous_upper_bound,
    `CollatzShadowing.QuadraticTransfer.exists_descent_of_weight,
    `CollatzShadowing.QuadraticTransfer.exists_descent_of_relative_weight,
    `CollatzShadowing.QuadraticTransfer.exists_descent_of_lower_descent]

private def run : CommandElabM Unit := do
  let env := (← getEnv).setExporting false
  for root in roots do
    unless (env.find? root).isSome do
      throwError "Missing audited theorem: {root}"
    let axioms ← Lean.collectAxioms root
    for ax in axioms do
      unless allowed ax do
        throwError "Unexpected axiom in {root}: {ax}"
    logInfo m!"DESCENT_TRANSFER_ROOT_AUDIT: PASS {root}; axioms: {axioms.toList}"
  logInfo m!"DESCENT_TRANSFER_AUDIT: PASS; roots: {roots.size}"

set_option maxHeartbeats 0 in
run_cmd run

end DescentTransferAudit
