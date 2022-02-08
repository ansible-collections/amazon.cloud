from ansible_collections.amazon.aws.plugins.module_utils.ec2 import camel_dict_to_snake_dict


def format_list(response):
    result = list()
    identifier = response.get('ResourceDescription', {}).get('Identifier', None)

    # Convert the Resource Properties from a str back to json
    properties = response.get('ResourceDescription', {}).get('Properties', {})
    properties = json.loads(properties)
    
    bucket = dict()
    bucket['Identifier'] = identifier
    bucket['properties'] = properties
    result.append(bucket)
    
    result = [camel_dict_to_snake_dict(res) for res in result]

    return result


def diff_dict(d1, d2):
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    shared_keys = d1_keys.intersection(d2_keys)
    shared_deltas = {o: (d1[o], d2[o]) for o in shared_keys if d1[o] != d2[o]}
    added_keys = d2_keys - d1_keys
    added_deltas = {o: (None, d2[o]) for o in added_keys}
    deltas = {**shared_deltas, **added_deltas}
    return parse_deltas(deltas)


def parse_deltas(deltas: dict):
    res = {}
    for k, v in deltas.items():
        if isinstance(v[0], dict):
            tmp = diff_dict(v[0], v[1])
            if tmp:
                res[k] = tmp
        else:
            res[k] = v[1]
    return res
