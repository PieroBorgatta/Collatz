import csv
from collections import defaultdict


INPUT_GROUPS_FILE = "collatz_11_confluenze_alte.csv"

OUTPUT_ENTRY_FILE = "collatz_13_ingressi_autostrada.csv"
OUTPUT_TRUNK_FILE = "collatz_13_tronco_comune.csv"
OUTPUT_SUMMARY_FILE = "collatz_13_summary_autostrada.txt"

MAX_STEPS = 20_000


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


def read_first_group(filename: str):
    with open(filename, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        first = next(reader)

    members = [int(x) for x in first["members"].split(",") if x.strip()]

    return {
        "common_value": int(first["common_value"]),
        "members_count": int(first["members_count"]),
        "members": sorted(members),
    }


def build_trajectory_list(start: int, max_steps: int = MAX_STEPS):
    """
    Lista di dizionari:
    step, value, v2_from_previous
    """
    n = start
    trajectory = [{
        "step": 0,
        "value": n,
        "v2_from_previous": 0,
    }]

    for step in range(1, max_steps + 1):
        n, a = syracuse(n)

        trajectory.append({
            "step": step,
            "value": n,
            "v2_from_previous": a,
        })

        if n == 1:
            break

    return trajectory


def trajectory_value_to_step(trajectory):
    d = {}

    for row in trajectory:
        value = row["value"]
        if value not in d:
            d[value] = row["step"]

    return d


def find_common_values(trajectories):
    sets = []

    for traj in trajectories.values():
        sets.append(set(row["value"] for row in traj))

    common = set.intersection(*sets)

    return common


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


def main():
    group = read_first_group(INPUT_GROUPS_FILE)

    members = group["members"]

    print("Analisi autostrada gravitazionale comune")
    print("-" * 120)
    print(f"Valore comune iniziale dal file: {group['common_value']}")
    print(f"Membri del gruppo: {len(members)}")
    print()

    trajectories = {}

    for i, n in enumerate(members, start=1):
        trajectories[n] = build_trajectory_list(n)

        if i % 10 == 0:
            print(f"Traiettorie costruite: {i}/{len(members)}")

    common_values = find_common_values(trajectories)

    # escludiamo 1? No, ma cerchiamo anche il massimo valore comune.
    max_common_value = max(common_values)
    min_common_value = min(common_values)

    print()
    print(f"Valori comuni a tutti i {len(members)} membri: {len(common_values)}")
    print(f"Massimo valore comune: {max_common_value}")
    print(f"Minimo valore comune: {min_common_value}")

    # Il tronco comune inizia dal massimo valore comune condiviso da tutti.
    trunk_start = max_common_value

    # Prendiamo una traiettoria qualsiasi e tagliamola dal trunk_start fino a 1.
    sample_start = members[0]
    sample_traj = trajectories[sample_start]

    trunk_rows = []
    inside_trunk = False

    for row in sample_traj:
        if row["value"] == trunk_start:
            inside_trunk = True

        if inside_trunk:
            trunk_rows.append({
                "trunk_step": len(trunk_rows),
                "value": row["value"],
                "v2_from_previous": row["v2_from_previous"],
            })

    # Per ogni membro: quando entra nel tronco?
    entry_rows = []

    for n in members:
        traj = trajectories[n]
        value_to_step = trajectory_value_to_step(traj)

        entry_step = value_to_step[trunk_start]

        # valore massimo prima di entrare nel tronco
        pre_entry_values = [
            row["value"]
            for row in traj
            if row["step"] <= entry_step
        ]

        entry_rows.append({
            "start": n,
            "entry_value": trunk_start,
            "entry_step": entry_step,
            "max_before_entry": max(pre_entry_values),
            "ratio_max_before_entry": max(pre_entry_values) / n,
            "total_steps_to_1": traj[-1]["step"],
            "steps_from_entry_to_1": traj[-1]["step"] - entry_step,
            "start_mod_1024": n % 1024,
            "start_mod_4096": n % 4096,
            "start_mod_65536": n % 65536,
        })

    entry_rows.sort(key=lambda x: x["entry_step"])

    export_csv(OUTPUT_ENTRY_FILE, entry_rows)
    export_csv(OUTPUT_TRUNK_FILE, trunk_rows)

    lines = []
    lines.append("AUTOSTRADA GRAVITAZIONALE COMUNE")
    lines.append("=" * 120)
    lines.append("")
    lines.append(f"Membri analizzati: {len(members)}")
    lines.append(f"Valori comuni a tutti i membri: {len(common_values)}")
    lines.append(f"Tronco comune scelto dal massimo valore comune: {trunk_start}")
    lines.append(f"Lunghezza tronco comune fino a 1: {len(trunk_rows) - 1} salti Syracuse")
    lines.append("")
    lines.append("Membri:")
    lines.append(", ".join(map(str, members)))
    lines.append("")
    lines.append("Primi 40 valori del tronco:")
    for row in trunk_rows[:40]:
        lines.append(
            f"trunk_step={row['trunk_step']:4d} | "
            f"value={row['value']:20d} | "
            f"v2={row['v2_from_previous']}"
        )

    export_summary(OUTPUT_SUMMARY_FILE, lines)

    print()
    print(f"CSV ingressi generato: {OUTPUT_ENTRY_FILE}")
    print(f"CSV tronco comune generato: {OUTPUT_TRUNK_FILE}")
    print(f"Summary generato: {OUTPUT_SUMMARY_FILE}")

    print()
    print("Top ingressi più precoci:")
    print("-" * 120)

    for row in entry_rows[:20]:
        print(
            f"n={row['start']:10d} | "
            f"entry_step={row['entry_step']:4d} | "
            f"max_ratio={row['ratio_max_before_entry']:12.3f} | "
            f"total_steps={row['total_steps_to_1']:4d} | "
            f"mod1024={row['start_mod_1024']:4d}"
        )

    print()
    print("Per aprirli:")
    print(f"open '{OUTPUT_ENTRY_FILE}'")
    print(f"open '{OUTPUT_TRUNK_FILE}'")
    print(f"open '{OUTPUT_SUMMARY_FILE}'")


if __name__ == "__main__":
    main()
