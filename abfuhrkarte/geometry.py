import overpass

from abfuhrkarte.constants import overpass_endpoint_url

overpass_api = overpass.API(endpoint=overpass_endpoint_url, timeout=600)

def query_geometry(street_name):
    r = overpass_api.get(
        f'area(3600062591);(way(area)["name"~"{street_name}"]["highway"];);(._;>;)', verbosity='geom')
    # extract the LineString(s)
    features = []
    for f in r.features:
        if f.geometry['type'] == "LineString" and f['id'] != 135848859:
            features.append(f)

    if len(features) == 1:
        return features[0]
    elif len(features) > 1:
        new_geom = []
        for f in features:
            new_geom.append(f.geometry['coordinates'])

        features[0].geometry['type'] = 'MultiLineString'
        features[0].geometry['coordinates'] = new_geom
        return features[0]

def query_geometries(street_names):
    geometries = {}
    for street_name in street_names:
        # street_name = entry.get('strasse')
        if street_name not in geometries:
            geometries[street_name] = query_geometry(street_name)
            print(".", end='', flush=True)
    return geometries
