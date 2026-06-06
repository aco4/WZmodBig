# Big
This Warzone 2100 mod adds big units and structures.

# Build
```bash
python3 main.py --scale 2 --inputs '[{"id":"tracked01","stat_file":"propulsion.json"},{"id":"Body11ABT","stat_file":"body.json"},{"id":"Cannon4AUTOMk1","stat_file":"weapons.json"},{"id":"PillBox4","stat_file":"structure.json"}]'
```
or
```bash
python3 main.py --scale 2 \
        --weapons $(grep -oP 'turrets:\s*\["x2_\K[^"]+' TEMPLATES.js | sort -u) \
        --bodies $(grep -oP 'body:\s*"x2_\K[^"]+' TEMPLATES.js | sort -u) \
        --propulsions $(grep -oP 'propulsion:\s*"x2_\K[^"]+' TEMPLATES.js | sort -u) && \
python3 main.py --scale 3 \
        --weapons $(grep -oP 'turrets:\s*\["x3_\K[^"]+' TEMPLATES.js | sort -u) \
        --bodies $(grep -oP 'body:\s*"x3_\K[^"]+' TEMPLATES.js | sort -u) \
        --propulsions $(grep -oP 'propulsion:\s*"x3_\K[^"]+' TEMPLATES.js | sort -u) && \
python3 main.py --scale 4 \
        --weapons $(grep -oP 'turrets:\s*\["x4_\K[^"]+' TEMPLATES.js | sort -u) \
        --bodies $(grep -oP 'body:\s*"x4_\K[^"]+' TEMPLATES.js | sort -u) \
        --propulsions $(grep -oP 'propulsion:\s*"x4_\K[^"]+' TEMPLATES.js | sort -u) && \
python3 main.py --scale 5 \
        --weapons $(grep -oP 'turrets:\s*\["x5_\K[^"]+' TEMPLATES.js | sort -u) \
        --bodies $(grep -oP 'body:\s*"x5_\K[^"]+' TEMPLATES.js | sort -u) \
        --propulsions $(grep -oP 'propulsion:\s*"x5_\K[^"]+' TEMPLATES.js | sort -u)
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
