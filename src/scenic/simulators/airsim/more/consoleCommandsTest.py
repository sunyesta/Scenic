import airsim

# Connect to the AirSim simulator
client = airsim.MultirotorClient()
client.confirmConnection()

print(client.simListSceneObjects())

# Run a console command in the simulation
command = "quit"
response = client.simRunConsoleCommand(command)

# Check the response from the console command
print("Console command response:", response)
