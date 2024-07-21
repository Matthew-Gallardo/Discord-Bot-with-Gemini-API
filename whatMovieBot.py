import discord
from dotenv import load_dotenv
import os
import pathlib
import textwrap
import google.generativeai as genai
from IPython.display import display, Markdown

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

load_dotenv()

geminikey= os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=geminikey)

model = genai.GenerativeModel('gemini-1.5-flash')



class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        if message.content.startswith('!suggest_movie'):
            parts = message.content.split(' ', 1)
            if len(parts) > 1:
                genre = parts[1].strip()
                
                prompt = f"Suggest 1 movie based on this genre: {genre}. Just give the title of the movie and the year. Simple as that"
                response = model.generate_content(prompt)
                movie_suggestion = response.text
                
                await message.channel.send(movie_suggestion)
            else:
                await message.channel.send("Please specify a genre after the command. Usage: `!suggest_movie <genre>`")

intents = discord.Intents.default()
intents.message_content = True

discordKey = os.getenv('DISCORD_TOKEN')
client = MyClient(intents=intents)
client.run(discordKey)
