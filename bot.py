import discord
import aiohttp
import json
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


with open("opts.json", "r") as f:
    TOKEN: str = json.load(f)["token"]

URL: str = "https://www.oref.org.il/WarningMessages/History/AlertsHistory.json"


@bot.event
async def on_ready():
    print("Bot is up and ready!")
    print(f"Logged in as {bot.user.name}")

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


@bot.tree.command(name="countalerts")
@app_commands.describe()
async def countalerts(
    intrection: discord.Interaction,
):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(URL) as response:
                response.raise_for_status()
                json_data = await response.json()
                line_count = len(json_data)

        output = f"Israel Had: {line_count} In the past 24 Hours!"

    except aiohttp.ClientError as e:
        output = f"Error fetching the JSON data: {e}"

    except ValueError as e:
        output = f"Error parsing the JSON data: {e}"
    except Exception as e:
        print(e)
        output = e

    embed = discord.Embed(
        title="Alerts",
        description=output,
        color=discord.Colour.blue(),
    )

    embed.set_footer(text=f"Developed By Hatol, MrCatNerd & Pikud horef | Red Alerts")

    await intrection.response.send_message(embed=embed)


bot.run(TOKEN)
