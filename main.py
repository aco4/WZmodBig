import argparse
import json
from pathlib import Path
import wzpie
import wzstat
from collections.abc import Iterable
from typing import TypedDict


class Job(TypedDict):
    scale: str
    prefix: str
    inputs: list[str]
    recurse_on: list[str]

class NotFoundError(Exception):
    pass


def write_pies(pie_names: Iterable[str], prefix: str, scale: int):
    for pie_name in pie_names:
        pie_name = pie_name.lower()
        pie_data = wzpie.get(pie_name)
        if pie_data is None:
            raise NotFoundError(f"{pie_name} was not found!")

        old_path, old_text = ( pie_data['path'], pie_data['text'] )
        new_pie_text = wzpie.scale(old_text, scale)

        path = Path(__file__).parent / 'mod' / old_path / f'{prefix}{pie_name}'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(new_pie_text)
        print('Wrote', path)

def write_diffs(diffs: wzstat.Diffs, prefix: str):
    for stat_file, diff in diffs.items():
        path = Path(__file__).parent / 'mod' / 'diffs' / f'{prefix}WZmodBig' / 'stats' / stat_file
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(diff))
        print('Wrote', path)

def write(pie_names: Iterable[str], diffs: wzstat.Diffs, prefix: str, scale: int):
    write_pies(pie_names, prefix, scale)
    write_diffs(diffs, prefix)

def prefix(scale: int):
    return f'x{scale}_'

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scale", type=int, required=False)
    parser.add_argument("--inputs", nargs='+', required=False, default=[])
    parser.add_argument("--vanillapropulsion", action='store_true')
    parser.add_argument("--x2_inputs", nargs='+', required=False, default=[])
    parser.add_argument("--x3_inputs", nargs='+', required=False, default=[])
    parser.add_argument("--x4_inputs", nargs='+', required=False, default=[])
    parser.add_argument("--x5_inputs", nargs='+', required=False, default=[])
    return parser.parse_args()

def main():
    args = parse_args()

    if args.inputs:
        pies, diffs = wzstat.scale_all(args.inputs, prefix(args.scale), args.scale, vanilla_propulsion=args.vanillapropulsion)
        write(pies, diffs, prefix(args.scale), args.scale)
    else:
        if args.x2_inputs:
            pies, diffs = wzstat.scale_all(args.x2_inputs, prefix(2), 2, vanilla_propulsion=args.vanillapropulsion)
            write(pies, diffs, prefix(2), 2)

        if args.x3_inputs:
            pies, diffs = wzstat.scale_all(args.x3_inputs, prefix(3), 3, vanilla_propulsion=args.vanillapropulsion)
            write(pies, diffs, prefix(3), 3)

        if args.x4_inputs:
            pies, diffs = wzstat.scale_all(args.x4_inputs, prefix(4), 4, vanilla_propulsion=args.vanillapropulsion)
            write(pies, diffs, prefix(4), 4)

        if args.x5_inputs:
            pies, diffs = wzstat.scale_all(args.x5_inputs, prefix(5), 5, vanilla_propulsion=args.vanillapropulsion)
            write(pies, diffs, prefix(5), 5)


if __name__ == "__main__":
    main()
