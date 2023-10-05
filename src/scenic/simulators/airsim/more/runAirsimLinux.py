import subprocess

import airsim

# Path to the shortcut file
shortcut_path = (
    r"/home/mary/Documents/AirSim/Blocks/LinuxBlocks1.8.1/LinuxNoEditor/Blocks.sh"
)

# Command-line arguments for the executable
arguments = '-settings="/home/mary/Documents/AirSim/ScenicTesting/src/scenic/simulators/airsim/objs/cubes/airsimSettings.json"'

# Construct the command to run the shortcut with arguments
command = f"{shortcut_path} {arguments}"

subprocess.run(command, shell=True)


client = airsim.VehicleClient()
client.confirmConnection()
client.simPause(True)
