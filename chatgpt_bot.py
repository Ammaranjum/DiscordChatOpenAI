import os
from dotenv import load_dotenv
from openai import AzureOpenAI
import discord
from discord.ext import commands
import json
import asyncio

# Load environment variables
load_dotenv()

# Set up intents
intents = discord.Intents.default()
intents.message_content = True

# Environment variables
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION", "2023-05-15")  # Use a default value

# Set up Azure OpenAI client
client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version=OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)

class ChatGPTBot(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.pre_prompt = "You are a discord bot chat bot. There are lots of people in the server; don't assume everyone is talking to you, especially if they don't address you directly!"
        self.pre_pre_prompt = ""

    async def set_pre_prompt(self, pre_prompt):
        self.pre_pre_prompt = pre_prompt
        await self.change_presence(activity=discord.Game(name=self.pre_pre_prompt))

    async def art(self, art_prompt, message):
        try:
            response = client.images.generate(
                model="dall-e-3",  # Adjust based on your Azure OpenAI setup
                prompt=art_prompt,
                n=1,
                size="1024x1024"
            )
            image_url = response.data[0].url
            await message.channel.send(image_url)
        except Exception as e:
            await message.channel.send(f"An error occurred while generating the image: {str(e)}")

    async def on_message(self, message):
        if message.author == self.user:
            return

        channel = message.channel
        message_history = []
        async for previous_message in channel.history(limit=5):
            if previous_message.content == "context block":
                break
            role = "assistant" if previous_message.author == self.user else "user"
            content = previous_message.content if role == "assistant" else f"{previous_message.author} said {previous_message.content}"
            message_history.append({"role": role, "content": content})

        message_history.reverse()
        if self.pre_pre_prompt:
            message_history.append({"role": "system", "content": self.pre_pre_prompt})
        message_history.append({"role": "system", "content": self.pre_prompt})

        try:
            should_talk_response = client.chat.completions.create(
                model="gpt-4",  # Adjust based on your Azure OpenAI setup
                messages=message_history,
                functions=[{
                    "name": "should_i_talk",
                    "description": "Determine if the bot should respond based on recent messages",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "answer": {
                                "type": "string",
                                "enum": ["yes", "no"],
                                "description": "Whether the bot should respond",
                            },
                        },
                        "required": ["answer"],
                    },
                }],
                function_call={"name": "should_i_talk"}
            )

            should_talk = json.loads(should_talk_response.choices[0].message.function_call.arguments).get("answer")

            if should_talk == "yes":
                response = client.chat.completions.create(
                    model="gpt-4",  # Adjust based on your Azure OpenAI setup
                    messages=message_history,
                    functions=[
                        {
                            "name": "set_pre_prompt",
                            "description": "Sets the bot's pre-prompt",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "new_pre_prompt": {
                                        "type": "string",
                                        "description": "The new pre-prompt",
                                    },
                                },
                                "required": ["new_pre_prompt"],
                            },
                        },
                        {
                            "name": "art",
                            "description": "Generates an image with a prompt",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "art_prompt": {
                                        "type": "string",
                                        "description": "Prompt to generate art with",
                                    },
                                },
                                "required": ["art_prompt"],
                            },
                        }
                    ],
                    function_call="auto"
                )

                response_message = response.choices[0].message

                if response_message.function_call:
                    function_name = response_message.function_call.name
                    function_args = json.loads(response_message.function_call.arguments)
                    
                    if function_name == "set_pre_prompt":
                        await self.set_pre_prompt(function_args.get("new_pre_prompt"))
                    elif function_name == "art":
                        await self.art(function_args.get("art_prompt"), message)
                else:
                    await message.channel.send(response_message.content)
        
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            await message.channel.send("I encountered an error while processing your message. Please try again later.")

async def main():
    bot = ChatGPTBot(command_prefix="!", intents=intents)
    async with bot:
        await bot.start(DISCORD_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())