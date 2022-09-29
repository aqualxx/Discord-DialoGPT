# Discord DialoGPT ChatBot

Welcome to my personal DialoGPT chatbot!

## How to use

Run `./build.bat` to install necessary dependencies.

### Using The Console Bot

1. Run `./console.bat`.
2. Enjoy!

### Using The Discord Bot

1. Run `python ./main.py --token=(discord bot token)`.
2. Enjoy!

## Parameters (Global)

### `--model`

- What model to use. Default is DialoGPT, set to a valid huggingface model from <https://huggingface.co/models> to use a custom model.
- Include --local to use a local model instead.

### `--temperature`

- Use temperature to decrease the chance of low probability candidates.
- As the temperature approches zero, sentences will be less random but more repetitive.
- The default value is 0.8. Set to a decimal between 0 - 1.
- <https://huggingface.co/blog/how-to-generate>

### `--top-k`

- Sets Top-K. The default value is 40. Set to an integer.
- <https://docs.cohere.ai/token-picking/>

### `--top-p`

- Sets Top-P. The default value is 0.9. Set to a decimal between 0 - 1.
- <https://docs.cohere.ai/token-picking/>

### `--max_history`

- How many messages do you want the bot to remember concurrently?
- Smaller values of max_history will remove chat context.
- The default value is 4. Set to an integer.

## Parameters (Discord)

### `--token`

- Your Discord bot's token.
- Required when using a Discord bot.

### `--response_chance`

- The chance to respond to a message.
- Setting to 0 disables this.
- The default value is 0. Set to a decimal between 0 - 1.

### `--reply`

- Whether or not to reply to a message.
- Doesn't ping the user.
- Setting to 0 disables this.
- The default value is 0. Set to the integer 0 or 1.

### `--whitelist`

- Whitelists a channel ID so the bot will speak in it.

## Parameters (console)

### `--bots`

- Set value to 2 to have two chatbots talking to each other.
- Set value to 1 to make an input to the chatbot.
