import requests
from typing import TypedDict, cast, Literal
import copy


class NotFoundError(Exception):
    pass


# Types
PieName = str
StatId = str
StatFile = Literal['weapons.json', 'body.json', 'propulsion.json', 'structure.json', 'features.json', 'research.json']
PropulsionExtraModel = dict[Literal['left', 'still', 'moving'], PieName]
class Weapon(TypedDict):
    id: StatId
    name: str
    buildPoints: int
    buildPower: int
    shortRange: int
    longRange: int
class Body(TypedDict):
    id: StatId
    name: str
    buildPoints: int
    buildPower: int
    hitpoints: int
    propulsionExtraModels: dict[StatId, PropulsionExtraModel]
    size: str
class Propulsion(TypedDict):
    id: StatId
    name: str
    buildPoints: int
    buildPower: int
class Structure(TypedDict):
    id: StatId
    name: str
    buildPoints: int
    buildPower: int
    width: int
    breadth: int
    structureModel: list[PieName]
    weapons: list[StatId]
class Feature(TypedDict):
    id: StatId
    name: str
class Research(TypedDict):
    id: StatId
    name: str
    requiredResearch: list[StatId]
    researchPoints: int
    researchPower: int
    resultComponents: list[StatId]
    resultStructures: list[StatId]
    statID: StatId
StatItem = Weapon | Body | Propulsion | Structure | Feature | Research
Diffs = dict[StatFile, dict[StatId, StatItem]]

# Helpers
def lookup_stat_id(id: StatId) -> tuple[StatItem, StatFile]:
    """Get the stat info from a dictionary in O(1) time.

    Raises:
        NotFoundError: If the id is not found in any of the JSON files
    """
    stat_item = WEAPONS.get(id)
    if stat_item:
        return copy.deepcopy(stat_item), 'weapons.json'

    stat_item = BODY.get(id)
    if stat_item:
        return copy.deepcopy(stat_item), 'body.json'

    stat_item = PROPULSION.get(id)
    if stat_item:
        return copy.deepcopy(stat_item), 'propulsion.json'

    stat_item = STRUCTURE.get(id)
    if stat_item:
        return copy.deepcopy(stat_item), 'structure.json'

    stat_item = FEATURES.get(id)
    if stat_item:
        return copy.deepcopy(stat_item), 'features.json'

    stat_item = RESEARCH.get(id)
    if stat_item:
        return copy.deepcopy(stat_item), 'research.json'

    raise NotFoundError(f'{id} was not found!')

def get_json(url: str):
    response = requests.get(url) # GET request
    response.raise_for_status() # bad codes 4xx or 5xx
    return response.json()

def get_stats():
    """
        Raises:
            HTTPError: If GET request fails
    """
    a = get_json('https://raw.githubusercontent.com/Warzone2100/warzone2100/refs/heads/master/data/mp/stats/weapons.json')
    b = get_json('https://raw.githubusercontent.com/Warzone2100/warzone2100/refs/heads/master/data/mp/stats/body.json')
    c = get_json('https://raw.githubusercontent.com/Warzone2100/warzone2100/refs/heads/master/data/mp/stats/propulsion.json')
    d = get_json('https://raw.githubusercontent.com/Warzone2100/warzone2100/refs/heads/master/data/mp/stats/structure.json')
    e = get_json('https://raw.githubusercontent.com/Warzone2100/warzone2100/refs/heads/master/data/base/stats/features.json')
    f = get_json('https://raw.githubusercontent.com/Warzone2100/warzone2100/refs/heads/master/data/mp/stats/research.json')
    return cast(dict[StatId, Weapon], a), cast(dict[StatId, Body], b), cast(dict[StatId, Propulsion], c), cast(dict[StatId, Structure], d), cast(dict[StatId, Feature], e), cast(dict[StatId, Research], f)

