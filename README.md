# Discord Bot with Azure OpenAI Integration

This project implements a Discord bot that uses Azure OpenAI services to generate responses and create images based on user interactions.

## Features

- Responds to user messages using Azure OpenAI's language models
- Generates images based on text prompts
- Dynamically adjusts its behavior based on conversation context
- Allows setting a custom pre-prompt to guide the bot's responses

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7 or higher
- An Azure account with an active subscription
- Access to Azure OpenAI services (currently limited and requires approval)
- A Discord account and a registered Discord application/bot

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/Ammaranjum/DiscordChatOpenAI.git
   cd DISCORD_CHATBOT
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install python-dotenv openai discord.py
   ```

## Configuration

1. Create a `.env` file in the root directory of the project.

2. Add the following environment variables to the `.env` file:
   ```
   AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
   DISCORD_TOKEN=your_discord_bot_token_here
   AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
   OPENAI_API_VERSION=2023-05-15
   ```

   Replace the placeholder values with your actual Azure OpenAI API key, Discord bot token, and Azure OpenAI endpoint.

3. Ensure your Azure OpenAI service has the necessary models deployed (e.g., GPT-4 for text generation, DALL-E for image generation).

## Usage

To start the bot, run:

```
python chatgpt_bot.py
```

The bot will now be online and ready to respond to messages in your Discord server.

## Commands

The bot doesn't use traditional command prefixes. Instead, it analyzes the conversation context to determine when and how to respond. You can interact with it in the following ways:

- Ask questions or make statements in the Discord channel where the bot is present.
- Request image generation by asking the bot to create or draw something.
- Set a new pre-prompt by asking the bot to change its behavior or role.

## Customization

You can customize the bot's behavior by modifying the `pre_prompt` and `pre_pre_prompt` variables in the `ChatGPTBot` class.

## Troubleshooting

If you encounter any issues:

1. Ensure all environment variables are correctly set in the `.env` file.
2. Check that your Azure OpenAI service is properly set up and the endpoint is correct.
3. Verify that your Discord bot token is valid and the bot has the necessary permissions in your server.
4. Check the console output for any error messages when running the bot.

## Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE.md](LICENSE) file for details.


## Contact

If you have any questions or feedback, please open an issue in this repository.
