/- Strict root audit for the last-exponent transport, 2026-09-26.
AI-assisted (Codex) with Piero Borgatta. Not an independent kernel checker. -/
import CollatzShadowing.LastExponentTransport
import Lean

open Lean Elab Command

namespace LastExponentDependencyAudit

private def roots : Array Name :=
  #[`CollatzShadowing.LastExponentTransport.matches_and_endpoint_of_affine,
    `CollatzShadowing.LastExponentTransport.last_constant_unchanged,
    `CollatzShadowing.LastExponentTransport.last_exponent_transport,
    `CollatzShadowing.LastExponentTransport.correction_positive,
    `CollatzShadowing.LastExponentTransport.transport_height_cost,
    `CollatzShadowing.LastExponentTransport.last_exponent_height_cost,
    `CollatzShadowing.LastExponentTransport.not_bounded_height]

private def run : CommandElabM Unit := do
  let env := (← getEnv).setExporting false
  for root in roots do
    unless (env.find? root).isSome do
      throwError "Missing audited theorem: {root}"
    let axioms ← Lean.collectAxioms root
    for ax in axioms do
      unless ax == `propext || ax == `Classical.choice || ax == `Quot.sound do
        throwError "Unexpected axiom in {root}: {ax}"
    logInfo m!"LAST_EXPONENT_ROOT_AUDIT: PASS {root}; axioms: {axioms.toList}"
  logInfo m!"LAST_EXPONENT_AUDIT: PASS; roots: {roots.size}"

set_option maxHeartbeats 0 in
run_cmd run

end LastExponentDependencyAudit
