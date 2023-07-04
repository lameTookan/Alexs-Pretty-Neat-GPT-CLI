# GPTChat Documentation

The `GPTChat` class is designed to provide an abstraction for interacting with the OpenAI API to chat with a language model. It simplifies the process of making API calls and handling the responses.

## Attributes

### `possible_return_types`

A set of possible return types for the chat. Available options are:

- `"string"`
- `"json"`
- `"dict"`
- `"Message"`

### `return_type`

The return type of the chat. This attribute determines the format in which the response will be returned. It should be set to one of the possible return types mentioned above.

### Essential Attributes

- `model_name`: The name of the model to use for completion. Please refer to the OpenAI API documentation for a list of available models.
- `API_key`: The API key to use for the OpenAI API. If you don't have an API key, you won't be able to make API calls.

### OpenAI Completion Parameters

These attributes define the parameters for the OpenAI completion requests. These parameters can be modified to control the behavior and output of the language model.

- `temperature`: A float value between 0 and 2. Higher values (e.g., 1.5) result in more random and creative output, while lower values (e.g., 0.5) make the output more deterministic and focused.
- `top_p`: An alternative to temperature, this parameter selects the highest probability tokens until the cumulative probability reaches the specified value. It is specified as a float between 0 and 1.
- `max_tokens`: The maximum number of tokens to generate in the completion. It should be an integer value between 1 and the model's maximum tokens limit.
- `frequency_penalty`: A float value between 0 and 2 that penalizes new tokens based on their frequency in the generated text so far. Higher values (e.g., 1.2) discourage repeating the same tokens.
- `presence_penalty`: A float value between 0 and 2 that penalizes new tokens based on their existing frequency in the text so far. Higher values (e.g., 1.2) discourage using tokens that have already been used.

## Methods

### Setter and Getter Methods

- `temperature`: Setter and getter methods for the `temperature` attribute.
- `model_name`: Setter and getter methods for the `model_name` attribute.
- `max_tokens`: Setter and getter methods for the `max_tokens` attribute.
- `top_p`: Setter and getter methods for the `top_p` attribute.
- `frequency_penalty`: Setter and getter methods for the `frequency_penalty` attribute.
- `presence_penalty`: Setter and getter methods for the `presence_penalty` attribute.
- `return_type`: Setter and getter methods for the `return_type` attribute.

### `_format_return(self, response: dict)`

This method formats the response from the OpenAI API based on the `return_type` attribute. It returns the formatted response as a string, JSON, dictionary, or a `Message` object.

### `modify_params(self, params: dict)`

This method allows modifying the model parameters by providing a dictionary with the parameter names as keys and the new values as values. Only the specified parameters will be modified, and any parameters not included in the dictionary will remain unchanged.

### `get_params(self)`

This method returns the current model parameters as a dictionary.

### `make_api_call(self, messages: list | ChatLog)`

This method makes an API call to the OpenAI API with the provided `messages`. The `messages` argument can be a list of dictionaries representing messages or a `ChatLog` object. It returns the API response in the format specified by the `return_type` attribute.

### `make_save_dict(self)`

This method returns a dictionary that contains all the necessary information to recreate the `GPTChat` object. It can be used to save the model and reload it later.

### `_verify_save_dict(self, save_dict: dict)`

This method verifies the integrity of a save dictionary. It checks if all the required keys are present and valid.

### `load_save_dict(self, save_dict: dict)`

This method loads the attributes of the `GPTChat` object from a save dictionary. It raises an error if the save dictionary is invalid or missing any required keys.

Please note that this documentation is a high-level overview of the `GPTChat` class. For detailed implementation and usage examples, please refer to the source code or provided documentation.

## Notes

  -If you would like to modify other parameters, you can modify the .make_api_call() method directly. There are others, but they are beyond the scope of this project
    - ie this doesn't support the stream parameter, only one response is returned at a time, and logit_bias is not supported

- should be fairly easy to add support for these parameters, if you want to. Add a setter and getter for the parameter, and then modify the make_api_call method to include the parameter the same as the other parameters
- also, if you want to add support for the stream parameter, you would need to do some serious refactoring of the make_api_call method, as it would need to be able to handle multiple responses at once, as well as the ChatLog class, and the menu system.
  - Honestly would probably recommend starting from scratch if you want to add support for the stream parameter, I am not yet familiar enough with server events to do it myself yet
  - this isn't called Intermediate Chatbot for nothing!
