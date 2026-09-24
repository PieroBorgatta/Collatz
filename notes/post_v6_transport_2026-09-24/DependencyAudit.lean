/-
SPDX-License-Identifier: Apache-2.0
AI-assisted dependency audit for the post-v6 tower parameter development.
Reuses the traversal pattern of the repository's optimized predecessor audit.
This is a named type/body dependency audit, not an independent kernel checker.
-/
import CollatzShadowing.TowerSuffix
import Lean

open Lean Elab Command

namespace TowerTransportAudit

private def allowed (name : Name) : Bool :=
  name == `propext || name == `Classical.choice || name == `Quot.sound

private def roots : Array Name :=
  #[`CollatzShadowing.TowerParameter.quotient_difference_valuation,
    `CollatzShadowing.TowerParameter.quotient_modEq_iff,
    `CollatzShadowing.TowerParameter.quotient_residue_bijective,
    `CollatzShadowing.TowerParameter.suffix_iff_affine_residue,
    `CollatzShadowing.TowerParameter.finite_suffix_residue,
    `CollatzShadowing.TowerParameter.finite_suffix_arbitrarily_large,
    `CollatzShadowing.TowerParameter.phaseB_exit_burst,
    `CollatzShadowing.TowerParameter.phaseC_tower_burst,
    `CollatzShadowing.TowerParameter.tower_finite_suffix_arbitrarily_large,
    `CollatzShadowing.TowerParameter.tower_delayed_compensation,
    `CollatzShadowing.TowerParameter.finite_suffix_bounded_iff]

private def run : CommandElabM Unit := do
  let env := (← getEnv).setExporting false
  for root in roots do
    unless (env.find? root).isSome do
      throwError "Missing audited theorem: {root}"
    let axioms ← Lean.collectAxioms root
    for ax in axioms do
      unless allowed ax do
        throwError "Unexpected axiom in {root}: {ax}"
    logInfo m!"TOWER_ROOT_AUDIT: PASS {root}; axioms: {axioms.toList}"
  let mut todo := roots
  let mut seen : NameSet := {}
  let mut axioms : NameSet := {}
  let mut privateCount := 0
  let mut bodies := 0
  let mut edges := 0
  while !todo.isEmpty do
    let name := todo.back!
    todo := todo.pop
    if seen.contains name then continue
    seen := seen.insert name
    let some info := env.find? name |
      throwError "Missing reachable declaration: {name}"
    if name.toString.startsWith "_private." then privateCount := privateCount + 1
    if (info.value? (allowOpaque := true)).isSome then bodies := bodies + 1
    match info with
    | .axiomInfo _ =>
      unless allowed name do throwError "Unexpected reachable axiom: {name}"
      axioms := axioms.insert name
    | _ => pure ()
    let deps := info.getUsedConstantsAsSet.toArray
    edges := edges + deps.size
    todo := todo ++ deps
  for required in #[`CollatzShadowing.TowerParameter.numerator_valuation,
      `CollatzShadowing.syracuseWordMatches_iff_exactResidue,
      `CollatzShadowing.cancellationTower_iterate] do
    unless seen.contains required do
      throwError "Required arithmetic/orbit connection absent: {required}"
  logInfo m!"TOWER_DEPENDENCY_AUDIT: PASS"
  logInfo m!"roots: {roots.size}"
  logInfo m!"reachable declarations: {seen.toArray.size}"
  logInfo m!"private declarations: {privateCount}"
  logInfo m!"declaration bodies: {bodies}"
  logInfo m!"type/body edges: {edges}"
  logInfo m!"axioms: {axioms.toArray.toList}"

set_option maxHeartbeats 0 in
run_cmd run

end TowerTransportAudit
