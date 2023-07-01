# GPT Template Guide

The `GPTTemplateManager` class uses templates to set up `ChatLog` and `GPTChat` objects. Each template should be a dictionary item, with the key being the name of the template. The value should be another dictionary containing the following keys:

- `chat_log`
- `gpt_chat`
- `description`
- `tags`

Below is a sample template named `gpt-4_default`:

```json
"gpt-4_default": {
    "chat_log": {
        "model": "gpt-4",
        "max_model_tokens": 8000,
        "max_completion_tokens": 1000,
        "max_chat_messages": 1000,
        "token_padding": 500
    },
    "gpt_chat": {
        "model_name": "gpt-4",
        "max_tokens": 1000,
        "temperature": 1.1,
        "top_p": 1.0,
        "frequency_penalty": 0.5
    },
    "description": "Default settings for gpt-4",
    "tags": ["gpt-4", "default", "normal"]
}
```

## Template Keys

Each template key has a specific role:

- `chat_log`: Contains parameters for the `ChatLog` object. The `chat_log` dictionary can have the following keys: `model`, `max_model_tokens`, `max_completion_tokens`, `max_chat_messages`, `token_padding`. All these keys are optional since `ChatLog` has default values for them. However, it's a good practice to at least include the `model` to prevent unexpected behavior.
- `gpt_chat`: Contains parameters for the `GPTChat` object. The `gpt_chat` dictionary can have the following keys: `model_name`, `max_tokens`, `temperature`, `top_p`, `frequency_penalty`, `presence_penalty`. All these keys are optional, but the `GPTChat` object is designed to exclude any `None` values. It's recommended to at least include `model_name` to ensure correct behavior.
- `description`: A string describing the template. Even if it's empty, it must be included to prevent errors.
- `tags`: A list of tags for the template. Even if the list is empty, it must be included to prevent errors.

Note: In `chat_log`, the `model` refers to the model used, and in `gpt_chat`, `model_name` refers to the model used. These are essentially the same, so be careful not to confuse them.

Please make sure your templates follow the correct format as described above. Otherwise, a `BadTemplateError` will be thrown.

This setup allows for flexibility and easy modification of the settings for the `ChatLog` and `GPTChat` objects while maintaining clear and concise code. Happy coding!
