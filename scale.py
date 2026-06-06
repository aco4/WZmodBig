import requests
from typing import TypedDict, cast, Literal


# Custom Exceptions
class NotFoundError(Exception):
    pass


# Types
PieName = str
StatId = str
StatFile = Literal['weapons.json', 'body.json', 'propulsion.json', 'structure.json', 'features.json']
class InputEntry(TypedDict):
    id: StatId
    stat_file: StatFile
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
Diffs = dict[StatFile, dict[StatId, StatItem]]

# Helpers
def raiseException(e: Exception):
    raise e

def get_stat_item(id: StatId, stat_file: StatFile) -> StatItem:
    e = NotFoundError(f'{id} was not found in {stat_file}!')
    match stat_file:
        case 'weapons.json'    : return WEAPONS   .get(id) or raiseException(e)
        case 'body.json'       : return BODY      .get(id) or raiseException(e)
        case 'propulsion.json' : return PROPULSION.get(id) or raiseException(e)
        case 'structure.json'  : return STRUCTURE .get(id) or raiseException(e)
        case 'features.json'   : return FEATURES  .get(id) or raiseException(e)

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

def process_inputs(work_queue: list[InputEntry], scale: int, prefix: str):
    def process_entry(entry: InputEntry):
        stat_item = get_stat_item(entry['id'], entry['stat_file'])

        # Collect top-level .pie names and update them
        for key, pie_name in stat_item.items():
            if isinstance(pie_name, str) and pie_name.lower().endswith('.pie'):
                pending_pie_names.add(pie_name.lower()) # collect
                stat_item[key] = prefix + pie_name # update

        # Process structureModel
        if entry['stat_file'] == 'structure.json' and 'structureModel' in stat_item:
            new_structure_model: list[PieName] = []
            for pie_name in stat_item['structureModel']:
                pending_pie_names.add(pie_name.lower()) # collect
                new_structure_model.append(prefix + pie_name)

            stat_item['structureModel'] = new_structure_model

        # Process weapons
        if entry['stat_file'] == 'structure.json' and 'weapons' in stat_item:
            new_weapons: list[StatId] = []
            for component_id in stat_item['weapons']:
                work_queue.append({
                    'id': component_id,
                    'stat_file': 'weapons.json'
                })
                new_weapons.append(prefix + component_id)

            stat_item['weapons'] = new_weapons

        # Process propulsionExtraModels
        if 'propulsionExtraModels' in stat_item:

            new_propulsion_extra_models = {}

            for component_id, propulsion_extra_model in stat_item['propulsionExtraModels'].items():

                new_propulsion_extra_models[prefix + component_id] = {}

                for state, pie_name in propulsion_extra_model.items():
                    if pie_name.lower() == 'big2x_prltrk1.pie': raise ValueError("ju")
                    pending_pie_names.add(pie_name.lower())
                    new_propulsion_extra_models[prefix + component_id][state] = prefix + pie_name

                work_queue.append({
                    'id': component_id,
                    'stat_file': 'propulsion.json'
                })

            stat_item['propulsionExtraModels'] = new_propulsion_extra_models

        # Process id
        if 'id' in stat_item:
            new_id = prefix + entry['id']
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
        if entry['stat_file'] == 'body.json' and 'hitpoints' in stat_item:
            stat_item['hitpoints'] *= scale**2

        # Process size
        if entry['stat_file'] == 'body.json' and 'size' in stat_item:
            if scale == 2 and stat_item['size'] == 'LIGHT':
                stat_item['size'] = 'MEDIUM'
            elif scale == 2 and stat_item['size'] == 'MEDIUM' or scale == 3 and stat_item['size'] == 'LIGHT':
                stat_item['size'] = 'HEAVY'
            else:
                stat_item['size'] = 'SUPER HEAVY'

        # Process shortRange
        if entry['stat_file'] == 'weapons.json' and 'shortRange' in stat_item:
            stat_item['shortRange'] += 128 * scale

        # Process longRange
        if entry['stat_file'] == 'weapons.json' and 'longRange' in stat_item:
            stat_item['longRange'] += 128 * scale

        # Process width
        if entry['stat_file'] == 'structure.json' and 'width' in stat_item:
            stat_item['width'] *= scale

        # Process breadth
        if entry['stat_file'] == 'structure.json' and 'breadth' in stat_item:
            stat_item['breadth'] *= scale

        # Collect diffs
        diffs[entry['stat_file']][stat_item['id']] = stat_item

        # Mark component as complete
        finished_entries.add(entry['id'])

    finished_entries = set[StatId]()

    # Collect all pie names (e.g. 'prltrk1.pie') before scaling.
    # Must be lowercase!
    pending_pie_names = set[str]()

    # Collect diffs
    diffs: Diffs = {
        'weapons.json': {},
        'body.json': {},
        'propulsion.json': {},
        'structure.json': {},
        'features.json': {}
    }

    while len(work_queue) > 0:
        entry = work_queue.pop(0)
        if not entry['id'] in finished_entries:
            process_entry(entry)

    return pending_pie_names, diffs

# Fetch data
WEAPONS, BODY, PROPULSION, STRUCTURE, FEATURES = get_stats()
