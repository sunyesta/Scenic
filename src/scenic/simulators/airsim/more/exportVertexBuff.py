import json
import os
import pprint
import re
import tempfile
import time

import airsim
import cv2
import numpy as np
import trimesh

outputDirectory = (
    "/home/mary/Documents/AirSim/ScenicTesting/src/scenic/simulators/airsim/more/"
)

client = airsim.MultirotorClient()
client.confirmConnection()
client.simPause(True)


objNameDict = {}
assets = client.simListAssets()
for asset in assets:
    objName = client.simSpawnObject(
        object_name=asset,
        asset_name=asset,
        pose=airsim.Pose(position_val=airsim.Vector3r(0, 0, 0)),
        scale=airsim.Vector3r(1, 1, 1),
    )
    objNameDict[objName.lower()] = asset

print("getting buffs")
meshes = client.simGetMeshPositionVertexBuffers()
print("done")


meshesList = []

for mesh in meshes:
    meshName = mesh.name.lower()
    assetName = None
    if meshName in objNameDict:
        assetName = objNameDict[meshName]

    meshesList.append(
        dict(
            name=mesh.name,
            vertices=mesh.vertices,
            indices=mesh.indices,
            assetName=assetName,
        )
    )


with open(outputDirectory + "meshData.json", "w") as outfile:
    json.dump(meshesList, outfile)
