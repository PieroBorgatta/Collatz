import csv
from collections import deque, defaultdict


ROOT = 8216025965

# Cerchiamo nodi piccoli sotto questo valore.
TARGET_LIMIT = 5_000_000

# Però per arrivarci, dobbiamo attraversare nodi intermedi molto grandi.
SEARCH_MAX_VALUE = ROOT

MAX_DEPTH = 200

INPUT_MEMBERS_FILE = "collatz_13_ingressi_autostrada.csv"
OUTPUT_TREE_FILE = "collatz_16_albero_inverso_tronco_CORRETTO.csv"
OUTPUT_MATCH_FILE = "collatz_16_match_membri_62_CORRETTO.csv"
SUMMARY_FILE = "collatz_16_summary_albero_inverso_CORRETTO.txt"


def read_expected_members(filename: str):
    members = set()

    with open(filename, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")

        for row in reader:
            members.add(int(row["start"]))

    return members


def v2(x: int) -> int:
    count = 0

    while x % 2 == 0:
        x //= 2
        count += 1

    return count


def syracuse(n: int):
    x = 3 * n + 1
    a = v2(x)
    return x >> a, a


def inverse_predecessors(m: int, search_max_value: int):
    """
    Trova predecessori dispari n tali che:

        S(n) = m

    cioè:

        (3n + 1) / 2^a = m

    quindi:

        n = (m * 2^a - 1) / 3

    ATTENZIONE:
    Non usiamo TARGET_LIMIT qui.
    Anche predecessori molto grandi possono poi scendere con altri passi inversi a=1.
    """
    preds = []

    if m % 3 == 0:
        return preds

    a = 1

    while True:
        numerator = m * (2 ** a) - 1

        if numerator % 3 == 0:
            n = numerator // 3

            if n > search_max_value:
                break

            if n > 0 and n % 2 == 1:
                preds.append((n, a))

        a += 1

        if a > 300:
            break

    return preds


def build_inverse_tree(root: int, search_max_value: int, max_depth: int):
    """
    BFS inversa dal root.
    Genera tutti i predecessori fino a SEARCH_MAX_VALUE.
    """
    queue = deque()
    queue.append((root, 0, None, None))

    seen = set()
    rows = []

    while queue:
        value, depth, parent, exponent_a = queue.popleft()

        if value in seen:
            continue

        seen.add(value)

        rows.append({
            "value": value,
            "depth": depth,
            "parent": parent,
            "a_to_parent": exponent_a,
            "within_target_limit": value <= TARGET_LIMIT,
            "within_search_limit": value <= search_max_value,
        })

        if depth >= max_depth:
            continue

        preds = inverse_predecessors(value, search_max_value)

        for pred, a in preds:
            if pred not in seen:
                queue.append((pred, depth + 1, value, a))

    return rows


def export_csv(filename: str, rows: list):
    if not rows:
        return

    fieldnames = list(rows[0].keys())

    with open(filename, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def export_summary(filename: str, lines: list):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def reconstruct_path(value, parent_by_value, a_by_value):
    """
    Ricostruisce il percorso value -> ROOT seguendo i parent.
    """
    path = []

    current = value

    while current is not None:
        path.append({
            "value": current,
            "a_to_parent": a_by_value.get(current),
            "parent": parent_by_value.get(current),
        })

        current = parent_by_value.get(current)

    return path


def main():
    expected_members = read_expected_members(INPUT_MEMBERS_FILE)

    print("Costruzione albero inverso del tronco comune - VERSIONE CORRETTA")
    print("-" * 120)
    print(f"Root: {ROOT}")
    print(f"Target limit: {TARGET_LIMIT}")
    print(f"Search max value: {SEARCH_MAX_VALUE}")
    print(f"Max depth: {MAX_DEPTH}")
    print(f"Membri attesi: {len(expected_members)}")
    print()

    tree_rows = build_inverse_tree(ROOT, SEARCH_MAX_VALUE, MAX_DEPTH)

    values = set(row["value"] for row in tree_rows)
    within_target_values = set(
        row["value"]
        for row in tree_rows
        if row["value"] <= TARGET_LIMIT
    )

    matched = expected_members & within_target_values
    missing = expected_members - within_target_values
    extra = within_target_values - expected_members

    depth_by_value = {row["value"]: row["depth"] for row in tree_rows}
    parent_by_value = {row["value"]: row["parent"] for row in tree_rows}
    a_by_value = {row["value"]: row["a_to_parent"] for row in tree_rows}

    match_rows = []

    for n in sorted(expected_members):
        found = n in within_target_values

        path = reconstruct_path(n, parent_by_value, a_by_value) if found else []
        path_values = " -> ".join(str(p["value"]) for p in path)
        path_a = ",".join(
            str(p["a_to_parent"])
            for p in path
            if p["a_to_parent"] is not None
        )

        # Verifica diretta: applicando Syracuse depth volte devo arrivare al root.
        check = n
        ok_forward = False

        if found:
            for _ in range(depth_by_value[n]):
                check, _ = syracuse(check)

            ok_forward = check == ROOT

        match_rows.append({
            "start": n,
            "found_in_inverse_tree": found,
            "depth_to_root": depth_by_value.get(n),
            "parent": parent_by_value.get(n),
            "a_to_parent": a_by_value.get(n),
            "forward_check_reaches_root": ok_forward,
            "path_a_sequence_to_root": path_a,
            "path_values_to_root": path_values,
        })

    export_csv(OUTPUT_TREE_FILE, tree_rows)
    export_csv(OUTPUT_MATCH_FILE, match_rows)

    depth_counts_all = defaultdict(int)
    depth_counts_target = defaultdict(int)

    for row in tree_rows:
        depth_counts_all[row["depth"]] += 1

        if row["value"] <= TARGET_LIMIT:
            depth_counts_target[row["depth"]] += 1

    lines = []
    lines.append("ALBERO INVERSO DEL TRONCO COMUNE - VERSIONE CORRETTA")
    lines.append("=" * 120)
    lines.append("")
    lines.append(f"Root: {ROOT}")
    lines.append(f"Target limit: {TARGET_LIMIT}")
    lines.append(f"Search max value: {SEARCH_MAX_VALUE}")
    lines.append(f"Max depth: {MAX_DEPTH}")
    lines.append("")
    lines.append(f"Nodi totali generati: {len(tree_rows)}")
    lines.append(f"Nodi <= target limit: {len(within_target_values)}")
    lines.append("")
    lines.append(f"Membri attesi: {len(expected_members)}")
    lines.append(f"Membri trovati: {len(matched)}")
    lines.append(f"Membri mancanti: {len(missing)}")
    lines.append(f"Nodi extra <= target limit: {len(extra)}")
    lines.append("")
    lines.append("Distribuzione nodi totali per profondità:")
    lines.append("-" * 120)

    for depth in sorted(depth_counts_all):
        lines.append(f"depth={depth:4d} | count={depth_counts_all[depth]}")

    lines.append("")
    lines.append("Distribuzione nodi <= target limit per profondità:")
    lines.append("-" * 120)

    for depth in sorted(depth_counts_target):
        lines.append(f"depth={depth:4d} | count={depth_counts_target[depth]}")

    lines.append("")
    lines.append("Membri mancanti:")
    lines.append(", ".join(map(str, sorted(missing))) if missing else "nessuno")

    lines.append("")
    lines.append("Extra entro target limit non nei 62 membri:")
    lines.append(", ".join(map(str, sorted(extra)[:500])) if extra else "nessuno")

    export_summary(SUMMARY_FILE, lines)

    print(f"Nodi totali generati: {len(tree_rows)}")
    print(f"Nodi <= target limit: {len(within_target_values)}")
    print(f"Membri trovati: {len(matched)}/{len(expected_members)}")
    print(f"Membri mancanti: {len(missing)}")
    print(f"Nodi extra <= target limit: {len(extra)}")

    print()
    print(f"CSV albero generato: {OUTPUT_TREE_FILE}")
    print(f"CSV match generato: {OUTPUT_MATCH_FILE}")
    print(f"Summary generato: {SUMMARY_FILE}")

    print()
    print("Per aprirli:")
    print(f"open '{OUTPUT_TREE_FILE}'")
    print(f"open '{OUTPUT_MATCH_FILE}'")
    print(f"open '{SUMMARY_FILE}'")


if __name__ == "__main__":
    main()
