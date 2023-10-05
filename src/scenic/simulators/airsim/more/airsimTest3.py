# standard libs
from cmath import atan, pi, tan
import math
from math import copysign, degrees, radians, sin
import threading
import time

# third party libs
import airsim
import numpy as np
from promise import Promise
import scipy

# scenic libs
from scenic.core.simulators import (
    Simulation,
    SimulationCreationError,
    Simulator,
    SimulatorInterfaceWarning,
)
from scenic.core.type_support import toVector
from scenic.core.vectors import Orientation, Vector
from scenic.simulators.airsim.utils import (
    airsimToScenicLocation,
    airsimToScenicOrientation,
    scenicToAirsimOrientation,
    scenicToAirsimScale,
    scenicToAirsimVector,
)


def createPromise(future):
    def promFunc(resolve, reject):
        def joinAsync():
            future.join()
            resolve(True)

        threading.Thread(target=joinAsync).start()

    prom = Promise(promFunc)

    return prom


def flyToPosition(client, drone, home, newPos, speed=5, tolerance=1):
    """flys the drone to the specified position

    Args:
        client (airsim client): airsim client
        drone (string): drone name in airsim
        newPose (vector or tuple): position you want the drone to go to in scenic space
    """
    print("flying")
    newPos = scenicToAirsimVector(toVector(newPos))

    distance = 0
    while True:
        curPos = client.simGetVehiclePose(drone).position
        print(curPos.z_val)
        curToNew = newPos - curPos
        distance = curToNew.get_length()

        if distance <= tolerance:
            break

        curToNew = (curToNew / distance) * min(speed * distance, speed)
        Promise.wait(
            createPromise(
                client.moveByVelocityAsync(
                    curToNew.x_val,
                    curToNew.y_val,
                    curToNew.z_val,
                    duration=0.1,
                    vehicle_name=drone,
                )
            )
        )
    # print(drone, client.simGetVehiclePose(drone).position)


client = airsim.MultirotorClient()
client.confirmConnection()


client.reset()
# client.simPause(True)
drone1Start = airsim.Vector3r(0, 0, -5)

drone1 = client.listVehicles()[0]
client.enableApiControl(True, drone1)
client.armDisarm(True, drone1)
client.moveByVelocityAsync(0, 0, 0, duration=0.1, vehicle_name=drone1)

client.simPause(False)


print(drone1, client.simGetVehiclePose(drone1).position)
client.simSetVehiclePose(
    airsim.Pose(
        position_val=drone1Start,
    ),
    True,
    drone1,
)


time.sleep(1)
print(drone1, client.simGetVehiclePose(drone1).position)


def promComplete():
    print("finished")


flyToPosition(client, drone1, drone1Start, (3, 3, 3))


if not ("Drone2" in client.listVehicles()):
    client.simAddVehicle(
        vehicle_name="Drone2",
        vehicle_type="simpleflight",
        pose=airsim.Pose(
            airsim.Vector3r(0, 0, 0),
        ),
    )

drone2 = "Drone2"

client.enableApiControl(True, drone2)
client.armDisarm(True, drone2)
client.moveByVelocityAsync(0, 0, 0, duration=0.1, vehicle_name=drone2)

flyToPosition(client, drone2, drone1Start, (3, 3, 3))


# client.reset()
# gain = PIDGains(100, 0, 0)
# client.setVelocityControllerGains(
#     vehicle_name=drone, velocity_gains=VelocityControllerGains(gain, gain, gain)
# )
