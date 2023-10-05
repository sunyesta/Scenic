import json

import numpy as np
import trimesh

# Load the obj files

tmeshes = []
scene = trimesh.Scene()

with open(
    "/home/mary/Documents/AirSim/ScenicTesting/src/scenic/simulators/airsim/objs/cubes/worldInfo.json",
    "r",
) as inFile:
    meshes = json.load(inFile)
    for meshData in meshes:
        tmesh = trimesh.load(
            "/home/mary/Documents/AirSim/ScenicTesting/src/scenic/simulators/airsim/objs/cubes/"
            + meshData["assetName"]
            + ".obj"
        )
        scale = 0.05
        # matrix = np.eye(4)
        # matrix[:2, :2] *= scale
        # matrix[0][3] = meshData["position"][0]
        # matrix[1][3] = meshData["position"][1]
        # matrix[2][3] = meshData["position"][2]

        matrix = [
            [scale, 0, 0, meshData["position"][0]],
            [0, scale, 0, meshData["position"][1]],
            [0, 0, scale, -meshData["position"][2]],
            [0, 0, 0, 1],
        ]

        print(matrix)
        tmesh.apply_transform(matrix)

        color = trimesh.visual.random_color()
        for facet in tmesh.facets:
            tmesh.visual.face_colors[facet] = color

        scene.add_geometry(tmesh)


# Show all the meshes

scene.set_camera(center=(0, 0, 0), distance=30)
scene.show()