def scale(stat_item: StatItem, stat_file: StatFile, *, prefix: str, scale: int, vanilla_propulsion: bool=False, initial_stat_ids: frozenset[StatId]=frozenset(), research: bool=False):
    discovered_pie_names = set[PieName]()
    discovered_stat_ids = set[StatId]()

    # Process id
    if 'id' in stat_item:
        old_id = stat_item['id']
        new_id = prefix + old_id
        stat_item['id'] = new_id

    # Process name
    if 'name' in stat_item:
        match scale:
            case 2: modifier = 'Big '
            case 3: modifier = 'Super Big '
            case 4: modifier = 'Massive '
            case _: modifier = 'Super Massive '
        stat_item['name'] = modifier + stat_item['name']

    # Process buildPower
    if 'buildPower' in stat_item:
        stat_item['buildPower'] *= scale

    # Process buildPoints
    if 'buildPoints' in stat_item:
        stat_item['buildPoints'] *= scale

    # Collect top-level .pie names and update them
    for key, pie_name in stat_item.items():
        if isinstance(pie_name, str) and pie_name.lower().endswith('.pie'):
            discovered_pie_names.add(pie_name.lower())
            stat_item[key] = prefix + pie_name

    # Process structureModel
    if stat_file == 'structure.json' and 'structureModel' in stat_item:
        new_structure_model: list[PieName] = []
        for pie_name in stat_item['structureModel']:
            discovered_pie_names.add(pie_name.lower())
            new_structure_model.append(prefix + pie_name)

        stat_item['structureModel'] = new_structure_model

    # Process weapons
    if stat_file == 'structure.json' and 'weapons' in stat_item:
        new_weapons: list[StatId] = []
        for weapon_id in stat_item['weapons']:
            discovered_stat_ids.add(weapon_id)
            new_weapons.append(prefix + weapon_id)

        stat_item['weapons'] = new_weapons

    # Process propulsionExtraModels
    if 'propulsionExtraModels' in stat_item:

        new_propulsion_extra_models = {}

        for propulsion_id, propulsion_extra_model in stat_item['propulsionExtraModels'].items():
            if propulsion_id in initial_stat_ids:
                if vanilla_propulsion:
                    new_propulsion_id = propulsion_id
                else:
                    new_propulsion_id = prefix + propulsion_id

                new_propulsion_extra_models[new_propulsion_id] = {}

                for state, pie_name in propulsion_extra_model.items():
                    discovered_pie_names.add(pie_name.lower())
                    new_propulsion_extra_models[new_propulsion_id][state] = prefix + pie_name

                discovered_stat_ids.add(propulsion_id)

        stat_item['propulsionExtraModels'] = new_propulsion_extra_models

    # Process research
    if stat_file == 'research.json' and 'requiredResearch' in stat_item:
        stat_item['requiredResearch'] = [old_id]
    if stat_file == 'research.json' and 'researchPoints' in stat_item:
        stat_item['researchPoints'] = min(65535, 2 * stat_item['researchPoints'])
    if stat_file == 'research.json' and 'researchPower' in stat_item:
        stat_item['researchPower'] *= 2
    if stat_file == 'research.json' and 'resultComponents' in stat_item:
        for result_component in stat_item['resultComponents']:
            discovered_stat_ids.add(result_component)
        stat_item['resultComponents'] = [ prefix + x for x in stat_item['resultComponents'] ]
    if stat_file == 'research.json' and 'resultStructures' in stat_item:
        for result_component in stat_item['resultStructures']:
            discovered_stat_ids.add(result_component)
        stat_item['resultStructures'] = [ prefix + x for x in stat_item['resultStructures'] ]
    if stat_file == 'research.json' and 'statID' in stat_item:
        stat_item['statID'] = prefix + stat_item['statID']

    # Process hitpoints
    if stat_file == 'body.json' and 'hitpoints' in stat_item:
        stat_item['hitpoints'] *= scale**2

    # Process size
    if stat_file == 'body.json' and 'size' in stat_item:
        if scale == 2 and stat_item['size'] == 'LIGHT':
            stat_item['size'] = 'HEAVY'
        else:
            stat_item['size'] = 'SUPER HEAVY'

    # Process shortRange
    if stat_file == 'weapons.json' and 'shortRange' in stat_item:
        stat_item['shortRange'] += 128 * scale

    # Process longRange
    if stat_file == 'weapons.json' and 'longRange' in stat_item:
        stat_item['longRange'] += 128 * scale

    # Process width
    if stat_file == 'structure.json' and 'width' in stat_item:
        stat_item['width'] *= scale

    # Process breadth
    if stat_file == 'structure.json' and 'breadth' in stat_item:
        stat_item['breadth'] *= scale

    return stat_item, discovered_pie_names, discovered_stat_ids

def scale_all(stat_ids: list[StatId], prefix: str, SCALE: int, vanilla_propulsion: bool=False, research: bool=False):
    # Helper data structures
    work_queue: list[StatId] = stat_ids
    initial_stat_ids = frozenset[StatId](stat_id for stat_id in stat_ids)
    finished_stat_ids = set[StatId]()

    # Add research stat items
    if research:
        for research_item in RESEARCH.values():
            for stat_id in stat_ids:
                _, stat_file = lookup_stat_id(stat_id)
                if stat_file == 'propulsion.json' and vanilla_propulsion:
                    continue

                if 'resultComponents' in research_item and stat_id in research_item['resultComponents']:
                    work_queue.append(research_item['id'])
                if 'resultStructures' in research_item and stat_id in research_item['resultStructures']:
                    work_queue.append(research_item['id'])

    # Output
    unscaled_pie_names = set[PieName]()
    unwritten_diffs: Diffs = {}

    # Scale the stat items
    while len(work_queue) > 0:
        stat_id = work_queue.pop()
        if stat_id in finished_stat_ids:
            continue

        stat_item, stat_file = lookup_stat_id(stat_id)

        if stat_file == 'propulsion.json' and vanilla_propulsion:
            finished_stat_ids.add(stat_id)
            continue
        if stat_file == 'research.json' and not research:
            finished_stat_ids.add(stat_id)
            continue

        if stat_file not in unwritten_diffs:
            unwritten_diffs[stat_file] = {}

        new_stat_item, discovered_pie_names, discovered_stat_ids = scale(
            stat_item,
            stat_file,
            prefix=prefix,
            scale=SCALE,
            initial_stat_ids=initial_stat_ids,
            vanilla_propulsion=vanilla_propulsion,
        )

        finished_stat_ids.add(stat_id)

        for pie_name in discovered_pie_names:
            unscaled_pie_names.add(pie_name)

        for discovered_stat_id in discovered_stat_ids:
            if discovered_stat_id not in finished_stat_ids:
                work_queue.append(discovered_stat_id)

        # Collect diffs
        unwritten_diffs[stat_file][prefix + stat_id] = new_stat_item

    return unscaled_pie_names, unwritten_diffs


# Fetch data
WEAPONS, BODY, PROPULSION, STRUCTURE, FEATURES, RESEARCH = get_stats()
