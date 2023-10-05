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

client = airsim.MultirotorClient()
client.confirmConnection()


client.simPause(True)


meshes = client.simGetMeshPositionVertexBuffers()


meshDict = {}
for mesh in meshes:
    meshDict[mesh.name] = mesh


print(meshDict.keys())

m = meshDict["templatecube_rounded_97"]
vertex_list = np.array(m.vertices, dtype=np.float32)
indices = np.array(m.indices, dtype=np.uint32)

num_vertices = int(len(vertex_list) / 3)
num_indices = len(indices)

vertices_reshaped = vertex_list.reshape((num_vertices, 3))
indices_reshaped = indices.reshape((int(num_indices / 3), 3))
vertices_reshaped = vertices_reshaped.astype(np.float64)
indices_reshaped = indices_reshaped.astype(np.int64)

tmesh = trimesh.Trimesh(vertices=vertices_reshaped, faces=indices_reshaped, process=True)
if tmesh.body_count > 1:
    tmesh.fix_normals(multibody=True)
else:
    tmesh.fix_normals()


tmesh.show()

print(len(objs))
