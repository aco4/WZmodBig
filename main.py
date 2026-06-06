import argparse
import scale
import pie
import json
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scale", type=int, required=True)
    parser.add_argument("--inputs", required=False, default="[]")
    parser.add_argument("--weapons", nargs="+", required=False, default=[])
    parser.add_argument("--bodies", nargs="+", required=False, default=[])
    parser.add_argument("--propulsions", nargs="+", required=False, default=[])
    parser.add_argument("--structures", nargs="+", required=False, default=[])
    parser.add_argument("--features", nargs="+", required=False, default=[])
    return parser.parse_args()


def main():
    args = parse_args()

    SCALE = int(args.scale)
    PREFIX = f'x{SCALE}_'

    # Build the input list
    inputs: list[scale.InputEntry] = json.loads(args.inputs)
    for weapon in args.weapons:
        inputs.append({ 'id': weapon, 'stat_file': 'weapons.json' })
    for body in args.bodies:
        inputs.append({ 'id': body, 'stat_file': 'body.json' })
    for propulsion in args.propulsions:
        inputs.append({ 'id': propulsion, 'stat_file': 'propulsion.json' })
    for structure in args.structures:
        inputs.append({ 'id': structure, 'stat_file': 'structure.json' })
    for feature in args.features:
        inputs.append({ 'id': feature, 'stat_file': 'features.json' })

    # Process the input list
    pies, diffs = scale.process_inputs(inputs, SCALE, PREFIX)

    # Write the pies
    for pie_name in pies:
        pie_data = pie.get(pie_name)
        if pie_data is None:
            print(f'Error getting {pie_name}')
            continue;

        old_path, old_text = ( pie_data['path'], pie_data['text'] )
        new_pie_text = pie.scale(old_text, SCALE)

        path = Path(__file__).parent / 'mod' / old_path / f'{PREFIX}{pie_name}'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(new_pie_text)
        print('Wrote', path)

    # Write the diffs
    for stat, diff in diffs.items():
        path = Path(__file__).parent / 'mod' / 'diffs' / f'{PREFIX}WZmodBig' / 'stats' / stat
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(diff))
        print('Wrote', path)


if __name__ == "__main__":
    main()
