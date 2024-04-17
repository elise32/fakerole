import os
from dotenv import load_dotenv
from discord.ext import commands
from discord import Intents, Message, Interaction

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents: Intents = Intents.default()

client: commands.Bot = commands.Bot(command_prefix='!@#$%^&*()_+', intents=intents)

@client.tree.command(name='ping', description='Sends pong')
async def ping(interaction: Interaction) -> None:
    await interaction.response.send_message(content=f'Pong! {round(client.latency*1000)} ms', ephemeral=True)

def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()
