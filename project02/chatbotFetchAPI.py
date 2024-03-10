import os
import discord
import requests
from discord.ui import View, Modal, TextInput, Select


cocktail_url = "http://www.thecocktaildb.com/api/json/v1/1/search.php?s=margarita"


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

class AnotherView(View):
    def __init__(self):
        super().__init__()

    async def fetch_cocktail_data(self):
        response = requests.get(cocktail_url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print("Failed to fetch cocktail data:", response.status_code)
            return None

    @discord.ui.button(label="Any questions?", style=discord.ButtonStyle.blurple)
    async def button_callback(self, interaction, button):
        await interaction.response.send_message("How is it going?")

    @discord.ui.button(label="Continue", style=discord.ButtonStyle.green)
    async def buttonCallback2(self, interaction, button):
         await interaction.channel.send("New Messages are here.")
         await interaction.response.defer()


    @discord.ui.button(label="Have a break")
    async def button_callback02(self,interaction, button):
        
        data = await self.fetch_cocktail_data()
        if data:
                drink = data.get("drinks", [])[0]
                if drink:
                     dr_name = drink["strDrink"]
                     dr_img = drink["strDrinkThumb"]

                     await interaction.response.send_message(f"{dr_name}\n{dr_img}")
                
                else:
                    await interaction.response.send_message("Would you like any drinks?")
                  


@client.event
async def on_ready():
  print("Bot is ready")


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if client.user in message.mentions:
    ourview = AnotherView()
    await message.channel.send("Thanks to mentioning me~")

  if message.content.startswith("would you like to have a chat?"):
    ourview = AnotherView()
    await message.channel.send("Sure! ", view=ourview)


from discord.ui import Modal, TextInput

class chatcontinue(Modal, title = 'Other topics to talk about'):
  name = TextInput(label = 'Name')
  answer = TextInput(label = 'response', style = discord.TextInput.paragraph)

  async def on_submit(self, interaction: discord.Interaction):
    await interaction.response.send_message(f'new topics : {self.answer}', ephemeral = True)

my_secret = os.getenv('DISCORD_BOT_SECRET')
client.run(my_secret)