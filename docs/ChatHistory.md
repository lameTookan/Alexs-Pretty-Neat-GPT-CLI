# Comprehensive Guide to Chat History

# ChatLog Class

This class is used for managing and preparing a chat log for use with the OpenAI API.

## Attributes

### Token Information Attributes

- `max_model_tokens (int)`: The maximum number of tokens allowed for the model.
- `max_completion_tokens (int)`: The maximum number of tokens allowed for the completion.
- `token_padding (int)`: To subtract from the `max_model_tokens` to allow for the completion.
- `max_chat_tokens (int)`: The maximum number of tokens allowed for the chat log, worked out from the token information attributes in `.work_out_tokens()`.

### Chat Log Attributes

- `max_chat_messages (int)`: The maximum number of messages allowed in the chat log.
- `_sys_prompt (str)`: The system prompt, must be added via setter properties before use.
- `model (str)`: The model used to encode the messages, for use in counting tokens.
- `full_chat_log (list)`: The full chat log, containing Message objects.
- `trimmed_chat_log (deque)`: The trimmed chat log, containing Message objects, trimmed to the `max_chat_messages` and `max_chat_tokens`.
- `trimmed_chat_log_tokens (int)`: The number of tokens in the trimmed chat log, for use in the trimming process.
- `trimmed_messages (int)`: The number of messages in the trimmed chat log, for use in the trimming process.
- `is_loaded (bool)`: Whether the chat log has been loaded from a file or not.

## Methods

### General Methods

- `_check_wildcards`: Checks if wildcards are valid, for use in the wildcard system.
- `set_token_info`: Sets the token information attributes, allowing for easy changing of the token information after construction.
- `work_out_tokens`: Works out the maximum number of tokens allowed for the chat log, based on the token information attributes, and sets it to `max_chat_tokens`.
- `setup(self)`: For convenience, runs `work_out_tokens` and sets the system prompt. If you set the token information or system prompt after construction, you must run this method before using the chat log.
- `system_prompt` getter: Returns the `_sys_prompt`, or raises `NoSystemPromptError` if it is None. Also adds wildcards to the system prompt.
- `system_prompt` setter: Sets the `_sys_prompt`. Must be used before the chat log is used.
- `_check_sys_prompt`: Checks if the system prompt is set, and if it is valid.
- `add_more_wildcards`: Adds more wildcards to the wildcard system.
- `_add_wildcards`: Adds wildcards to a string, replacing placeholders with the values of the wildcards.

### Methods for Trimming Process and Core Functionality

- `work_out_tokens`: Works out the maximum number of tokens allowed for the chat log, based on the token information attributes, and sets it to `max_chat_tokens`.
- `trim_chat_log`: Trims the chat log to the maximum number of tokens and messages allowed.
- `get_finished_chat_log`: Returns the trimmed chat log as a list of dictionaries, for use with the OpenAI API.
- `finished_chat_log(self)`: Getter property for `get_finished_chat_log` for convenience.

### Methods for Adding Messages

- `make_message`: Makes a Message object from a role and content, or a dictionary containing the role and content.
- `add_message_obj`: Core method for adding messages to the chat log, accepts Message objects.
- `add_message`: Takes a role and content, or message dict, turns it into a Message object, and adds it to the chat log using `add_message_obj`.
- `add_message_list (list)`: Takes a list of message dicts, converts them to Message objects, and adds them to the chat log using `add_message_obj`.
- `user_message(self)`: Getter property for the user message, for convenience, returns the last message in the chat log with the role 'user' as a Message object.
- `user_message(self, message)`: Setter property for the user message, for convenience, takes a string or Message object, converts it to a Message object, and adds it to the chat log using `add_message_obj`.
- `assistant_message(self)`: Getter property for the assistant message, for convenience, returns the last message in the chat log with the role 'assistant' as a Message object.
- `assistant_message(self, message)`: Setter property for the assistant message, for convenience, takes a string or Message object, converts it to a Message object, and adds it to the chat log using `add_message_obj`.

### Methods for Retrieving Messages

- `get_messages(role = None, limit = None, reverse = True)`: Generator Returns the chat log as a list of Message objects, with the option to filter by role, limit the number of messages returned, and reverse the order of the messages.
- `get_messages_as_list(role = None, limit = None, reverse = True, format = "Message")`: Returns the chat log as a list. Format can be:
  - "Message" : Message objects
  - "dict": Message objects as dictionaries
  - "string": Content of the messages as strings
  - "pretty" for a pretty printed string, using the Message.pretty() method.
- `get_pretty_messages(role = None, limit = None, reverse = True)`: Returns the chat log as a pretty printed string, using the `Message.pretty()` method, with the option to filter by role, limit the number of messages returned, and reverse the order of the messages. Format will be pretty strings separated by newlines.

### Methods for Saving the Chat Log

- `save(file_name)`: Saves the chat log to a file, using the `SaveToFile` class as well as the `SaveToDict` class.
- `load(file_name)`: Loads the chat log from a file, using the `SaveToFile` class as well as the `SaveToDict` class.

## Subclasses

- `SaveToDict`: A class for saving and loading the class to a dictionary, as well as verifying the dictionary.
- `SaveToFile`: A class for saving and loading the class to a file, using the `SaveToDict` class, as well as managing the file system.

## Usage

1. Create a `ChatLog` object, setting the token information attributes, and optionally the `max_chat_messages` attribute.
2. Set the system prompt using the `system_prompt` setter property.
3. Add messages to the chat log using the `add_message` method, or more easily using the `user_message` and `assistant_message` setter properties.
4. Send off the finished chat log to the OpenAI API.
5. Set the response as the assistant message using the `assistant_message` setter property.
6. Repeat steps 3-5 until you are done.
7. Save the chat log to a file using the `save` method.
8. Load the chat log from a file using the `load` method.
9. When loading, check the `is_loaded` attribute to see if the chat log was loaded successfully and if the history should be printed to user.

## Dependencies

- `Message` class
- `Tiktoken` module
- `BadMessageError`
- `NoSystemPromptError`
- `NoTokenInfoError`
- `BadSaveDictError`
