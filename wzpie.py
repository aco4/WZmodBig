import requests
from typing import TypedDict, Literal

class PieData(TypedDict):
    url: str
    path: str
    text: str
    group: str
    type: Literal['component', 'structure', 'feature', 'effect']
    subtype: str | None

pie_dict: dict[str, PieData] = {}

def get(pie_name: str):
    if not is_pie_name(pie_name): raise TypeError('pie_name is not type pie_name')

    if pie_dict.get(pie_name) is None and not find(pie_name):
        return None
    return pie_dict.get(pie_name)


# Type check
def is_pie_name(string: object):
    return isinstance(string, str) and string.islower() and len(string) > 4 and not string.startswith(BASE_URL) and string.endswith('.pie')

# GET request
BASE_URL = 'https://raw.githubusercontent.com/Warzone2100/warzone2100/refs/heads/master/data/'
def request(url: str):
    try:
        print('GET', url)
        response = requests.get(url) # GET request
        response.raise_for_status() # bad codes 4xx or 5xx
        return response.text
    except requests.exceptions.RequestException:
        return None

def find(pie_name: str):
    if not is_pie_name(pie_name): raise TypeError('pie_name is not type pie_name')

    # Edge case
    if pie_name == 'dpvtol.pie':
        pie_url = BASE_URL + 'base/misc/researchimds/' + pie_name
        pie_text = request(pie_url)
        if pie_text:
            pie_dict[pie_name] = {
                'url': pie_url,
                'path': 'components/prop',
                'text': pie_text,
                'group': 'base',
                'type': 'component',
                'subtype': 'propulsion'
            }
            return True
        return False

    pie_url = BASE_URL + 'base/components/prop/' + pie_name
    pie_text = request(pie_url)
    if pie_text:
        pie_dict[pie_name] = {
            'url': pie_url,
            'path': 'components/prop',
            'text': pie_text,
            'group': 'base',
            'type': 'component',
            'subtype': 'propulsion'
        }
        return True

    pie_url = BASE_URL + 'base/effects/' + pie_name
    pie_text = request(pie_url)
    if pie_text:
        pie_dict[pie_name] = {
            'url': pie_url,
            'path': 'effects',
            'text': pie_text,
            'group': 'base',
            'type': 'effect',
            'subtype': None
        }
        return True

    pie_url = BASE_URL + 'base/components/weapons/' + pie_name
    pie_text = request(pie_url)
    if pie_text:
        pie_dict[pie_name] = {
            'url': pie_url,
            'path': 'components/weapons',
            'text': pie_text,
            'group': 'base',
            'type': 'component',
            'subtype': 'weapon'
        }
        return True

    pie_url = BASE_URL + 'base/components/bodies/' + pie_name
    pie_text = request(pie_url)
    if pie_text:
        pie_dict[pie_name] = {
            'url': pie_url,
            'path': 'components/bodies',
            'text': pie_text,
            'group': 'base',
            'type': 'component',
            'subtype': 'body'
        }
        return True

    pie_url = BASE_URL + 'mp/components/weapons/' + pie_name
    pie_text = request(pie_url)
    if pie_text:
        pie_dict[pie_name] = {
            'url': pie_url,
            'path': 'components/weapons',
            'text': pie_text,
            'group': 'mp',
            'type': 'component',
            'subtype': 'weapon'
        }
        return True

    pie_url = BASE_URL + 'mp/components/prop/' + pie_name
    pie_text = request(pie_url)
    if pie_text:
        pie_dict[pie_name] = {
            'url': pie_url,
            'path': 'components/prop',
            'text': pie_text,
            'group': 'mp',
            'type': 'component',
            'subtype': 'propulsion'
        }
        return True

    pie_url = BASE_URL + 'mp/components/bodies/' + pie_name
    pie_text = request(pie_url)
    if pie_text:
        pie_dict[pie_name] = {
            'url': pie_url,
            'path': 'components/bodies',
            'text': pie_text,
            'group': 'mp',
            'type': 'component',
            'subtype': 'body'
        }
        return True

    pie_url = BASE_URL + 'base/structs/' + pie_name
    pie_text = request(pie_url)
    if pie_text:
        pie_dict[pie_name] = {
            'url': pie_url,
            'path': 'structs',
            'text': pie_text,
            'group': 'base',
            'type': 'structure',
            'subtype': None
        }
        return True

    pie_url = BASE_URL + 'base/features/' + pie_name
    pie_text = request(pie_url)
    if pie_text:
        pie_dict[pie_name] = {
            'url': pie_url,
            'path': 'features',
            'text': pie_text,
            'group': 'base',
            'type': 'feature',
            'subtype': None
        }
        return True

    pie_url = BASE_URL + 'mp/effects/' + pie_name
    pie_text = request(pie_url)
    if pie_text:
        pie_dict[pie_name] = {
            'url': pie_url,
            'path': 'effects',
            'text': pie_text,
            'group': 'mp',
            'type': 'effect',
            'subtype': None
        }
        return True

    return False


# Pie manipulation
def scale(pie_text: str, scale: float):
    lines = pie_text.splitlines()
    output: list[str] = []
    for line in lines:
        parts = line.strip().split()
        if line[0] == '\t' and len(parts) == 3:
            x, y, z = float(parts[0]), float(parts[1]), float(parts[2])
            x2 = x * scale
            y2 = y * scale
            z2 = z * scale
            output.append(f'\t{x2} {y2} {z2}')
        else:
            output.append(line)

    return '\n'.join(output)
