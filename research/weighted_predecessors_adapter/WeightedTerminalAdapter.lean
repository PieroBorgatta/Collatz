import Erdos1135.ND.PositiveDensity.Geom2ShiftedWideSymmetricRootUniformGroupedCapacity
import Erdos1135.ND.PositiveDensity.Geom2ShiftedWideSymmetricCoreBackwardMean
import WeightedPathOccupation

/-!
# Exact-word encoding of a fixed-stage terminal family

This adapter uses the public slim v2.1 baseline. A fixed initial owner and
whole exact valuation word determine a terminal incidence. No non-return or
convergence hypothesis is used. The incidence weight is the initial owner
weight times the exact word weight.
-/

namespace Erdos1135.ND.PositiveDensity

open scoped BigOperators

noncomputable section

namespace WeightedTerminalAdapter

theorem wordAtom_reverse (w : List ℕ+) :
    ndRootUniformWordAtom w.reverse = ndRootUniformWordAtom w := by
  simp only [ndRootUniformWordAtom, List.length_reverse, Tao.taoTupleWeight_reverse]

theorem terminalAtom_eq_wordAtom
    {Label : Type*} {root base shift : Label → ℕ} {K : ℕ}
    (z : NDGeom2PredictableRootSideBoundedOvershootIncidence
      Label root base shift K) :
    ndGeom2PredictableRootSideBoundedOvershootIncidenceAtom z =
      ndRootUniformWordAtom
        (ndGeom2PredictableRootSideBoundedOvershootIncidenceRootSideWord z) := by
  unfold ndGeom2PredictableRootSideBoundedOvershootIncidenceAtom ndRootUniformWordAtom
  rw [← ndGeom2PredictableRootSideBoundedOvershootIncidence_word_length z,
    referencePrefix_atom_eq]
  simp only [zpow_neg, zpow_natCast, div_eq_mul_inv]

open NDGeom2ShiftedWideSymmetricRootSideUniformFloorState

theorem terminalWeight_eq_ownerWeight_mul_wholeWordAtom
    (U : NDGeom2ShiftedWideSymmetricRootSideUniformFloorState)
    (cap : ℕ → ℕ) (n : ℕ)
    (shift : (U.forwardIterate cap n).state.Label → ℕ) (K : ℕ)
    (z : U.FullTerminalAt cap n shift K) :
    ndGeom2PredictableRootSideBoundedOvershootIncidenceWeight
        (U.forwardIterate cap n).state.outerWeight z =
      U.state.outerWeight (fullTerminalAncestor z) *
        ndRootUniformWordAtom (fullTerminalWord z) := by
  rw [ndGeom2PredictableRootSideBoundedOvershootIncidenceWeight,
    U.forwardWeight_eq_ownerWeight_mul_wordAtom cap n,
    terminalAtom_eq_wordAtom, fullTerminalWord, rootUniformWordAtom_append]
  simp only [fullTerminalAncestor, mul_assoc]

theorem terminalWeight_eq_ownerWeight_mul_pathWordAtom
    (U : NDGeom2ShiftedWideSymmetricRootSideUniformFloorState)
    (cap : ℕ → ℕ) (n : ℕ)
    (shift : (U.forwardIterate cap n).state.Label → ℕ) (K : ℕ)
    (z : U.FullTerminalAt cap n shift K) :
    ndGeom2PredictableRootSideBoundedOvershootIncidenceWeight
        (U.forwardIterate cap n).state.outerWeight z =
      U.state.outerWeight (fullTerminalAncestor z) *
        ndRootUniformWordAtom (U.fullTerminalPath cap n shift K z).word := by
  rw [U.fullTerminalPath_word_eq_reverse, wordAtom_reverse]
  exact terminalWeight_eq_ownerWeight_mul_wholeWordAtom U cap n shift K z

