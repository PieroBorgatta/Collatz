#!/usr/bin/env python3
"""
Minimal exact core for a lazy symbolic 2-adic trie.

The represented sets are cylinders

    u = residue (mod 2^bits)

and the represented functions are affine forms ``F + G*u`` with odd
``G``.  Such a form has one and only one root cylinder at every depth:

    v2(F + G*u) >= m
      iff
    u = -F*G^(-1) (mod 2^m).

No range of integer values is enumerated.  Refinement follows the unique
root child; its sibling is the whole branch of values whose valuation is
exactly the current depth.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterator


@dataclass(frozen=True)
class Cylinder:
    """The congruence class ``u = residue (mod 2^bits)``."""

    residue: int
    bits: int

    def __post_init__(self) -> None:
        if not isinstance(self.bits, int) or self.bits < 0:
            raise ValueError("bits must be a nonnegative integer")
        object.__setattr__(self, "residue", self.residue % self.modulus)

    @property
    def modulus(self) -> int:
        return 1 << self.bits

    @classmethod
    def all(cls) -> Cylinder:
        """The depth-zero cylinder containing every integer."""
        return cls(0, 0)

    def contains(self, value: int) -> bool:
        return value % self.modulus == self.residue

    def contains_cylinder(self, other: Cylinder) -> bool:
        """Return whether every point of ``other`` belongs to ``self``."""
        return (
            self.bits <= other.bits
            and other.residue % self.modulus == self.residue
        )

    def intersection(self, other: Cylinder) -> Cylinder | None:
        """
        Intersect two 2-adic cylinders.

        Two such cylinders are either disjoint or nested, so a nonempty
        intersection is simply the deeper one.
        """
        if self.bits <= other.bits:
            return other if self.contains(other.residue) else None
        return self if other.contains(self.residue) else None

    def children(self) -> tuple[Cylinder, Cylinder]:
        """Return the two depth-``bits + 1`` subcylinders."""
        return (
            Cylinder(self.residue, self.bits + 1),
            Cylinder(self.residue + self.modulus, self.bits + 1),
        )


class ThresholdState(Enum):
    """Exact status of a valuation threshold on a whole cylinder."""

    BELOW = "below"
    AT_LEAST = "at_least"
    UNRESOLVED = "unresolved"


@dataclass(frozen=True)
class ThresholdClassification:
    """Result of deciding ``v2(F + G*u) >= threshold`` on a cylinder."""

    state: ThresholdState
    query: Cylinder
    threshold: int
    root: Cylinder


@dataclass(frozen=True)
class RootRefinement:
    """
    One lazy split along the affine root spine.

    ``on_spine`` is the unique child where the valuation may increase.
    Every value in ``off_spine`` has valuation exactly ``parent.bits``.
    """

    parent: Cylinder
    on_spine: Cylinder
    off_spine: Cylinder

    @property
    def root_child(self) -> Cylinder:
        """The child where the valuation is at least ``parent.bits + 1``."""
        return self.on_spine

    @property
    def exact_child(self) -> Cylinder:
        """The sibling where the valuation is exactly ``parent.bits``."""
        return self.off_spine

    @property
    def exact_valuation(self) -> int:
        return self.parent.bits


@dataclass(frozen=True)
class ThresholdRefinement:
    """One lazy split of an unresolved threshold query."""

    split: RootRefinement
    on_state: ThresholdState
    off_state: ThresholdState


@dataclass(frozen=True)
class CylinderRestriction:
    """
    An affine form in the local coordinate ``u = r + 2^k*v``.

    If ``fixed_valuation`` is set, the whole cylinder has that exact
    valuation.  Otherwise

        original(r + 2^k*v) = 2^k * residual(v),

    where ``residual`` is again an ``OddAffine`` form.
    """

    cylinder: Cylinder
    original: OddAffine
    offset: int
    step: int
    fixed_valuation: int | None
    residual: OddAffine | None

    def local_to_global(self, v: int) -> int:
        return self.cylinder.residue + self.cylinder.modulus * v

    def value(self, v: int) -> int:
        """Evaluate the original form through the local coordinate."""
        return self.offset + self.step * v

    @property
    def follows_root(self) -> bool:
        return self.residual is not None


@dataclass(frozen=True)
class OddAffine:
    """An integer affine form ``constant + coefficient*u``, coefficient odd."""

    constant: int
    coefficient: int

    def __post_init__(self) -> None:
        if self.coefficient % 2 == 0:
            raise ValueError("coefficient must be odd")

    def value(self, u: int) -> int:
        return self.constant + self.coefficient * u

    def root_cylinder(self, bits: int) -> Cylinder:
        """Return the unique cylinder where the form vanishes modulo ``2^bits``."""
        if not isinstance(bits, int) or bits < 0:
            raise ValueError("bits must be a nonnegative integer")
        if bits == 0:
            return Cylinder.all()
        modulus = 1 << bits
        inverse = pow(self.coefficient, -1, modulus)
        return Cylinder(-self.constant * inverse, bits)

    def root_spine(self, start_bits: int = 0) -> Iterator[Cylinder]:
        """Yield the nested root cylinders lazily, starting at ``start_bits``."""
        bits = start_bits
        while True:
            yield self.root_cylinder(bits)
            bits += 1

    def reparameterize(self, cylinder: Cylinder) -> CylinderRestriction:
        """
        Substitute ``u = residue + 2^bits*v`` exactly.

        On a root-spine cylinder the known factor ``2^bits`` is removed,
        exposing another odd affine form in ``v``.  Off the spine, the
        valuation is already uniform and is returned as ``fixed_valuation``.
        """
        offset = self.value(cylinder.residue)
        step = cylinder.modulus * self.coefficient
        if offset != 0 and valuation_nonzero(offset) < cylinder.bits:
            return CylinderRestriction(
                cylinder=cylinder,
                original=self,
                offset=offset,
                step=step,
                fixed_valuation=valuation_nonzero(offset),
                residual=None,
            )
        divisor = cylinder.modulus
        assert offset % divisor == 0
        return CylinderRestriction(
            cylinder=cylinder,
            original=self,
            offset=offset,
            step=step,
            fixed_valuation=None,
            residual=OddAffine(offset // divisor, self.coefficient),
        )

    def refine_root(self, parent: Cylinder) -> RootRefinement:
        """
        Refine one node already known to lie on the root spine.

        The returned sibling is exactly the cylinder on which the form has
        valuation ``parent.bits``.
        """
        if parent != self.root_cylinder(parent.bits):
            raise ValueError("parent is not on this affine root spine")
        on_spine = self.root_cylinder(parent.bits + 1)
        first, second = parent.children()
        off_spine = second if on_spine == first else first
        return RootRefinement(parent, on_spine, off_spine)

    def exact_valuation_cylinder(self, valuation: int) -> Cylinder:
        """Return the single cylinder where the form has valuation exactly ``valuation``."""
        if not isinstance(valuation, int) or valuation < 0:
            raise ValueError("valuation must be a nonnegative integer")
        return self.refine_root(self.root_cylinder(valuation)).off_spine

    def classify_threshold(
        self,
        query: Cylinder,
        threshold: int,
    ) -> ThresholdClassification:
        """
        Classify ``v2(form) >= threshold`` uniformly on ``query``.

        ``UNRESOLVED`` means that the threshold root is a strict subcylinder
        of ``query``.  It can be handled by ``refine_threshold`` without
        enumerating any representatives.
        """
        root = self.root_cylinder(threshold)
        overlap = query.intersection(root)
        if overlap is None:
            state = ThresholdState.BELOW
        elif root.contains_cylinder(query):
            state = ThresholdState.AT_LEAST
        else:
            state = ThresholdState.UNRESOLVED
        return ThresholdClassification(state, query, threshold, root)

    def refine_threshold(
        self,
        query: Cylinder,
        threshold: int,
    ) -> ThresholdRefinement:
        """Split one unresolved threshold query by one bit."""
        classification = self.classify_threshold(query, threshold)
        if classification.state is not ThresholdState.UNRESOLVED:
            raise ValueError("threshold is already decided on this cylinder")
        split = self.refine_root(query)
        on_state = self.classify_threshold(
            split.on_spine,
            threshold,
        ).state
        off_state = self.classify_threshold(
            split.off_spine,
            threshold,
        ).state
        return ThresholdRefinement(split, on_state, off_state)


def valuation_nonzero(value: int) -> int:
    """Return ``v2(value)``; reject zero, whose 2-adic valuation is infinite."""
    if value == 0:
        raise ValueError("zero has infinite 2-adic valuation")
    value = abs(value)
    return (value & -value).bit_length() - 1


def _self_test() -> None:
    # Cylinder normalization, nesting, disjointness, and exact intersection.
    assert Cylinder(-1, 3) == Cylinder(7, 3)
    assert Cylinder.all().intersection(Cylinder(5, 3)) == Cylinder(5, 3)
    assert Cylinder(1, 2).intersection(Cylinder(5, 3)) == Cylinder(5, 3)
    assert Cylinder(1, 2).intersection(Cylinder(3, 3)) is None
    assert Cylinder(1, 2).children() == (Cylinder(1, 3), Cylinder(5, 3))

    # The three root congruences used in the Phase 11 note.
    source = OddAffine(50, 1163)
    baseline = OddAffine(4, 93)
    competitor = OddAffine(14397, 334833)
    assert source.root_cylinder(2) == Cylinder(2, 2)
    assert source.root_cylinder(6) == Cylinder(42, 6)
    assert baseline.root_cylinder(5) == Cylinder(12, 5)
    assert competitor.root_cylinder(19) == Cylinder(287475, 19)

    # Roots are nested; their sibling records one exact valuation level.
    spine = source.root_spine()
    roots = [next(spine) for _ in range(7)]
    assert all(
        roots[bits].contains_cylinder(roots[bits + 1])
        for bits in range(6)
    )
    assert source.exact_valuation_cylinder(3) == Cylinder(2, 4)
    exact_three = source.exact_valuation_cylinder(3)
    assert valuation_nonzero(source.value(exact_three.residue)) == 3

    # Exact local coordinate: u = 2 + 4*v on the depth-two root.
    root_restriction = source.reparameterize(Cylinder(2, 2))
    assert root_restriction.follows_root
    assert root_restriction.fixed_valuation is None
    assert root_restriction.residual == OddAffine(594, 1163)
    assert root_restriction.value(7) == source.value(
        root_restriction.local_to_global(7)
    )
    assert root_restriction.value(7) == 4 * root_restriction.residual.value(7)

    # Off the root spine, substitution closes the whole branch immediately.
    off_restriction = source.reparameterize(Cylinder(1, 2))
    assert not off_restriction.follows_root
    assert off_restriction.fixed_valuation == 0
    assert off_restriction.residual is None

    # A threshold is refined only on the root child.  Every sibling closes.
    query = Cylinder.all()
    for expected_depth in range(1, 4):
        decision = source.classify_threshold(query, 3)
        assert decision.state is ThresholdState.UNRESOLVED
        refinement = source.refine_threshold(query, 3)
        assert refinement.off_state is ThresholdState.BELOW
        assert refinement.split.on_spine.bits == expected_depth
        assert refinement.split.root_child == refinement.split.on_spine
        assert refinement.split.exact_child == refinement.split.off_spine
        assert refinement.split.exact_valuation == expected_depth - 1
        query = refinement.split.on_spine
    assert source.classify_threshold(query, 3).state is ThresholdState.AT_LEAST

    # Competing Phase 11 cylinders are symbolically disjoint.
    source_shadow = OddAffine(20027, 465905).root_cylinder(2)
    destination_k16 = competitor.root_cylinder(3)
    assert source_shadow == Cylinder(1, 2)
    assert destination_k16 == Cylinder(3, 3)
    assert source_shadow.intersection(destination_k16) is None

    # An integral 2-adic root remains on every threshold spine.
    integral_root = OddAffine(-1, 1)
    assert all(integral_root.root_cylinder(bits).contains(1) for bits in range(8))
    try:
        valuation_nonzero(integral_root.value(1))
    except ValueError:
        pass
    else:
        raise AssertionError("zero must be treated as infinite valuation")

    print("symbolic_2adic_trie_self_test=ok")
    print("phase11_root_congruences=4")
    print("integer_ranges_enumerated=0")


if __name__ == "__main__":
    _self_test()
