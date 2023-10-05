import random
import threading
import time

import airsim

client = airsim.MultirotorClient()
client.confirmConnection()


if len(client.listVehicles()) == 1:
    client.simAddVehicle(
        vehicle_name="Drone2",
        vehicle_type="simpleflight",
        pose=airsim.Pose(
            position_val=airsim.Vector3r(0, 0, -5),
        ),
    )

# client.simSpawnObject(
#     object_name="s",
#     asset_name="Cone",
#     pose=airsim.Pose(
#         position_val=airsim.Vector3r(0, 0, 0),
#     ),
#     scale=airsim.Vector3r(0.5, 0.5, 0.5),
# )

drone1 = client.listVehicles()[0]
drone2 = client.listVehicles()[1]

# connect to the AirSim simulator

client.enableApiControl(True, drone1)
client.enableApiControl(True, drone2)

client.simSetVehiclePose(
    airsim.Pose(
        position_val=airsim.Vector3r(4, 0, -2),
    ),
    True,
    drone1,
)
client.simSetVehiclePose(
    airsim.Pose(
        position_val=airsim.Vector3r(8, 0, -2),
    ),
    True,
    drone2,
)

client.armDisarm(True, drone1)
client.armDisarm(True, drone2)
