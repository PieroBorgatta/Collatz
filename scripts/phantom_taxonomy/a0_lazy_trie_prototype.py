#!/usr/bin/env python3
"""
Small fully symbolic lazy-trie prototype for the A0 endpoint.

The fixed source and post-prefix current value are

    source(t)  = 103 + 256*t
    current(t) = 593 + 1458*t.

At an odd affine current ``x(v)``, the next Syracuse exponent is obtained
from the affine numerator ``3*x(v) + 1``.  After removing the common power
of two from its coefficient, the remaining coefficient is odd, so
``symbolic_2adic_trie.OddAffine`` gives its unique valuation spine.

The prototype never enumerates values of ``t``.  An exact-valuation sibling
gets its exact Syracuse step; a root child keeps a lower bound on the
exponent.  If the corresponding upper affine endpoint is coefficientwise
below the source, the whole root cylinder closes at once.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from fractions import Fraction

from symbolic_2adic_trie import Cylinder, OddAffine, valuation_nonzero


@dataclass(frozen=True)
class Linear:
    """An integer affine form ``constant + coefficient*v``."""

    constant: int
    coefficient: int

    def __post_init__(self) -> None:
        if self.constant < 0 or self.coefficient < 0:
            raise ValueError("A0 prototype expects nonnegative affine forms")

    def restrict(self, cylinder: Cylinder) -> Linear:
        """Substitute ``v = residue + 2^bits*w``."""
        return Linear(
            self.constant + self.coefficient * cylinder.residue,
            self.coefficient * cylinder.modulus,
        )

    def syracuse_numerator(self) -> Linear:
        return Linear(3 * self.constant + 1, 3 * self.coefficient)

    def divide_power_of_two(self, exponent: int) -> Linear:
        divisor = 1 << exponent
        if self.constant % divisor or self.coefficient % divisor:
            raise ValueError("affine form is not uniformly divisible")
        return Linear(self.constant // divisor, self.coefficient // divisor)

    def coefficientwise_below(self, other: Linear) -> bool:
        """A strict sufficient inequality for every local parameter ``v >= 0``."""
        return (
            self.constant < other.constant
            and self.coefficient < other.coefficient
        )


@dataclass(frozen=True)
class OrbitState:
    """
    One exact A0 branch.

    If ``t = cylinder.residue + 2^cylinder.bits*v``, ``source`` and
    ``current`` are the corresponding affine forms in the local ``v``.
    """

    cylinder: Cylinder
    source: Linear
    current: Linear
    exact_exponents: tuple[int, ...] = ()

    def __post_init__(self) -> None:
        if self.current.constant % 2 != 1:
            raise ValueError("accelerated Syracuse state must be odd")
        if self.current.coefficient % 2 != 0:
            raise ValueError("current must stay odd on the whole cylinder")

    def restrict(self, local: Cylinder) -> OrbitState:
        """Refine the local parameter by one exact 2-adic cylinder."""
        global_cylinder = Cylinder(
            self.cylinder.residue
            + self.cylinder.modulus * local.residue,
            self.cylinder.bits + local.bits,
        )
        return OrbitState(
            global_cylinder,
            self.source.restrict(local),
            self.current.restrict(local),
            self.exact_exponents,
        )

    def step(self, exponent: int) -> OrbitState:
        """Apply one uniformly exact accelerated Syracuse step."""
        next_current = (
            self.current.syracuse_numerator().divide_power_of_two(exponent)
        )
        return OrbitState(
            self.cylinder,
            self.source,
            next_current,
            self.exact_exponents + (exponent,),
        )

    def step_upper_bound(self, exponent_lower_bound: int) -> Linear:
        """
        Divide by the known minimum power of two.

        The actual accelerated endpoint divides this affine form by a
        further power of two, so it is pointwise no larger.
        """
        return self.current.syracuse_numerator().divide_power_of_two(
            exponent_lower_bound
        )


@dataclass(frozen=True)
class ClosedLeaf:
    cylinder: Cylinder
    source: Linear
    endpoint_upper: Linear
    exact_prefix: tuple[int, ...]
    final_exponent_at_least: int | None
    reason: str

    @property
    def step_count(self) -> int:
        return len(self.exact_prefix) + (
            1 if self.final_exponent_at_least is not None else 0
        )


@dataclass(frozen=True)
class ResidualLeaf:
    state: OrbitState
    reason: str


@dataclass
class AuditStats:
    orbit_states: int = 0
    valuation_nodes: int = 0
    valuation_splits: int = 0
    exact_siblings: int = 0
    root_children: int = 0
    splits_by_global_bits: Counter[int] = field(default_factory=Counter)


@dataclass(frozen=True)
class Exploration:
    closed: tuple[ClosedLeaf, ...]
    residual: tuple[ResidualLeaf, ...]
    stats: AuditStats


class LazyA0Explorer:
    """Depth-bounded symbolic exploration of the exact A0 valuation trie."""

    def __init__(self, *, max_bits: int = 8, max_steps: int = 4) -> None:
        if max_bits < 5:
            raise ValueError("max_bits must expose the required mod-32 leaf")
        if max_steps < 2:
            raise ValueError("max_steps must expose the required two-step leaf")
        self.max_bits = max_bits
        self.max_steps = max_steps
        self.closed: list[ClosedLeaf] = []
        self.residual: list[ResidualLeaf] = []
        self.stats = AuditStats()

    def run(self) -> Exploration:
        initial = OrbitState(
            cylinder=Cylinder.all(),
            source=Linear(103, 256),
            current=Linear(593, 1458),
        )
        self._explore_orbit(initial)
        return Exploration(
            closed=tuple(self.closed),
            residual=tuple(self.residual),
            stats=self.stats,
        )

    def _close_exact_state(self, state: OrbitState) -> bool:
        if not state.current.coefficientwise_below(state.source):
            return False
        self.closed.append(
            ClosedLeaf(
                cylinder=state.cylinder,
                source=state.source,
                endpoint_upper=state.current,
                exact_prefix=state.exact_exponents,
                final_exponent_at_least=None,
                reason="exact_endpoint_coefficientwise_drop",
            )
        )
        return True

    def _explore_orbit(self, state: OrbitState) -> None:
        self.stats.orbit_states += 1
        if self._close_exact_state(state):
            return
        if len(state.exact_exponents) >= self.max_steps:
            self.residual.append(ResidualLeaf(state, "step_cap"))
            return

        numerator = state.current.syracuse_numerator()
        coefficient_v2 = valuation_nonzero(numerator.coefficient)
        constant_v2 = valuation_nonzero(numerator.constant)
        if constant_v2 < coefficient_v2:
            # Distinct valuations make the exponent uniform on this cylinder.
            self._explore_orbit(state.step(constant_v2))
            return

        common = coefficient_v2
        residual_form = OddAffine(
            numerator.constant >> common,
            numerator.coefficient >> common,
        )
        self._explore_valuation_spine(
            state,
            residual_form,
            common,
            Cylinder.all(),
        )

    def _explore_valuation_spine(
        self,
        parent_state: OrbitState,
        residual_form: OddAffine,
        common_exponent: int,
        local_root: Cylinder,
    ) -> None:
        self.stats.valuation_nodes += 1
        state = parent_state.restrict(local_root)
        exponent_lower_bound = common_exponent + local_root.bits
        endpoint_upper = state.step_upper_bound(exponent_lower_bound)

        # This closes the entire threshold cylinder, including every deeper
        # exact-valuation child, with one affine inequality.
        if endpoint_upper.coefficientwise_below(state.source):
            self.closed.append(
                ClosedLeaf(
                    cylinder=state.cylinder,
                    source=state.source,
                    endpoint_upper=endpoint_upper,
                    exact_prefix=state.exact_exponents,
                    final_exponent_at_least=exponent_lower_bound,
                    reason="threshold_endpoint_coefficientwise_drop",
                )
            )
            return

        if state.cylinder.bits >= self.max_bits:
            self.residual.append(ResidualLeaf(state, "precision_cap"))
            return

        split = residual_form.refine_root(local_root)
        self.stats.valuation_splits += 1
        self.stats.exact_siblings += 1
        self.stats.root_children += 1
        self.stats.splits_by_global_bits[state.cylinder.bits] += 1

        # The sibling has residual valuation exactly local_root.bits.
        exact_state = parent_state.restrict(split.exact_child)
        exact_exponent = common_exponent + split.exact_valuation
        self._explore_orbit(exact_state.step(exact_exponent))

        # Only this child can have a larger valuation.
        self._explore_valuation_spine(
            parent_state,
            residual_form,
            common_exponent,
            split.root_child,
        )


def normalized_slope(state: OrbitState) -> Fraction:
    """Coefficient with respect to the original global parameter ``t``."""
    return Fraction(state.current.coefficient, state.cylinder.modulus)


def frontier_measure(exploration: Exploration) -> Fraction:
    """Dyadic measure of the closed-plus-residual prefix-free frontier."""
    cylinders = [
        *(leaf.cylinder for leaf in exploration.closed),
        *(leaf.state.cylinder for leaf in exploration.residual),
    ]
    return sum(
        (Fraction(1, cylinder.modulus) for cylinder in cylinders),
        start=Fraction(0),
    )


def closed_measure(exploration: Exploration) -> Fraction:
    """Dyadic measure already certified to descend by this bounded run."""
    return sum(
        (Fraction(1, leaf.cylinder.modulus) for leaf in exploration.closed),
        start=Fraction(0),
    )


def residual_measure(exploration: Exploration) -> Fraction:
    """Dyadic measure left explicitly unresolved by the configured caps."""
    return sum(
        (
            Fraction(1, leaf.state.cylinder.modulus)
            for leaf in exploration.residual
        ),
        start=Fraction(0),
    )


def _assert_disjoint_frontier(exploration: Exploration) -> None:
    cylinders = [
        *(leaf.cylinder for leaf in exploration.closed),
        *(leaf.state.cylinder for leaf in exploration.residual),
    ]
    for index, left in enumerate(cylinders):
        for right in cylinders[index + 1 :]:
            assert left.intersection(right) is None


def _required_leaf(
    exploration: Exploration,
    cylinder: Cylinder,
) -> ClosedLeaf:
    matches = [leaf for leaf in exploration.closed if leaf.cylinder == cylinder]
    assert len(matches) == 1
    return matches[0]


def _self_test(exploration: Exploration) -> None:
    _assert_disjoint_frontier(exploration)
    assert frontier_measure(exploration) == 1
    assert closed_measure(exploration) + residual_measure(exploration) == 1
    assert exploration.closed
    assert exploration.residual
    assert all(
        leaf.endpoint_upper.coefficientwise_below(leaf.source)
        for leaf in exploration.closed
    )

    one_step = _required_leaf(exploration, Cylinder(2, 4))
    assert one_step.exact_prefix == ()
    assert one_step.final_exponent_at_least == 5
    assert one_step.step_count == 1
    assert one_step.source == Linear(615, 4096)
    assert one_step.endpoint_upper == Linear(329, 2187)

    two_steps = _required_leaf(exploration, Cylinder(10, 5))
    assert two_steps.exact_prefix == (4,)
    assert two_steps.final_exponent_at_least == 2
    assert two_steps.step_count == 2
    assert two_steps.source == Linear(2663, 8192)
    assert two_steps.endpoint_upper == Linear(2134, 6561)


def main() -> None:
    exploration = LazyA0Explorer(max_bits=8, max_steps=4).run()
    _self_test(exploration)

    closed_by_bits = Counter(leaf.cylinder.bits for leaf in exploration.closed)
    residual_by_bits = Counter(
        leaf.state.cylinder.bits for leaf in exploration.residual
    )
    max_residual_slope = max(
        (normalized_slope(leaf.state) for leaf in exploration.residual),
        default=Fraction(0),
    )
    initial_slope = Fraction(1458)

    print("a0_lazy_trie_self_test=ok")
    print("integer_samples=0")
    print(f"max_bits=8")
    print(f"max_steps=4")
    print(f"closed_leaves={len(exploration.closed)}")
    print(f"residual_leaves={len(exploration.residual)}")
    print(f"closed_dyadic_measure={closed_measure(exploration)}")
    print(f"residual_dyadic_measure={residual_measure(exploration)}")
    print(f"frontier_dyadic_measure={frontier_measure(exploration)}")
    print(f"orbit_states={exploration.stats.orbit_states}")
    print(f"valuation_nodes={exploration.stats.valuation_nodes}")
    print(f"valuation_splits={exploration.stats.valuation_splits}")
    print(f"closed_by_bits={dict(sorted(closed_by_bits.items()))}")
    print(f"residual_by_bits={dict(sorted(residual_by_bits.items()))}")
    print(
        "splits_by_bits="
        f"{dict(sorted(exploration.stats.splits_by_global_bits.items()))}"
    )
    print(
        "max_residual_global_slope="
        f"{max_residual_slope.numerator}/{max_residual_slope.denominator}"
    )
    growth = max_residual_slope / initial_slope
    print(
        "max_residual_slope_growth="
        f"{growth.numerator}/{growth.denominator}"
    )
    print("certified_t=2_mod_16:steps=1:last_exponent>=5")
    print("certified_t=10_mod_32:steps=2:word=4,last_exponent>=2")


if __name__ == "__main__":
    main()
