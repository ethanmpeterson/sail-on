#!/usr/bin/python3

import sys, pygrib, numpy, networkx, json

def main():
    
    a-coord = [sys.argv[0], sys.argv[1]]
    b-coord = [sys.argv[2], sys.argv[3]]

    for i in range(2):
        a-coord[i] *= 4
        b-coord[i] *= 4

    # Open weather data files
    dirFile = pygrib.open('gfs.t12z.pgrb2.0p25.f008.VGRD')
    vFile = pygrib.open('gfs.t12z.pgrb2.0p25.f008.UGRD')

    # Extract primary message
    vMessage = vFile.message(1)
    dirMessage = dirFile.message(1)

    # Extract subset of global grid for faster processing
    globalGrid = gribToDict(vMessage, dirMessage)
    extractGrid = extractData(globalGrid, 100, 100)

    graph = buildGraph(extractGrid)
    shortest = networkx.shortest_path(graph, 8, 8000)

    xcoords = networkx.get_node_attributes(graph, 'x')
    ycoords = networkx.get_node_attributes(graph, 'y')

    output = {"path": []}

    for i in shortest:
        output["path"].append({
                    'lat': xcoords[i],
                    'lon': ycoords[i],
                })

    print(json.dumps(output))

def gribToDict(v, d):

    data = {
            'count': v.numberOfValues,
            'height': 360 * 4,
            'width': 360 * 4,

            'v': v.codedValues.tolist(),
            'd': d.codedValues.tolist(),

            'co-ords': {
                'x': v.latitudes.tolist(),
                'y': v.longitudes.tolist(),
                },
            }

    return data


def extractData(superSet, h, w):
    
    resolution = 0.25 # 0.25 degree grid resolution
    gridDimention = int(360 / resolution)

    data = {}

    data['count'] = h * w
    data['height'] = h
    data['width'] = w

    data['v'] = data['d'] = []

    data['co-ords'] = {
            'x': [],
            'y': [],
            }

    for i in range(0, h):
        lower = gridDimention * h
        upper = lower + w

        data['v'] += superSet['v'][lower:upper]
        data['d'] += superSet['d'][lower:upper]

        data['co-ords']['x'] += superSet['co-ords']['x'][lower:upper]
        data['co-ords']['y'] += superSet['co-ords']['y'][lower:upper]

    return data


def buildGraph(grid):
    graph = networkx.Graph()

    # create graph of grid points labeled by co-ordinate
    for i in range(grid['count']):
        graph.add_node(i, x=grid['co-ords']['x'][i], y=grid['co-ords']['y'][i])

    for i in range(grid['width']):
        for j in range(grid['height']):

            a = i * grid['width'] + j

            # if there is a node to the left, connect it
            if (i < grid['width']):
                b = a + 1
                graph.add_edge(a, b, weight=avg(a,b))

                # if there is a node to the [down, left] connect it
                if (j < grid['height']):
                    b = a + grid['width'] + 1
                    graph.add_edge(a, b, weight=avg(a,b))

            # if there is a node to the [down, right] connect it
            if (i > 0 and j < grid['height']):
                b = a + grid['width'] - 1
                graph.add_edge(a, b, weight=avg(a,b))

            # if there is a node below connect it
            if (j < grid['height']):
                b = a + grid['width']
                graph.add_edge(a, b, weight=avg(a,b))
                
    return graph


def avg(a, b):
    return (a + b) / 2

main()
