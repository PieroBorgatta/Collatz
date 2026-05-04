"""
58_escape_certificate.py

Certificato finite-state del rientro post-shadowing.

Per un fantasma w e una profondita' b, tutti gli interi

    n0(t) = r + 2^M t,     M = bA + 1,     r = q mod 2^M,

seguono b periodi del fantasma. Dopo lo shadowing l'orbita e' ancora affine:

    y0(t) = U + V t.

Questo script non campiona t. Costruisce invece una partizione delle classi
residue di t. Su una classe

    t = offset + stride * x,     x >= 0,

mantiene un'affine

    y(x) = U + V x

e prova una delle due cose:

1. certificazione di rientro:

       y(x) < n0(offset + stride*x)  per ogni x >= 0;

2. altrimenti, se la prossima valutazione v2(3y+1) e' costante sulla classe,
   applica un passo Syracuse simbolico;

3. se la valutazione non e' costante, spezza la classe in due sottoclassi
   x = 0 mod 2 e x = 1 mod 2.

Se tutte le foglie vengono certificate, abbiamo un certificato finite-state:
la famiglia infinita parametrizzata da t torna sotto il proprio valore iniziale.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from importlib import util
from pathlib import Path


def load_module(filename: str, name: str):
    path = Path(__file__).with_name(filename)
    spec = util.spec_from_file_location(name, path)
    module = util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def v2_int(n: int) -> int:
    if n == 0:
        return 10**18
    n = abs(n)
    a = 0
    while (n & 1) == 0:
        n >>= 1
        a += 1
    return a


@dataclass
class Node:
    offset: int
    stride: int
    U: int
    V: int
    steps: int
    depth: int


def certify_below_start(node: Node, residue: int, modulus: int) -> bool:
    """True se U+Vx < residue + modulus*(offset+stride*x) per ogni x >= 0."""
    start_U = residue + modulus * node.offset
    start_V = modulus * node.stride
    if node.V > start_V:
        return False
    return node.U < start_U


def tail_threshold(node: Node, residue: int, modulus: int) -> int | None:
    """
    Se la differenza y(x)-n0(x) ha pendenza negativa, ritorna il numero T
    tale che tutti gli x >= T sono gia' certificati. Gli x < T restano
    eccezioni finite.
    """
    start_U = residue + modulus * node.offset
    start_V = modulus * node.stride
    dU = node.U - start_U
    dV = node.V - start_V
    if dV >= 0:
        return None
    if dU < 0:
        return 0
    return dU // (-dV) + 1


def direct_stop_below(current: int, start: int, max_steps: int) -> bool:
    cur = current
    for _ in range(max_steps):
        a = v2_int(3 * cur + 1)
        cur = (3 * cur + 1) >> a
        if cur < start:
            return True
    return False


def certify_tail_with_finite_exceptions(
    node: Node,
    residue: int,
    modulus: int,
    max_steps: int,
    max_finite_checks: int,
) -> tuple[bool, int]:
    """
    Certifica una classe se ha coda affine sotto n0 e solo poche eccezioni
    finite, controllate direttamente.
    """
    threshold = tail_threshold(node, residue, modulus)
    if threshold is None:
        return False, 0
    if threshold == 0:
        return True, 0
    if threshold > max_finite_checks:
        return False, threshold

    start_U = residue + modulus * node.offset
    start_V = modulus * node.stride
    remaining = max(0, max_steps - node.steps)
    for x in range(threshold):
        current = node.U + node.V * x
        start = start_U + start_V * x
        if current < start:
            continue
        if not direct_stop_below(current, start, remaining):
            return False, threshold
    return True, threshold


def valuation_constant_on_node(node: Node) -> tuple[bool, int]:
    """
    Per y(x)=U+Vx, F(x)=3y+1.
    v2(F(x)) e' costante su tutti x se la perturbazione 3Vx e' divisibile
    da una potenza di 2 strettamente maggiore di v2(F(0)).
    """
    a = v2_int(3 * node.U + 1)
    return v2_int(3 * node.V) > a, a


def symbolic_step(node: Node, a: int) -> Node:
    denom = 1 << a
    new_U = (3 * node.U + 1) // denom
    new_V = (3 * node.V) // denom
    return Node(
        offset=node.offset,
        stride=node.stride,
        U=new_U,
        V=new_V,
        steps=node.steps + 1,
        depth=node.depth,
    )


def split_node(node: Node) -> tuple[Node, Node]:
    """Spezza x in 2x' e 2x'+1, aggiornando t offset/stride e affine y."""
    even = Node(
        offset=node.offset,
        stride=node.stride * 2,
        U=node.U,
        V=node.V * 2,
        steps=node.steps,
        depth=node.depth + 1,
    )
    odd = Node(
        offset=node.offset + node.stride,
        stride=node.stride * 2,
        U=node.U + node.V,
        V=node.V * 2,
        steps=node.steps,
        depth=node.depth + 1,
    )
    return even, odd


def after_shadow_affine(record: dict, b: int) -> tuple[int, int, int, int]:
    """
    Ritorna (residue, modulus, U, V), dove:
      n0(t) = residue + modulus*t
      after_shadow(t) = U + V*t
    """
    shadowing = load_module("55_shadowing_congruence.py", "shadowing")
    shadows = load_module("54_phantom_rational_shadows.py", "phantom_shadows")

    q = record["q"]
    period_bits = record["sum_a"]
    period_len = record["length"]
    modulus_bits = b * period_bits + 1
    modulus = 1 << modulus_bits
    residue = shadows.rational_mod_power_of_two(q, modulus_bits)
    if residue == 0:
        residue = modulus

    U = shadowing.iterate_odd(residue, b * period_len)
    V = 2 * (3 ** (b * period_len))
    return residue, modulus, U, V


def certify_family(
    record: dict,
    b: int,
    max_steps: int,
    max_depth: int,
    max_nodes: int,
    max_finite_checks: int,
) -> dict:
    residue, modulus, U, V = after_shadow_affine(record, b)
    stack = [Node(offset=0, stride=1, U=U, V=V, steps=0, depth=0)]

    processed = 0
    certified = 0
    split_count = 0
    symbolic_count = 0
    finite_checks = 0
    tail_certified = 0
    max_tail_threshold = 0
    unresolved = []
    max_seen_steps = 0
    max_seen_depth = 0
    max_leaf_stride_bits = 0

    while stack:
        node = stack.pop()
        processed += 1
        if processed > max_nodes:
            unresolved.append(("max_nodes", node))
            break

        max_seen_steps = max(max_seen_steps, node.steps)
        max_seen_depth = max(max_seen_depth, node.depth)

        if certify_below_start(node, residue, modulus):
            certified += 1
            max_leaf_stride_bits = max(max_leaf_stride_bits, node.stride.bit_length() - 1)
            continue

        tail_ok, checked = certify_tail_with_finite_exceptions(
            node,
            residue,
            modulus,
            max_steps,
            max_finite_checks,
        )
        if tail_ok:
            certified += 1
            tail_certified += 1
            finite_checks += checked
            max_tail_threshold = max(max_tail_threshold, checked)
            max_leaf_stride_bits = max(max_leaf_stride_bits, node.stride.bit_length() - 1)
            continue
        max_tail_threshold = max(max_tail_threshold, checked)

        if node.steps >= max_steps:
            unresolved.append(("max_steps", node))
            continue

        constant, a = valuation_constant_on_node(node)
        if constant:
            symbolic_count += 1
            stack.append(symbolic_step(node, a))
            continue

        if node.depth >= max_depth:
            unresolved.append(("max_depth", node))
            continue

        split_count += 1
        even, odd = split_node(node)
        stack.append(odd)
        stack.append(even)

    return {
        "k": record["k"],
        "cycle_id": record["cycle_id"],
        "b": b,
        "period_len": record["length"],
        "period_bits": record["sum_a"],
        "period_product": record["product"],
        "modulus_bits": b * record["sum_a"] + 1,
        "certified_all": int(not unresolved),
        "processed_nodes": processed,
        "certified_leaves": certified,
        "unresolved_count": len(unresolved),
        "split_count": split_count,
        "symbolic_steps": symbolic_count,
        "tail_certified": tail_certified,
        "finite_checks": finite_checks,
        "max_tail_threshold": max_tail_threshold,
        "max_seen_steps": max_seen_steps,
        "max_seen_depth": max_seen_depth,
        "max_leaf_stride_bits": max_leaf_stride_bits,
        "first_unresolved_reason": unresolved[0][0] if unresolved else "",
    }


def write_csv(rows: list[dict], path: str) -> None:
    if not rows:
        return
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def print_rows(rows: list[dict]) -> None:
    print("\n" + "=" * 118)
    print("  FINITE-STATE ESCAPE CERTIFICATE")
    print("=" * 118)
    print(f"  {'k':>3} {'id':>3} {'b':>2} {'M':>5} {'ok':>3} {'nodes':>8} "
          f"{'leaves':>8} {'splits':>8} {'sym':>8} {'tail':>7} "
          f"{'checks':>8} {'steps':>6} {'depth':>6} {'stride2':>7} {'unres':>6}")
    for row in rows:
        print(f"  {row['k']:>3} {row['cycle_id']:>3} {row['b']:>2} "
              f"{row['modulus_bits']:>5} {row['certified_all']:>3} "
              f"{row['processed_nodes']:>8} {row['certified_leaves']:>8} "
              f"{row['split_count']:>8} {row['symbolic_steps']:>8} "
              f"{row['tail_certified']:>7} {row['finite_checks']:>8} "
              f"{row['max_seen_steps']:>6} {row['max_seen_depth']:>6} "
              f"{row['max_leaf_stride_bits']:>7} {row['unresolved_count']:>6}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Certifica finite-state il rientro sotto n0 per famiglie phantom."
    )
    parser.add_argument("--k-min", type=int, default=10)
    parser.add_argument("--k-max", type=int, default=24)
    parser.add_argument("--b-min", type=int, default=1)
    parser.add_argument("--b-max", type=int, default=8)
    parser.add_argument("--max-steps", type=int, default=1000)
    parser.add_argument("--max-depth", type=int, default=24)
    parser.add_argument("--max-nodes", type=int, default=2_000_000)
    parser.add_argument("--max-finite-checks", type=int, default=20_000)
    parser.add_argument("--only-k", type=int, default=None)
    parser.add_argument("--only-cycle", type=int, default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    shadowing = load_module("55_shadowing_congruence.py", "shadowing")
    records = shadowing.phantom_records(args.k_min, args.k_max)
    if args.only_k is not None:
        records = [r for r in records if r["k"] == args.only_k]
    if args.only_cycle is not None:
        records = [r for r in records if r["cycle_id"] == args.only_cycle]

    print("=" * 118)
    print("  Certificato finite-state di uscita dai fantasmi")
    print("=" * 118)
    print(f"  k range: {args.k_min}..{args.k_max}")
    print(f"  b range: {args.b_min}..{args.b_max}")
    print(f"  max steps={args.max_steps}, max depth={args.max_depth}, "
          f"max nodes={args.max_nodes}, max finite checks={args.max_finite_checks}")
    if args.only_k is not None or args.only_cycle is not None:
        print(f"  filters: only_k={args.only_k}, only_cycle={args.only_cycle}")

    rows = []
    for record in records:
        print(f"  Record k={record['k']} id={record['cycle_id']} "
              f"L={record['length']} A={record['sum_a']}")
        for b in range(args.b_min, args.b_max + 1):
            rows.append(
                certify_family(
                    record,
                    b,
                    max_steps=args.max_steps,
                    max_depth=args.max_depth,
                    max_nodes=args.max_nodes,
                    max_finite_checks=args.max_finite_checks,
                )
            )

    out_path = "collatz_58_escape_certificate.csv"
    write_csv(rows, out_path)
    print_rows(rows)
    print(f"\n  Certificati: {out_path}")


if __name__ == "__main__":
    main()
