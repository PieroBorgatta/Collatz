/- Strict root audit for the signed-transport arithmetic, 2026-09-26.
AI-assisted (Codex) with Piero Borgatta. Not an independent kernel checker. -/
import CollatzShadowing.SignedTransport
import Lean

open Lean Elab Command

namespace SignedTransportDependencyAudit

private def roots : Array Name :=
  #[`CollatzShadowing.SignedTransport.affine_comparison,
    `CollatzShadowing.SignedTransport.odd_ne_two_pow_mul,
    `CollatzShadowing.SignedTransport.congruent_shift_requires_large,
    `CollatzShadowing.SignedTransport.positive_shift_expands,
    `CollatzShadowing.SignedTransport.negative_shift_compresses,
    `CollatzShadowing.SignedTransport.lift_comparison]

private def run : CommandElabM Unit := do
  let env := (← getEnv).setExporting false
  for root in roots do
    unless (env.find? root).isSome do
      throwError "Missing audited theorem: {root}"
    let axioms ← Lean.collectAxioms root
    for ax in axioms do
      unless ax == `propext || ax == `Classical.choice || ax == `Quot.sound do
        throwError "Unexpected axiom in {root}: {ax}"
    logInfo m!"SIGNED_TRANSPORT_ROOT_AUDIT: PASS {root}; axioms: {axioms.toList}"
  logInfo m!"SIGNED_TRANSPORT_AUDIT: PASS; roots: {roots.size}"

set_option maxHeartbeats 0 in
run_cmd run

end SignedTransportDependencyAudit
