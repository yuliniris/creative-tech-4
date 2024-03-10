import os
import discord
import requests
from discord.ui import View, Modal, TextInput, Button
from TextGeneration import generateText


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
      await interaction.response.send_modal(FeedbackModal())
      # await interaction.response.defer()
  

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

class FeedbackModal(Modal):
      def __init__(self):
        super().__init__(title="Generate Text Prompt")
        self.start = TextInput(label="what woud you like to say?")
        self.model = TextInput(label = "model is model")
        self.key = TextInput(label="key is three")
        self.maxLen = TextInput(label="maximum lenght")

        self.add_item(self.start)
        self.add_item(self.model)
        self.add_item(self.key)
        self.add_item(self.maxLen)
        # self.submit_button = Button(label = "Generate")
        # self.add_item(self.submit_button)

      async def callback(self, interaction):
        startText = self.start.value
        model = self.model.value
        key = self.key.value
        maxLen = self.maxLen.value

        GeneratedText = generateText(startText, model, key, maxLen)

        await interaction.response.send_message(GeneratedText)

        await interaction.message.delete()
        
# intents = discord.Intents.default()
# intents.message_content = True

# client = discord.Client(intents=intents)
        

my_secret = os.getenv('DISCORD_BOT_SECRET')
client.run(my_secret)