theorem terminalWeight_eq_pathWordAtom_of_ownerWeight_one
    (U : NDGeom2ShiftedWideSymmetricRootSideUniformFloorState)
    (hone : ∀ i, U.state.outerWeight i = 1)
    (cap : ℕ → ℕ) (n : ℕ)
    (shift : (U.forwardIterate cap n).state.Label → ℕ) (K : ℕ)
    (z : U.FullTerminalAt cap n shift K) :
    ndGeom2PredictableRootSideBoundedOvershootIncidenceWeight
        (U.forwardIterate cap n).state.outerWeight z =
      ndRootUniformWordAtom (U.fullTerminalPath cap n shift K z).word := by
  simpa only [hone, one_mul] using
    terminalWeight_eq_ownerWeight_mul_pathWordAtom U cap n shift K z

/-- Whole words identify incidences whenever the initial owner is unique. -/
theorem terminal_pathWord_injective
    (U : NDGeom2ShiftedWideSymmetricRootSideUniformFloorState)
    [Subsingleton U.state.Label]
    (cap : ℕ → ℕ) (n : ℕ)
    (shift : (U.forwardIterate cap n).state.Label → ℕ) (K : ℕ) :
    Function.Injective (fun z : U.FullTerminalAt cap n shift K =>
      (U.fullTerminalPath cap n shift K z).word) := by
  intro z w hw
  apply fullTerminal_eq_of_ancestor_word_eq (Subsingleton.elim _ _)
  apply List.reverse_injective
  exact (U.fullTerminalPath_word_eq_reverse cap n shift K z).symm.trans
    (hw.trans (U.fullTerminalPath_word_eq_reverse cap n shift K w))

/-- An orbit fixes the word at a given source and depth; no unique hitting
time assumption is required. This is the encoding needed by a fiber bound. -/
theorem terminal_source_depth_injective
    (U : NDGeom2ShiftedWideSymmetricRootSideUniformFloorState)
    [Subsingleton U.state.Label]
    (cap : ℕ → ℕ) (n : ℕ)
    (shift : (U.forwardIterate cap n).state.Label → ℕ) (K : ℕ) :
    Function.Injective (fun z : U.FullTerminalAt cap n shift K =>
      (ndGeom2PredictableRootSideBoundedOvershootIncidenceSource z,
        (U.fullTerminalPath cap n shift K z).depth)) := by
  intro z w h
  apply terminal_pathWord_injective U cap n shift K
  exact NDGeom2RootSideSyracusePath.word_eq_of_source_depth_eq
    (U.fullTerminalPath cap n shift K z)
    (U.fullTerminalPath cap n shift K w)
    (congrArg Prod.fst h) (congrArg Prod.snd h)

/-- In the concrete singleton state the common terminal is definitionally R. -/
def singletonTerminalPath
    (b R : ℕ) (hb : 200 ≤ b) (hR : Odd R) (hl : 16 ^ b ≤ R)
    (cap : ℕ → ℕ) (n : ℕ)
    (shift : ((ndRootCoreSingletonState b R hb hR hl).forwardIterate cap n).state.Label → ℕ)
    (K : ℕ)
    (z : (ndRootCoreSingletonState b R hb hR hl).FullTerminalAt cap n shift K) :
    NDGeom2RootSideSyracusePath
      (ndGeom2PredictableRootSideBoundedOvershootIncidenceSource z) R :=
  (ndRootCoreSingletonState b R hb hR hl).fullTerminalPath cap n shift K z

theorem singletonTerminalWeight_eq_pathWordAtom
    (b R : ℕ) (hb : 200 ≤ b) (hR : Odd R) (hl : 16 ^ b ≤ R)
    (cap : ℕ → ℕ) (n : ℕ)
    (shift : ((ndRootCoreSingletonState b R hb hR hl).forwardIterate cap n).state.Label → ℕ)
    (K : ℕ)
    (z : (ndRootCoreSingletonState b R hb hR hl).FullTerminalAt cap n shift K) :
    ndGeom2PredictableRootSideBoundedOvershootIncidenceWeight
        ((ndRootCoreSingletonState b R hb hR hl).forwardIterate cap n).state.outerWeight z =
      ndRootUniformWordAtom (singletonTerminalPath b R hb hR hl cap n shift K z).word := by
  exact terminalWeight_eq_pathWordAtom_of_ownerWeight_one
    (ndRootCoreSingletonState b R hb hR hl) (fun _ => rfl) cap n shift K z

