#!/usr/bin/env python3
"""
Exact merge audit for the depth-bounded A0 lazy-trie residual frontier.

This diagnostic never enumerates values of the A0 parameter ``t``.  It
consumes the symbolic affine leaves produced by ``a0_lazy_trie_prototype``
and asks whether two residual proof obligations can be merged without
forgetting any of the following data:

* the affine relation between the original source and the current endpoint;
* the last available precision-tax template, one of ``[1]``, ``[1, 2]``,
  and ``[2, 1]``;
* the exact pointwise 2-adic valuation profile of the corresponding phantom
  numerator ``x + 1``, ``x + 5``, or ``x + 7``.

The normal forms below are algebraic invariants, not hashes.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction
from typing import Hashable

from a0_lazy_trie_prototype import LazyA0Explorer, Linear, OrbitState
from symbolic_2adic_trie import valuation_nonzero


@dataclass(frozen=True)
class PrecisionTemplate:
    """One Lean-verified expansive phantom template."""

    name: str
    word: tuple[int, ...]
    numerator_shift: int


WORD_ONE = PrecisionTemplate("n+1", (1,), 1)
WORD_ONE_TWO = PrecisionTemplate("n+5", (1, 2), 5)
WORD_TWO_ONE = PrecisionTemplate("n+7", (2, 1), 7)


@dataclass(frozen=True)
class AffineRelation:
    """
    Coordinate-free identity ``current = slope * source + intercept``.

    Substituting any affine local coordinate into both ``source`` and
    ``current`` leaves this pair unchanged.  Equal pairs can therefore be
    covered by one exact affine theorem, even when their source cylinders
    are disjoint.
    """

    slope: Fraction
    intercept: Fraction


@dataclass(frozen=True)
class RootedValuationProfile:
    """
    Exact profile of ``v2(constant + coefficient*v)``.

    After removing ``2^common_v2``, the coefficient is odd and the rational
    root determines every root cylinder.  Two rooted profiles are equal iff
    the valuation functions agree pointwise (up to multiplication by an odd
    rational unit, which does not change ``v2``).
    """

    common_v2: int
    root: Fraction


@dataclass(frozen=True)
class UniformValuationProfile:
    """A valuation function that is constant on the whole local parameter."""

    valuation: int


ValuationProfile = RootedValuationProfile | UniformValuationProfile


@dataclass(frozen=True)
class PhantomAffineNormalForm:
    """
    Express the source through the active phantom numerator ``F``:

        source = source_per_phantom * F + source_at_phantom_zero.

    This identity is invariant under a common affine reparameterization of
    the source and current endpoint.
    """

    source_per_phantom: Fraction
    source_at_phantom_zero: Fraction


@dataclass(frozen=True)
class TracedMergeSignature:
    """
    Exact candidate signature for a state carrying a precision-tax trace.

    The template supplies the trace law, ``phantom_affine`` preserves the
    descent comparison, and ``valuation_profile`` preserves every local
    precision cylinder.  Dropping any of the three is not a sound residual
    quotient.
    """

    template: PrecisionTemplate
    phantom_affine: PhantomAffineNormalForm
    valuation_profile: ValuationProfile


@dataclass(frozen=True)
class UntracedMergeSignature:
    """
    Conservative exact signature when no current precision template applies.

    The whole exact suffix word is retained because there is no trace theorem
    justifying a cyclic identification.
    """

    exact_word: tuple[int, ...]
    affine_relation: AffineRelation


MergeSignature = TracedMergeSignature | UntracedMergeSignature


def last_precision_template(
    exact_word: tuple[int, ...],
) -> PrecisionTemplate | None:
    """Return the longest supported template that is a suffix of the word."""
    if exact_word[-2:] == WORD_ONE_TWO.word:
        return WORD_ONE_TWO
    if exact_word[-2:] == WORD_TWO_ONE.word:
        return WORD_TWO_ONE
    if exact_word[-1:] == WORD_ONE.word:
        return WORD_ONE
    return None


def applicable_precision_templates(
    exact_word: tuple[int, ...],
) -> tuple[PrecisionTemplate, ...]:
    """
    Return every supported suffix template, not just the longest one.

    A word ending in ``[2, 1]`` admits both the two-step ``n + 7`` trace and
    the one-step ``n + 1`` trace.  Auditing both prevents the canonical
    longest-template choice from hiding a possible exact merge.
    """
    return tuple(
        template
        for template in (WORD_ONE, WORD_ONE_TWO, WORD_TWO_ONE)
        if exact_word[-len(template.word) :] == template.word
    )


def affine_relation(state: OrbitState) -> AffineRelation:
    """Normalize ``state.current`` as an exact affine function of the source."""
    source = state.source
    current = state.current
    slope = Fraction(current.coefficient, source.coefficient)
    intercept = Fraction(current.constant) - slope * source.constant
    relation = AffineRelation(slope, intercept)

    # Algebraic identity check; no parameter value is sampled.
    assert relation.slope * source.coefficient == current.coefficient
    assert (
        relation.slope * source.constant + relation.intercept
        == current.constant
    )
    return relation


def valuation_profile(form: Linear) -> ValuationProfile:
    """
    Return the exact pointwise valuation normal form of a positive affine form.

    If ``v2(constant) < v2(coefficient)``, the ultrametric inequality makes
    the valuation uniform.  Otherwise the coefficient can be made odd by
    removing its full power of two, and the resulting rational root encodes
    the complete nested root spine.
    """
    constant_v2 = valuation_nonzero(form.constant)
    coefficient_v2 = valuation_nonzero(form.coefficient)
    if constant_v2 < coefficient_v2:
        return UniformValuationProfile(constant_v2)

    divisor = 1 << coefficient_v2
    assert form.constant % divisor == 0
    reduced_constant = form.constant // divisor
    reduced_coefficient = form.coefficient // divisor
    assert reduced_coefficient % 2 == 1
    return RootedValuationProfile(
        common_v2=coefficient_v2,
        root=Fraction(-reduced_constant, reduced_coefficient),
    )


def phantom_affine_normal_form(
    state: OrbitState,
    template: PrecisionTemplate,
) -> PhantomAffineNormalForm:
    """
    Normalize the pair ``(source, current + template_shift)`` exactly.
    """
    source = state.source
    phantom_constant = state.current.constant + template.numerator_shift
    phantom_coefficient = state.current.coefficient
    source_per_phantom = Fraction(
        source.coefficient,
        phantom_coefficient,
    )
    source_at_phantom_zero = (
        Fraction(source.constant)
        - source_per_phantom * phantom_constant
    )
    normal = PhantomAffineNormalForm(
        source_per_phantom,
        source_at_phantom_zero,
    )

    # Check both coefficients of
    # source = source_per_phantom * phantom + source_at_phantom_zero.
    assert (
        normal.source_per_phantom * phantom_coefficient
        == source.coefficient
    )
    assert (
        normal.source_per_phantom * phantom_constant
        + normal.source_at_phantom_zero
        == source.constant
    )
    return normal


def merge_signature(state: OrbitState) -> MergeSignature:
    """Build the most permissive merge signature justified by current lemmas."""
    template = last_precision_template(state.exact_exponents)
    if template is None:
        return UntracedMergeSignature(
            exact_word=state.exact_exponents,
            affine_relation=affine_relation(state),
        )

    phantom = Linear(
        state.current.constant + template.numerator_shift,
        state.current.coefficient,
    )
    return TracedMergeSignature(
        template=template,
        phantom_affine=phantom_affine_normal_form(state, template),
        valuation_profile=valuation_profile(phantom),
    )


def traced_signature_for(
    state: OrbitState,
    template: PrecisionTemplate,
) -> TracedMergeSignature:
    """Build the exact trace signature for one applicable template choice."""
    if template not in applicable_precision_templates(state.exact_exponents):
        raise ValueError("template is not a suffix of the exact word")
    phantom = Linear(
        state.current.constant + template.numerator_shift,
        state.current.coefficient,
    )
    return TracedMergeSignature(
        template=template,
        phantom_affine=phantom_affine_normal_form(state, template),
        valuation_profile=valuation_profile(phantom),
    )


def class_sizes(items: list[Hashable]) -> Counter[int]:
    """Histogram of quotient-class cardinalities."""
    classes: dict[Hashable, int] = Counter(items)
    return Counter(classes.values())


def _group_indices(items: list[Hashable]) -> dict[Hashable, list[int]]:
    groups: dict[Hashable, list[int]] = defaultdict(list)
    for index, item in enumerate(items):
        groups[item].append(index)
    return groups


def main() -> None:
    max_bits = 8
    max_steps = 4
    exploration = LazyA0Explorer(
        max_bits=max_bits,
        max_steps=max_steps,
    ).run()
    residual_states = [leaf.state for leaf in exploration.residual]

    assert len(residual_states) == 65
    assert all(leaf.reason == "step_cap" for leaf in exploration.residual)
    assert all(len(state.exact_exponents) == max_steps for state in residual_states)

    words = [state.exact_exponents for state in residual_states]
    templates = [last_precision_template(word) for word in words]
    affine_forms = [affine_relation(state) for state in residual_states]
    signatures = [merge_signature(state) for state in residual_states]

    traced_profiles = [
        signature.valuation_profile
        for signature in signatures
        if isinstance(signature, TracedMergeSignature)
    ]
    traced_signatures = [
        signature
        for signature in signatures
        if isinstance(signature, TracedMergeSignature)
    ]
    untraced_signatures = [
        signature
        for signature in signatures
        if isinstance(signature, UntracedMergeSignature)
    ]
    all_trace_assignments = [
        traced_signature_for(state, template)
        for state in residual_states
        for template in applicable_precision_templates(state.exact_exponents)
    ]
    assignments_by_template = {
        template.name: [
            signature
            for signature in all_trace_assignments
            if signature.template == template
        ]
        for template in (WORD_ONE, WORD_ONE_TWO, WORD_TWO_ONE)
    }

    template_counts = Counter(
        template.name if template is not None else "none"
        for template in templates
    )
    signature_groups = _group_indices(signatures)
    exact_class_count = len(signature_groups)
    reduction = len(residual_states) - exact_class_count

    # Fixed-run regression facts.  The tempting template-only quotient has
    # four labels, but each traced state has a distinct exact root/affine
    # obligation, while every untraced exact word is also distinct.
    assert len(set(words)) == 65
    assert len(set(affine_forms)) == 65
    assert template_counts == Counter(
        {"none": 25, "n+1": 20, "n+5": 10, "n+7": 10}
    )
    assert len(traced_profiles) == 40
    assert len(set(traced_profiles)) == 40
    assert len(traced_signatures) == 40
    assert len(set(traced_signatures)) == 40
    assert len(all_trace_assignments) == 50
    assert {
        name: (len(items), len(set(items)))
        for name, items in assignments_by_template.items()
    } == {"n+1": (30, 30), "n+5": (10, 10), "n+7": (10, 10)}
    assert len(untraced_signatures) == 25
    assert len(set(untraced_signatures)) == 25
    assert exact_class_count == 65
    assert reduction == 0
    assert class_sizes(signatures) == Counter({1: 65})

    print("a0_residual_exact_quotient=ok")
    print("integer_samples=0")
    print(f"max_bits={max_bits}")
    print(f"max_steps={max_steps}")
    print(f"residual_states={len(residual_states)}")
    print(f"distinct_exact_words={len(set(words))}")
    print(
        "last_template_counts="
        + ",".join(
            f"{name}:{template_counts[name]}"
            for name in ("none", "n+1", "n+5", "n+7")
        )
    )
    print(f"template_only_labels={len(template_counts)}")
    print(f"affine_relation_classes={len(set(affine_forms))}")
    print(f"traced_states={len(traced_signatures)}")
    print(f"all_applicable_trace_assignments={len(all_trace_assignments)}")
    print(
        "exact_trace_classes_by_template="
        + ",".join(
            f"{name}:{len(set(assignments_by_template[name]))}"
            f"/{len(assignments_by_template[name])}"
            for name in ("n+1", "n+5", "n+7")
        )
    )
    print(f"traced_pointwise_precision_profiles={len(set(traced_profiles))}")
    print(f"untraced_states={len(untraced_signatures)}")
    print(f"exact_merge_classes={exact_class_count}")
    print(f"largest_exact_merge_class={max(map(len, signature_groups.values()))}")
    print(f"frontier_reduction={reduction}/{len(residual_states)}")
    print("kill_criterion=NO_GO:no_exact_residual_merges")
    print(
        "reason=template labels compress only after discarding the "
        "source/phantom affine relation and the exact 2-adic root"
    )


if __name__ == "__main__":
    main()
