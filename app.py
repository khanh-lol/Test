import discord
import requests
import os  # To read environment variables securely

# Create an instance of the bot client
intents = discord.Intents.default()
intents.message_content = True  # Make sure the bot can read message content
client = discord.Client(intents=intents)

# Roblox API URL for fetching game servers
ROBLOX_API_URL = "https://games.roblox.com/v1/games/{game_id}/servers/Public?sortOrder=Asc&limit=100"

# The game ID for "The Chosen One"
GAME_ID = "11137575513"

# Event listener when the bot has connected
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

# Create a class for the button interaction
class JoinServerButton(discord.ui.Button):
    def __init__(self, server_id):
        super().__init__(label=f"Join Server {server_id}", style=discord.ButtonStyle.success)
        self.server_id = server_id

    async def callback(self, interaction: discord.Interaction):
        # Prepare the Lua command for teleportation using the server ID
        lua_command = f'game:GetService("ReplicatedStorage").__ServerBrowser:InvokeServer("teleport","{self.server_id}")'
        # Respond to the interaction
        await interaction.response.send_message(f"Copy and run this command in Roblox:\n`{lua_command}`")

# Event listener when a message is received
@client.event
async def on_message(message):
    if message.author == client.user:
        return  # Ignore messages from the bot itself

    # Command to find the best server in "The Chosen One" game
    if message.content.startswith('!findserver'):
        await message.channel.send("e")  # Respond with "e" when the command is called

        # Fetch server info from Roblox
        try:
            response = requests.get(ROBLOX_API_URL.format(game_id=GAME_ID))
            data = response.json()

            if "data" not in data or len(data['data']) == 0:
                await message.channel.send('No servers found for this game ID.')
                return

            # Find the server with the most players
            best_server = max(data['data'], key=lambda server: server['playing'])

            # Send server details to the Discord channel
            server_info = f"Best server for game ID {GAME_ID} ('The Chosen One'):\n" \
                          f"Server ID: {best_server['id']}\n" \
                          f"Playing: {best_server['playing']}/{best_server['maxPlayers']}\n" \
                          f"Ping: {best_server['ping']}ms"
            await message.channel.send(server_info)

        except Exception as e:
            await message.channel.send(f"Error fetching server info: {str(e)}")

    # Command to find an item in "The Chosen One" game
    if message.content.startswith('/find'):
        item_name = "The Arkenstone"  # Name of the item to search for

        # Fetch server info from Roblox
        try:
            response = requests.get(ROBLOX_API_URL.format(game_id=GAME_ID))
            data = response.json()

            if "data" not in data or len(data['data']) == 0:
                await message.channel.send('No servers found for this game ID.')
                return

            server_info_list = []
            for server in data['data']:
                server_info_list.append((server['id'], server['playing']))

            # Limit the number of servers sent to avoid exceeding the character limit
            max_servers_to_send = 5  # You can adjust this number
            servers_to_send = server_info_list[:max_servers_to_send]

            # Prepare the response message
            response_message = f"Look for {item_name} in the game. Available servers:\n"

            # Create buttons for each server
            view = discord.ui.View()
            for server_id, players in servers_to_send:
                button = JoinServerButton(server_id)
                view.add_item(button)

            # Send the response with buttons
            await message.channel.send(response_message, view=view)

        except Exception as e:
            await message.channel.send(f"Error fetching item info: {str(e)}")



# Run the bot using the token
client.run('MTI5ODg4NzE3Mjg0OTQwMTg3Nw.Ge5BTp.v22p1fQJ3bfuqUgZ1DfwA4CGJ3xs27X57HwROo')