theorem singletonTerminal_pathWord_injective
    (b R : ℕ) (hb : 200 ≤ b) (hR : Odd R) (hl : 16 ^ b ≤ R)
    (cap : ℕ → ℕ) (n : ℕ)
    (shift : ((ndRootCoreSingletonState b R hb hR hl).forwardIterate cap n).state.Label → ℕ)
    (K : ℕ) :
    Function.Injective (fun z :
      (ndRootCoreSingletonState b R hb hR hl).FullTerminalAt cap n shift K =>
        (singletonTerminalPath b R hb hR hl cap n shift K z).word) := by
  letI : Subsingleton (ndRootCoreSingletonState b R hb hR hl).state.Label := by
    change Subsingleton Unit
    infer_instance
  exact terminal_pathWord_injective (ndRootCoreSingletonState b R hb hR hl) cap n shift K

theorem singletonTerminal_source_depth_injective
    (b R : ℕ) (hb : 200 ≤ b) (hR : Odd R) (hl : 16 ^ b ≤ R)
    (cap : ℕ → ℕ) (n : ℕ)
    (shift : ((ndRootCoreSingletonState b R hb hR hl).forwardIterate cap n).state.Label → ℕ)
    (K : ℕ) :
    Function.Injective (fun z :
      (ndRootCoreSingletonState b R hb hR hl).FullTerminalAt cap n shift K =>
        (ndGeom2PredictableRootSideBoundedOvershootIncidenceSource z,
          (singletonTerminalPath b R hb hR hl cap n shift K z).depth)) := by
  letI : Subsingleton (ndRootCoreSingletonState b R hb hR hl).state.Label := by
    change Subsingleton Unit
    infer_instance
  exact terminal_source_depth_injective (ndRootCoreSingletonState b R hb hR hl) cap n shift K

/-- Concrete replacement for the old non-returning-seed source charge.
The cost is `R * (3 * R + 1)` instead of `R`, while repeated visits and
periodic endpoints remain allowed. -/
theorem singletonTerminal_weighted_source_bound
    (b R : ℕ) (hb : 200 ≤ b) (hR : Odd R) (hl : 16 ^ b ≤ R)
    (cap : ℕ → ℕ) (n : ℕ)
    (shift : ((ndRootCoreSingletonState b R hb hR hl).forwardIterate cap n).state.Label → ℕ)
    (K : ℕ) (X : ℝ) (hX : 0 < X)
    (hsource : ∀ z : (ndRootCoreSingletonState b R hb hR hl).FullTerminalAt cap n shift K,
      X ≤ (ndGeom2PredictableRootSideBoundedOvershootIncidenceSource z : ℝ))
    (psi : ℕ → ℝ) (hpsi : ∀ x, 0 ≤ psi x) :
    let U := ndRootCoreSingletonState b R hb hR hl;
    letI := (U.forwardIterate cap n).state.labelFintype;
    (∑ z : U.FullTerminalAt cap n shift K,
      ndGeom2PredictableRootSideBoundedOvershootIncidenceWeight
        (U.forwardIterate cap n).state.outerWeight z *
        psi (ndGeom2PredictableRootSideBoundedOvershootIncidenceSource z)) ≤
      ((R : ℝ) * (3 * (R : ℝ) + 1) / X) *
        ∑ x ∈ U.fullTerminalSources cap n shift K, psi x := by
  classical
  let U := ndRootCoreSingletonState b R hb hR hl
  letI := (U.forwardIterate cap n).state.labelFintype
  have h := WeightedPathOccupation.weighted_source_bound
    (fun z : U.FullTerminalAt cap n shift K =>
      ndGeom2PredictableRootSideBoundedOvershootIncidenceSource z)
    (singletonTerminalPath b R hb hR hl cap n shift K)
    (singletonTerminal_source_depth_injective b R hb hR hl cap n shift K)
    hX hsource psi hpsi
  simpa only [← singletonTerminalWeight_eq_pathWordAtom b R hb hR hl cap n shift K,
    U, fullTerminalSources] using h

end WeightedTerminalAdapter

end

end Erdos1135.ND.PositiveDensity
