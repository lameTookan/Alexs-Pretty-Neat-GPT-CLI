# Alex's Pretty Neat GPT CLI Chatbot

## Features

- Save and load chat logs from a file

- Set up chats using templates that configure all settings for the chat
- Never worry about getting a token error again! This program will automatically count tokens and trim off messages so that it always fits within the token limit.
- Configure model parameters such as temperature, top_p, frequency_penalty, and presence_penalty on the fly!
  - These are also included in chat log saves!
  - Robust error handling for invalid values
- Save and load system prompts and change them in the middle of a chat! These will be saved to the chat log file as well!
- Import messages from text files, using the from_file command and the respective folder name.
- Export chat logs to text files.

## Setup

If you have never set up a python project before, please see docs/HELP_ME.md for a more comprehensive guide.

1. Install the requirements

    ```bash
    pip install -r requirements.txt
    ```

2. Get an API key from platform.openai.com
3. Replace the API key in the .env.example file with your API key
    - If you do not have gpt-4 access, you can use gpt-3 instead, just be sure to set gpt-3 as the default model and gpt-3_default as the default template
4. Rename the .env.example file to .env
5. Run the program

    ```bash
    python main.py
    ```

## Usage

- Run main.py
- Read the on screen instructions
  - Type chat to start chatting with the default template(specified in the .env file)
  - Type template to see a list of available templates, and choose one before starting the chat
  - Type help to see a list of commands
    - Type "sys" to customize system prompts, as well as managing the text files that they are stored in
      - Note that you can easily add new system prompts by adding a new text file to the system_prompts folder. There are two wildcards that you can use: {model}, and {date}. These will be replaced with the current model and date respectively.
      - Wildcards will only be replaced if they are in the first 4K characters of the prompt. Your system prompt can be longer, but only wildcards in the first 4K characters will used
  - In the chat loop type 'help' to see a list of all commands
    - from_file -> read the from_file/default.txt and send it as a message(won't work if the file is longer than the max token length)
    - p -> modify the model's parameters, on the fly!
    - export -> enter the chat log export menu(only works on saved chats)
  - If there's an API error, the program will attempt to send it over two more times. If this still doesn't work, an emergency chatlog save will be created and the program will exit and the error message will be displayed.

## I found a bug

- If you are a dev using the code base, you should only ever see my custom exceptions. If you see a normal python exception, please open up an issue and include the traceback.
- If you encounter an error in the chat loop, please use the `debug` command and send me the output. This is also a good way to get information about the current state of the program if you are having issues or are just curious.
- If you are a user, you should never see a traceback. If you do, please open up an issue and include the traceback, especially if its a DevMessedUpError.
- If something doesn't work as expected, please open up an issue and include the traceback, if there is one.

## About this project

See my dev log in the docs folder for more information about the development of this project. Essentially I am a beginner dev, and ths project was meant to be a sort of mid term for myself. Its not perfect by any means, but I did learn a ton. I hope you enjoy it!

## Contributing

- If you have any suggestions, feel free to open up an issue or a pull request!
- If you want to add a new template, check out the template_documentation.md file in the docs folder.
- Any thoughts/feedback on how to improve the code are welcome as well!
- The code is a bit messy in some places(see the dev log for more info), so if you want to help clean it up, that would be great!
- The license is MIT, so feel free to fork this project and do whatever you want with it!
