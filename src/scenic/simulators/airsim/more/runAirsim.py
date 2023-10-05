import subprocess

import airsim

# Path to the shortcut file
shortcut_path = r"C:\Users\Mary\Documents\Code\Scenic\AirSimBinaries\Blocks\WindowsNoEditor\Blocks.exe"

# Command-line arguments for the executable
arguments = '-settings="C:\\Users\\Mary\\Documents\\Code\\Scenic\\airsimTesting\\settings\\noVehicles.json"'

# Construct the command to run the shortcut with arguments
command = f"start {shortcut_path} {arguments}"

subprocess.run(command, shell=True)


client = airsim.VehicleClient()
client.confirmConnection()
client.simPause(True)
