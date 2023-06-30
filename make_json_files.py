import json

# this is a random file used to quickly generate json files from a dict.
# paste whatever dictionary you want to use to make json file here

templates = {
    "gpt-4_default": {
        "chat_log": {
            "model": "gpt-4",
            "max_model_tokens": 8000,
            "max_completion_tokens": 1000,
            "max_chat_messages": 1000,
            "token_padding": 500,
        },
        "gpt_chat": {
            "model_name": "gpt-4",
            "max_tokens": 1000,
            "temperature": 1.1,
            "top_p": 1.0,
            "frequency_penalty": 0.5,
        },
        "description": "Default settings for gpt-4",
        "tags": ["gpt-4", "default", "normal"],
    },
    "gpt-4_small": {
        "chat_log": {
            "model": "gpt-4",
            "max_model_tokens": 8000,
            "max_completion_tokens": 1000,
            "max_chat_messages": 50,
            "token_padding": 500,
        },
        "gpt_chat": {
            "model_name": "gpt-4",
            "max_tokens": 1000,
            "temperature": 0.5,
            "top_p": 1.0,
        },
        "description": "To save money on tokens use this to limit the number of messages to 50",
        "tags": ["gpt-4", "small", "cheap", "low-cost"],
    },
    "gpt-4_creative": {
        "chat_log": {
            "model": "gpt-4",
            "max_model_tokens": 8000,
            "max_completion_tokens": 1000,
            "max_chat_messages": 1000,
            "token_padding": 500,
        },
        "gpt_chat": {
            "model_name": "gpt-4",
            "max_tokens": 1000,
            "temperature": 1.5,
        },
        "description": "Use this to get more creative responses, higher temperature means more creative",
        "tags": ["gpt-4", "creative", "high-temperature"],
    },
    "gpt-3_16K_default": {
        "chat_log": {
            "model": "gpt-3",
            "max_model_tokens": 16000,
            "max_completion_tokens": 2000,
            "max_chat_messages": 2000,
            "token_padding": 500,
        },
        "gpt_chat": {
            "model_name": "gpt-3-16K",
            "max_tokens": 2000,
            "temperature": 0.5,
        },
        "description": "Default settings for gpt-3-16K",
        "tags": ["gpt-3-16K", "default", "normal", "gpt-3"],
    },
}
# paste the variable name of the dictionary here
dict = templates

# name of the file you want to create
# caution: this will overwrite any file with the same name
# be sure to include the .json extension
name = "templates.json"

with open(name, "w") as outfile:
    json.dump(dict, outfile, indent=4, sort_keys=True)

print("done")
