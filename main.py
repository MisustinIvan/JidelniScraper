# MORTY, MORTY, I TURNED MYSELF INTO A PICKLE! PICKLE RICK!
#import pickle
import time
import asyncio
import lunch_scraper
import bakalari_scraper
import discord
from discord import app_commands
from discord.ext import tasks

# create the scraper and scrape the lunches
site_url = "https://www.strava.cz/strava5/Jidelnicky?zarizeni=0253"
ObedScraper = lunch_scraper.lunchScraper(site_url)


username_file = open("./username")
username = username_file.read()
username_file.close()

password_file = open("./password")
password = password_file.read()
password_file.close()


web_app_url: str = "https://bakalari.gymta.cz/"
BakScraper = bakalari_scraper.bakalariScraper(web_app_url, username, password)

# set the bot intents
intents = discord.Intents.default()
intents.message_content = True

# initialize the bot
bot = discord.Client(command_prefix='/', intents=intents)
tree = app_commands.CommandTree(bot)

@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')
    await tree.sync(guild=discord.Object(id=1093125706743021669))
    print("======================================")
    # start the backgroundTask
    backgroundTask.start()

@tree.command(name="obed", description="Oběd [den] dnů od dneška. Počítají se jen dny, ve které je oběd(ne víkendy/státní svátky)", guild=discord.Object(id=1093125706743021669))
async def obed_command(interaction, den: int):
    print(f'giving lunch info to {interaction.user}')
    await interaction.response.send_message(f"Datum: {ObedScraper.lunches[den].date}\nPolévka: {ObedScraper.lunches[den].soup}\nJídlo: {ObedScraper.lunches[den].lunch}", ephemeral=True)

@tree.command(name="rozvrh", description="Rozvrh na [den :: 1 <-> 5] v týdnu.", guild=discord.Object(id=1093125706743021669))
async def timetable_command(interaction, den: int):
    print(f"giving timetable info to {interaction.user}")
    await interaction.response.send_message(f"{BakScraper.getTimetableForDay(den-1)}", ephemeral=True)

@tree.command(name="pomoc", description="Prints the help info.", guild=discord.Object(id=1093125706743021669))
async def help_command(interaction):
    print(f"givint help info to {interaction.user}")
    await interaction.response.send_message(f"""
**<Jídelníček Bot>**
**->  Příkazy**
**-->  /obed [den]** -> Vyhodí informace o obědu [den] dnů od dneška([den] = 0 => dnes).
**-->  /rozvrh [den]** -> Vyhodí rozvrh pro třídu uživatele pro [den] v týdnu.
**-->  /pomoc** -> Vyhodí tento výstup.
""", ephemeral=True)

@tasks.loop(seconds=10)
async def backgroundTask():
    pass
#    channel = bot.get_channel(1093130555836608653)
#    await channel.send("Ligma")

def main():
    # get the token from the hidden file
    token_file = open("./bot_token")
    token = token_file.read()
    token_file.close()

    # run the bot
    bot.run(token)

if __name__ == "__main__":
    main()
