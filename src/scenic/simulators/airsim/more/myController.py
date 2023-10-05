import airsim


def goToPosition(client, drone, position):
    curPos = client.simGetVehiclePose(drone).position
    delta = pos - curPos
    delta /= delta.get_length()
    client.moveByVelocityAsync(delta.x_val, delta.y_val, delta.z_val)

    promise = Promise()

    return promise
