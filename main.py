import argparse
import json
from pathlib import Path
import wzpie
import wzstat


class NotFoundError(Exception):
    pass


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scale", type=int, required=True)
    parser.add_argument("--inputs", nargs="+", required=True)
    return parser.parse_args()


def main():
    args = parse_args()

    SCALE = int(args.scale)
    PREFIX = f'x{SCALE}_'

    # Process the input list
    finished_entries = set[wzstat.StatId]()

    # Collect all pie names (e.g. 'prltrk1.pie') before scaling.
    # Must be lowercase!
    pending_pie_names = set[str]()

    # Collect diffs
    diffs: dict[wzstat.StatFile, dict[wzstat.StatId, wzstat.StatItem]] = {
        'weapons.json': {},
        'body.json': {},
        'propulsion.json': {},
        'structure.json': {},
        'features.json': {}
    }

    # Scale the stat items
    while len(args.inputs) > 0:
        stat_id = args.inputs.pop(0)
        if stat_id in finished_entries:
            continue

        stat_item, stat_file = wzstat.lookup_stat_id(stat_id)

        new_stat_item, discovered_pie_names, discovered_stat_ids = wzstat.scale(stat_item, stat_file, PREFIX, SCALE)

        for pie_name in discovered_pie_names:
            pending_pie_names.add(pie_name)

        for stat_id in discovered_stat_ids:
            args.inputs.append(stat_id)

        # Collect diffs
        diffs[stat_file][stat_id] = new_stat_item

        # Mark stat item as complete
        finished_entries.add(stat_id)

    # Write the pies
    for pie_name in pending_pie_names:
        pie_data = wzpie.get(pie_name)
        if pie_data is None:
            raise NotFoundError(f"{pie_name} was not found!")

        old_path, old_text = ( pie_data['path'], pie_data['text'] )
        new_pie_text = wzpie.scale(old_text, SCALE)

        path = Path(__file__).parent / 'mod' / old_path / f'{PREFIX}{pie_name}'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(new_pie_text)
        print('Wrote', path)

    # Write the diffs
    for stat_file, diff in diffs.items():
        path = Path(__file__).parent / 'mod' / 'diffs' / f'{PREFIX}WZmodBig' / 'stats' / stat_file
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(diff))
        print('Wrote', path)


if __name__ == "__main__":
    main()
