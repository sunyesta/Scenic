import random
import threading
import time

import airsim
from promise import Promise


def goToPosition(drone, pos):
    curPos = client.simGetVehiclePose(drone).position
    delta = pos - curPos
    delta /= delta.get_length()
    client.moveByVelocityAsync(delta.x_val, delta.y_val, delta.z_val)

    promise = Promise()

    return promise


def scenicToAirsimRotation(orientation):
    pitch, yaw, roll = orientation.r.as_euler("XZY", degrees=True)
    return airsim.to_quaternion(pitch, roll, yaw)


def startWait(future):
    def joinAsync():
        future.join()

    threading.Thread(target=joinAsync).start()

    return future


client = airsim.MultirotorClient()
client.confirmConnection()

print(client.simListAssets())
if len(client.listVehicles()) == 1:
    client.simAddVehicle(
        vehicle_name="drone2",
        vehicle_type="simpleflight",
        pose=airsim.Pose(
            position_val=airsim.Vector3r(0, 0, -5),
        ),
    )

# client.simSpawnObject(
#     "myobj",
#     "Cube",
#     airsim.Pose(
#         position_val=airsim.Vector3r(0, 0, -3),
#     ),
#     airsim.Vector3r((1, 1, 1)),
# )

drone1 = client.listVehicles()[0]
drone2 = client.listVehicles()[1]

# enable api control
client.enableApiControl(True, drone1)
client.enableApiControl(True, drone2)
client.armDisarm(True, drone1)
client.armDisarm(True, drone2)

# start drones
client.moveByVelocityAsync(0, 0, 0, 1, vehicle_name=drone1)
client.moveByVelocityAsync(0, 0, 0, 1, vehicle_name=drone2)


client.simSetVehiclePose(
    airsim.Pose(
        position_val=airsim.Vector3r(-5, 0, -5),
    ),
    True,
    drone1,
)
client.simSetVehiclePose(
    airsim.Pose(
        position_val=airsim.Vector3r(5, 0, -5),
    ),
    True,
    drone2,
)
client.simPause(False)

time.sleep(1)

f1 = client.moveToPositionAsync(
    0,
    0,
    0,
    5,
    vehicle_name=drone1,
)
f2 = client.moveToPositionAsync(
    0,
    0,
    1,
    5,
    vehicle_name=drone2,
)

f1.join()
f2.join()


print("Drone 1 pos = ", client.simGetVehiclePose(drone1).position)
print("Drone 2 pos = ", client.simGetVehiclePose(drone2).position)

client.simPause(False)

time.sleep(0.1)
# client.simPause(True)
