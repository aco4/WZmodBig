# WZmodBig
This Warzone 2100 mod adds big units and structures.

# Build
The build script is `main.py`.
## Example usage
```bash
python3 main.py --scale 2 --inputs tracked01 Body11ABT Cannon1Mk1 PillBox4
```
Spawn the big versions in-game with cheat `give all` or WZ JS API functions:
```js
addDroid(player, x, y, "P.1000 Ratte", "x2_Body11ABT", "x2_tracked01", "", "", "x2_Cannon1Mk1");
addStructure("x2_PillBox4", player, x, y);
```
By default, the mod will generate dedicated propulsions only for each input listed (e.g. `tracked01` ⟶ `x2_tracked01`). To allow normal propulsion to fit onto big bodies instead, pass `--vanillapropulsion`:
```bash
python3 main.py --scale 2 --inputs tracked01 Body11ABT Cannon1Mk1 PillBox4 --vanillapropulsion
```
Now works:
```js
addDroid(player, x, y, "P.1000 Ratte", "x2_Body11ABT", "tracked01", "", "", "x2_Cannon1Mk1");
```
To allow other propulsions to be compatible, include them:
```bash
python3 main.py --scale 2 --inputs wheeled01 HalfTrack tracked01 hover01 V-Tol Body11ABT Cannon1Mk1 PillBox4 --vanillapropulsion
```
To generate research entries and allow gameplay access, pass `--research`:
```bash
python3 main.py --scale 2 --inputs wheeled01 HalfTrack tracked01 hover01 V-Tol Body11ABT Cannon1Mk1 PillBox4 --vanillapropulsion --research
```
## Suggested usage
To scan a directory for inputs, use grep:
```bash
python3 main.py --scale 2 --inputs $(grep -rhoP 'x2_\K[^"]+' /path/to/directory/or/file)
```
To generate multiple sizes:
```bash
python3 main.py --x2_inputs $(grep -rhoP 'x2_\K[^"]+' /path/to/directory/or/file) \
                --x3_inputs $(grep -rhoP 'x3_\K[^"]+' /path/to/directory/or/file) \
                --x4_inputs $(grep -rhoP 'x4_\K[^"]+' /path/to/directory/or/file) \
                --x5_inputs $(grep -rhoP 'x5_\K[^"]+' /path/to/directory/or/file)
```

## License
SPDX-License-Identifier: GPL-2.0-or-later

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, see https://www.gnu.org/licenses/.
