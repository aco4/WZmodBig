# WZmodBig
This Warzone 2100 mod adds big units and structures.

# Build
```bash
python3 main.py --scale 2 --inputs tracked01 Body11ABT Cannon4AUTOMk1 PillBox4
```
or
```bash
python3 main.py --scale 2 --inputs $(grep -oP 'x2_\K[^"]+' TEMPLATES.js | sort -u)
python3 main.py --scale 3 --inputs $(grep -oP 'x3_\K[^"]+' TEMPLATES.js | sort -u)
python3 main.py --scale 4 --inputs $(grep -oP 'x4_\K[^"]+' TEMPLATES.js | sort -u)
python3 main.py --scale 5 --inputs $(grep -oP 'x5_\K[^"]+' TEMPLATES.js | sort -u)
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
