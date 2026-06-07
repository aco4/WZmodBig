import requests
from typing import TypedDict, cast, Literal


class NotFoundError(Exception):
    pass


# Types
PieName = str
StatId = str
StatFile = Literal['weapons.json', 'body.json', 'propulsion.json', 'structure.json', 'features.json']
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
StatItem = Weapon | Body | Propulsion | Structure | Feature

# Helpers
def lookup_stat_id(id: StatId) -> tuple[StatItem, StatFile]:
    stat_item = WEAPONS.get(id)
    if stat_item:
        return stat_item, 'weapons.json'

    stat_item = BODY.get(id)
    if stat_item:
        return stat_item, 'body.json'

    stat_item = PROPULSION.get(id)
    if stat_item:
        return stat_item, 'propulsion.json'

    stat_item = STRUCTURE.get(id)
    if stat_item:
        return stat_item, 'structure.json'

    stat_item = FEATURES.get(id)
    if stat_item:
        return stat_item, 'features.json'

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
    return cast(dict[StatId, Weapon], a), cast(dict[StatId, Body], b), cast(dict[StatId, Propulsion], c), cast(dict[StatId, Structure], d), cast(dict[StatId, Feature], e)

def scale(stat_item: StatItem, stat_file: StatFile, prefix: str, scale: int):
    discovered_pie_names = set[PieName]()
    discovered_stat_ids = set[StatId]()

    # Collect top-level .pie names and update them
    for key, pie_name in stat_item.items():
        if isinstance(pie_name, str) and pie_name.lower().endswith('.pie'):
            discovered_pie_names.add(pie_name.lower()) # collect
            stat_item[key] = prefix + pie_name # update

    # Process structureModel
    if stat_file == 'structure.json' and 'structureModel' in stat_item:
        new_structure_model: list[PieName] = []
        for pie_name in stat_item['structureModel']:
            discovered_pie_names.add(pie_name.lower()) # collect
            new_structure_model.append(prefix + pie_name)

        stat_item['structureModel'] = new_structure_model

    # Process weapons
    if stat_file == 'structure.json' and 'weapons' in stat_item:
        new_weapons: list[StatId] = []
        for component_id in stat_item['weapons']:
            discovered_stat_ids.add(component_id)
            new_weapons.append(prefix + component_id)

        stat_item['weapons'] = new_weapons

    # Process propulsionExtraModels
    if 'propulsionExtraModels' in stat_item:

        new_propulsion_extra_models = {}

        for component_id, propulsion_extra_model in stat_item['propulsionExtraModels'].items():

            new_propulsion_extra_models[prefix + component_id] = {}

            for state, pie_name in propulsion_extra_model.items():
                if pie_name.lower() == 'big2x_prltrk1.pie': raise ValueError("ju")
                discovered_pie_names.add(pie_name.lower())
                new_propulsion_extra_models[prefix + component_id][state] = prefix + pie_name

            discovered_stat_ids.add(component_id)

        stat_item['propulsionExtraModels'] = new_propulsion_extra_models

    # Process id
    if 'id' in stat_item:
        new_id = prefix + stat_item['id']
        stat_item['id'] = new_id

    # Process name
    if 'name' in stat_item:
        match scale:
            case 2: modifier = 'Big'
            case 3: modifier = 'Super Big'
            case 4: modifier = 'Massive'
            case _: modifier = 'Super Massive'
        stat_item['name'] = modifier + ' ' + stat_item['name']

    # Process buildPower
    if 'buildPower' in stat_item:
        stat_item['buildPower'] *= scale

    # Process buildPoints
    if 'buildPoints' in stat_item:
        stat_item['buildPoints'] *= scale

    # Process hitpoints
    if stat_file == 'body.json' and 'hitpoints' in stat_item:
        stat_item['hitpoints'] *= scale**2

    # Process size
    if stat_file == 'body.json' and 'size' in stat_item:
        if scale == 2 and stat_item['size'] == 'LIGHT':
            stat_item['size'] = 'MEDIUM'
        elif scale == 2 and stat_item['size'] == 'MEDIUM' or scale == 3 and stat_item['size'] == 'LIGHT':
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


# Fetch data
WEAPONS, BODY, PROPULSION, STRUCTURE, FEATURES = get_stats()
