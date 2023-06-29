import ChatHistory as ch
import openai
import os
import json
from object_factory import templates
# import super_secret
from typing import List, Dict, Union, Any, Optional
import uuid
import datetime
import time

# API_KEY = super_secret.OPENAI_API_KEY

from ChatHistory import ChatLog


class BadModelParametersError(Exception):
    pass


class BadChatLogParametersError(Exception):
    pass

    def set_model_parameters(self, params: dict):
        self._check_completion_params(params)
        self._model_parameters = params

    def set_model(self, model: str):
        self.model = model

    def set_return_type(self, return_type: str):
        self.return_type = self._check_return_type(return_type)


class BadReturnTypeError(Exception):
    possible_return_types = {
        "dict": "Returns a dictionary with the following keys: role(str), and content(str)",
        "json": "Returns a json string with the following keys: role(str), and content(str)",
        "string": "Returns a string with the content of the message",
        "Message": "Returns a Message object(see ChatHistory.py for more info)",
    }

    def __init__(self, msg: str = None, return_type: str = None):
        if msg is None:
            msg = "Bad return type"
        if return_type is not None:
            msg += f"\n{return_type} is not a valid return type"
            msg += "\nPossible return types are:"
            for key, value in self.possible_return_types.items():
                msg += f"\n{key}: {value}"
        self.msg = msg
        super().__init__(self.msg)


class BadChatCompletionParams(Exception):
    good_params = {
        "model": "The model to use for completion, check out openai api for more info",
        "temperature": "The higher the temperature, the crazier the text float between 0 and 2",
        "max_tokens": "The maximum number of tokens to generate int between 1 and the model's max tokens",
        "top_p": "An alternative to sampling with temperature, selects the highest probability tokens whose cumulative probability exceeds the specified value float between 0 and 1",
        "frequency_penalty": "Float between 0 and 2 that penalizes new tokens based on whether they appear in the text so far",
        "presence_penalty": "Float between 0 and 2 that penalizes new tokens based on their existing frequency in the text so far",
    }

    def __init__(self, msg: str = None, bad_param: dict = None, good_value: str = None):
        if msg is None:
            msg = "Bad chat completion parameter(s)"
        if bad_param is not None:
            if not isinstance(bad_param, dict):
                raise TypeError(f"Bad param must be a dict, not {type(bad_param)}")
            param_name = list(bad_param.keys())[0]
            param_value = list(bad_param.values())[0]
            good_value = self.good_params[param_name]
            msg += f"\n{param_name} cannot be {param_value}"
            msg += f"More info: {good_value}"
        self.msg = msg

    def __str__(self):
        return self.msg


def BadGPTChatDictError(Exception):
    pass

def try_converting_to_datatype(value: any, datatype: type) -> any | False:
    """Converts a value to a datatype, returns False if it fails"""
    try:
        return datatype(value)
    except ValueError:
        return False
class GPTChat:
    """
    A class that abstracts away using the openai api to chat with a model
    Attributes:
        possible_return_types: A set of possible return types
        return_type: The return type of the chat
        Essential Attributes:
            model_name: The model to use for completion, check out openai api for more info
            API_key: The API key to use for the openai api
        OpenAI Completion Parameters:
            temperature: The higher the temperature, the crazier the text float between 0 and 2
            top_p: An alternative to sampling with temperature, selects the highest probability tokens whose cumulative probability exceeds the specified value float between 0 and 1
            max_tokens : The maximum number of tokens to generate int between 1 and the model's max tokens
            Frequency Penalty: Float between 0 and 2 that penalizes new tokens based on whether they appear in the text so far
            Presence Penalty: Float between 0 and 2 that penalizes new tokens based on their existing frequency in the text so far
    Methods:
        setters and getters for all model parameters
        _format_return(self, response: dict) -> Union[str, dict, Message]: Formats the response from the openai api
        modify_params(self, params: dict) -> None: Modifies the model parameters
        get_params(self) -> dict: Returns the model parameters
        make_api_call(self, messages: list | ChatLog) -> Union[str, dict, Message]: Makes the api call to the openai api
        make_save_dict(self) -> dict: Makes a dictionary that can be used to save the model
        _verify_save_dict(self, save_dict: dict) -> None: Verifies that the save dict is valid
        load_save_dict(self, save_dict: dict) -> None: Loads object information from a save dict



    """

    possible_return_types = {
        "string",
        "json",
        "dict",
        "Message",
    }
    possible_optional_params = {
        "max_tokens",
        "temperature",
        "top_p",
        "frequency_penalty",
        "presence_penalty",
    }
    param_help = {
        "model": "The model to use for completion, check out openai api for more info",
        "temperature": "The higher the temperature, the crazier the text float between 0 and 2",
        "max_tokens": "The maximum number of tokens to generate int between 1 and the model's max tokens",
        "top_p": "An alternative to sampling with temperature, selects the highest probability tokens whose cumulative probability exceeds the specified value float between 0 and 1",
        "frequency_penalty": "Float between 0 and 2 that penalizes new tokens based on whether they appear in the text so far",
        "presence_penalty": "Float between 0 and 2 that penalizes new tokens based on their existing frequency in the text so far",
    }

    def __init__(
        self,
        API_KEY: str,
        return_type: str = "string",
        temperature: float = 1,
        model_name: str = "gpt-4",
        max_tokens: int = None,
        top_p: float = None,
        frequency_penalty: float = None,
        presence_penalty: float = None,
        template = None
    ):
        self.constructor_params = {
            "temperature": temperature,
            "model_name": model_name,
            "max_tokens": max_tokens,
            "API_KEY": API_KEY,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
            "return_type": return_type,
            "template": template
        }
        # for use in the ChatLogAndGPTChatFactory class
        self.template = template
        self.temperature = temperature
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.api_key = API_KEY
        self.return_type = return_type
    def reload_from_template(self, template_name: None | str = None) -> bool:
        if template_name is None:
            template = self.template
        if template_name is None:
            return False
        if template_name not in self.template:
            return False
        self.model_name = template['model_name']
        del template['model_name']
        try:
            self.modify_params(**template)
        except BadChatCompletionParams:
            return False
        except TypeError:
            return False
        return True
    def __repr__(self):
        constructor = (
            "GPTChat("
            + ", ".join(
                f"{key} = {value}" for key, value in self.constructor_params.items()
            )
            + ")"
        )
        model_params = "model_params = " + ", ".join(
            f"{key} = {value}" for key, value in self.get_params().items()
        )
        other_info = "id = " + str(id(self))
        return "\n".join([constructor, model_params, other_info])

    @property
    def temperature(self) -> float:
        return self._temperature

    @temperature.setter
    def temperature(self, value: float) -> None:
        if value is None:
            self._temperature = value
        value = try_converting_to_datatype(value, float)
        if value is False:
            raise BadChatCompletionParams(bad_param={"temperature": value}, msg="Temperature must be a float")
        elif not 0 <= value <= 2:
            raise BadChatCompletionParams(bad_param={"temperature": value})
        else:
            self._temperature = value

    @property
    def model_name(self) -> str:
        return self._model_name

    @model_name.setter
    def model_name(self, value: str) -> None:
        # If you have a specific list of models, you can check here
        self._model_name = value

    @property
    def max_tokens(self) -> int:
        return self._max_tokens

    @max_tokens.setter
    def max_tokens(self, value: int) -> None:
        if value is None:
            self._max_tokens = value
        value = try_converting_to_datatype(value, int)
        if value is False:
            raise BadChatCompletionParams(bad_param={"max_tokens": value}, msg="Max tokens must be an int")
        
        elif value < 1:
            raise BadChatCompletionParams(bad_param={"max_tokens": value})
        else:
            self._max_tokens = value

    @property
    def top_p(self) -> float:
        return self._top_p

    @top_p.setter
    def top_p(self, value: float) -> None:
        if value is None:
            self._top_p = value
        value = try_converting_to_datatype(value, float)
        if value is False:
            raise BadChatCompletionParams(bad_param={"top_p": value}, msg="Top p must be a float")
        elif not 0 <= value <= 1:
            raise BadChatCompletionParams(bad_param={"top_p": value})
        else:
            self._top_p = value

    @property
    def frequency_penalty(self) -> float:
        return self._frequency_penalty

    @frequency_penalty.setter
    def frequency_penalty(self, value: float) -> None:
        if value is None:
            self._frequency_penalty = value
        value = try_converting_to_datatype(value, float)
        if value is False:
            raise BadChatCompletionParams(bad_param={"frequency_penalty": value}, msg="Frequency penalty must be a float")
        elif not 0 <= value <= 2:
            raise BadChatCompletionParams(bad_param={"frequency_penalty": value})
        else:
            self._frequency_penalty = value

    @property
    def presence_penalty(self) -> float:
        return self._presence_penalty

    @presence_penalty.setter
    def presence_penalty(self, value: float) -> None:
        
        if value is None:
            self._presence_penalty = value
        value = try_converting_to_datatype(value, float)
        if value is False:
            raise BadChatCompletionParams(bad_param={"presence_penalty": value}, msg="Presence penalty must be a float")
        elif not 0 <= value <= 2:
            raise BadChatCompletionParams(bad_param={"presence_penalty": value})
        else:
            self._presence_penalty = value

    @property
    def return_type(self) -> str:
        return self._return_type

    @return_type.setter
    def return_type(self, value: str) -> None:
        if value not in self.possible_return_types:
            raise BadReturnTypeError(return_type=value)
        self._return_type = value

    def _format_return(
        self, message: openai.ChatCompletion
    ) -> Union[ch.Message, str, dict]:
        """Formats the return type based on the return_type attribute"""
        message_dict = message.choices[0].message
        if self.return_type == "string":
            return message_dict["content"]
        elif self.return_type == "json":
            return json.dumps(message_dict)
        elif self.return_type == "dict":
            return message_dict
        elif self.return_type == "Message":
            return ch.Message(model=self.model_name, **message_dict)
        else:
            raise BadReturnTypeError(return_type=self.return_type)

    def modify_params(
        self,
        temperature: float = None,
        model_name: str = None,
        max_tokens: int = None,
        top_p: float = None,
        frequency_penalty: float = None,
        presence_penalty: float = None,
    ) -> None:
        """Modifies the parameters of the GPTChat instance, convenience method"""
        if temperature is not None:
            self.temperature = temperature
        if model_name is not None:
            self.model_name = model_name
        if max_tokens is not None:
            self.max_tokens = max_tokens
        if top_p is not None:
            self.top_p = top_p
        if frequency_penalty is not None:
            self.frequency_penalty = frequency_penalty
        if presence_penalty is not None:
            self.presence_penalty = presence_penalty

    def get_params(self) -> dict:
        """Returns the parameters of the GPTChat instance as a dictionary, convenience method"""

        def add_to_dict_if_not_none(dictionary, key, value):
            if value is not None:
                dictionary[key] = value

        return_dict = {}
        add_to_dict_if_not_none(return_dict, "temperature", self.temperature)
        add_to_dict_if_not_none(return_dict, "model", self.model_name)
        add_to_dict_if_not_none(return_dict, "max_tokens", self.max_tokens)
        add_to_dict_if_not_none(return_dict, "top_p", self.top_p)
        add_to_dict_if_not_none(
            return_dict, "frequency_penalty", self.frequency_penalty
        )
        add_to_dict_if_not_none(return_dict, "presence_penalty", self.presence_penalty)
        return return_dict

    def make_api_call(
        self, chat_log: Union[list[dict], ch.ChatLog]
    ) -> Union[ch.Message, str, dict]:
        """Makes an API call to OpenAI's API and returns the result in the format specified by the return_type attribute"""

        def add_to_dict_if_not_none(dictionary, key, value):
            if value is not None:
                dictionary[key] = value

        if isinstance(chat_log, ch.ChatLog):
            messages = chat_log.get_finished_chat_log()
        elif isinstance(chat_log, list):
            messages = chat_log
        else:
            raise TypeError(
                f"chat_log must be a ChatLog or a list of messages, not {type(chat_log)}"
            )

        openai.api_key = self.api_key

        completion_params = {}
        add_to_dict_if_not_none(completion_params, "temperature", self.temperature)
        add_to_dict_if_not_none(completion_params, "max_tokens", self.max_tokens)
        add_to_dict_if_not_none(completion_params, "top_p", self.top_p)
        add_to_dict_if_not_none(
            completion_params, "frequency_penalty", self.frequency_penalty
        )
        add_to_dict_if_not_none(
            completion_params, "presence_penalty", self.presence_penalty
        )

        completion_params["model"] = self.model_name
        completion_params["messages"] = messages
        retries = 3
        while True:
            try:
                completion = openai.ChatCompletion.create(**completion_params)

                return self._format_return(completion)
            except openai.OpenAIError as e:
                if retries == 0:
                    raise e
                    break
                print(
                    "Encountered the following error while making an API call to OpenAI's API"
                )
                print(e)
                retries -= 1
                print("Trying again... " + str(retries) + " retries left")
                time.sleep(3)

    def make_save_dict(self) -> dict:
        """Returns a dictionary that can be used to recreate the GPTChat object"""
        return {
            "temperature": self.temperature,
            "model_name": self.model_name,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "frequency_penalty": self.frequency_penalty,
            "presence_penalty": self.presence_penalty,
            "return_type": self.return_type,
        }

    def _verify_save_dict(self, save_dict):
        """Verifies that a save dict is valid, if not raises an error"""
        required_keys = {
            "temperature": float,
            "model_name": str,
            "top_p": float,
            "frequency_penalty": float,
            "presence_penalty": float,
            "return_type": str,
        }
        if not isinstance(save_dict, dict):
            raise TypeError("save_dict must be a dictionary")
        for key, value in required_keys.items():
            if not key in save_dict:
                raise BadGPTChatDictError(" Save Dict Missing key: " + key)
            if not isinstance(save_dict[key], value):
                raise BadGPTChatDictError(
                    f"Save Dict key {key} must be of type {value}, not {type(save_dict[key])}"
                )
        return save_dict

    def load_save_dict(self, save_dict: dict) -> None:
        """Loads a save dict into the GPTChat object"""
        save_dict = self._verify_save_dict(save_dict)
        self.temperature = save_dict["temperature"]
        self.model_name = save_dict["model_name"]
        self.top_p = save_dict["top_p"]
        self.frequency_penalty = save_dict["frequency_penalty"]
        self.presence_penalty = save_dict["presence_penalty"]
        self.return_type = save_dict["return_type"]


class ChatWrapper:
    """Wrapper for GPTChat and ChatLog to make it easier to use, simplifies making a chatbot. Provide an instance of GPTChat and ChatLog to the constructor. and use the run_chat method to send the chatlog to the API and add the response to the chatlog
    Attributes:
        gpt_chat (GPTChat): Instance of GPTChat object
        chat_log (ChatLog): Instance of ChatLog object
        uuid (uuid): Unique identifier for the chatbot
        version (str): Version of the ChatWrapper class
        is_loaded (bool): Whether the chatbot has been loaded from a save file
        save_and_load (SaveAndLoad): Instance of SaveAndLoad class
    Methods:
        run_chat(self)-> None: Sends chatlog to API and adds response to chatlog
        chat_with_assistant(self, message: str) -> str: Adds message to chatlog and runs chat, and returns the assistant message pretty printed
        save(self, file_name, overwrite=False) -> bool: Saves the chatbot to a file, uses the save_and_load object
        load(self, file_name) -> bool: Loads the chatbot from a file, uses the save_and_load object
    Subclasses:
        SaveAndLoad: Class for saving and loading chatbots
    Relies on:
        GPTChat, ChatLog, SaveAndLoad, Message
    Raises:
        TypeError: If gpt_chat is not an instance of GPTChat
        BadChatWrapperDictError: If the save dict is missing a key or has a key with the wrong type
    Example Usage:
        chatbot = ChatWrapper(GPTChat_object, ChatLog_object)
        print(chatbot.chat_with_assistant("Hello"))
        chatbot.save("chatbot_save")
        chatbot.load("chatbot_save")



    """

    version = "0.1.0"

    def __init__(
        self, gpt_chat: GPTChat, chat_log: ch.ChatLog, save_path: str = "chatbot_saves"
    ) -> None:
        self.gpt_chat = gpt_chat
        self.chat_log = chat_log
        self.gpt_chat.return_type = "string"
        self.uuid = uuid.uuid4()
        self.is_loaded = False
        self.save_and_load = self.SaveAndLoad(self, save_path=save_path)

    def run_chat(self) -> None:
        """Sends chatlog to API and adds response to chatlog, uses the GPTChat object's make_api_call method. If an error occurs while making an API call, the chatbot will be saved to a file with the current time as the name and the error will be raised"""
        try:
            response = self.gpt_chat.make_api_call(
                self.chat_log.get_finished_chat_log()
            )
        except openai.OpenAIError as e:
            print("A fatal error occurred while making an API call to OpenAI's API")
            save_name = (
                datetime.datetime.now().isoformat().replace(":", "-") + "_fatal_error"
            )
            print("Saving chatbot to " + save_name + " before exiting...")
            if self.save(save_name):
                print("Chatbot saved successfully")
            raise e

        self.chat_log.assistant_message = response

    @property
    def assistant_message(self) -> str:
        """Returns the assistant message"""

        return self.chat_log.assistant_message.pretty()

    @assistant_message.setter
    def assistant_message(self, message: str) -> None:
        """Sets the assistant message"""
        self.chat_log.assistant_message = message

    @property
    def user_message(self) -> str:
        """Returns the user message, pretty printed"""
        return self.chat_log.user_message.pretty()

    @user_message.setter
    def user_message(self, message: str) -> None:
        """Sets the user message"""
        self.chat_log.user_message = message

    def chat_with_assistant(self, message: str) -> str:
        """Sets an assistant message and returns the response, pretty printed"""
        self.user_message = message
        self.run_chat()
        return self.assistant_message

    def save(self, file_name: str, overwrite: bool = False) -> bool:
        return self.save_and_load.save_to_file(file_name, overwrite)

    def load(self, file_name: str) -> bool:
        return self.save_and_load.load_from_file(file_name)

    def modify_max_completion_tokens(self, max_completion_tokens: int) -> None:
        """This is necessary as the max_completion_tokens must be changed in both the ChatLog object and the GPTChat object"""
        self.chat_log.set_token_info(max_completion_tokens=max_completion_tokens)
        self.gpt_chat.max_tokens = max_completion_tokens

    class SaveAndLoad:
        """
        Class for saving and loading chat wrappers, with separate methods for saving and loading to file, and saving and loading to dictionary"
        Methods:
            save_to_file(file_name: str, overwrite: bool = False) -> bool
            load_from_file(file_name: str) -> bool
            get_files(remove_path = True) -> list
            make_save_dict(file_name: str) -> dict
            load_from_dict(save_dict: dict) -> None
            _verify_save_dict(save_dict: dict) -> dict
        Attributes:
            chat_wrapper: The chat wrapper to save or load from
            save_folder: The folder to save to or load from
            gpt_chat: The GPTChat object inside the chat wrapper
            chat_log: The ChatLog object inside the chat wrapper
        Example Usage:
            chat_wrapper = ChatWrapper(gpt_chat, chat_log)
            chat_wrapper.save_and_load.save_to_file("chat_wrapper_save")
            chat_wrapper.save_and_load.load_from_file("chat_wrapper_save")
            chat_wrapper.save_and_load.get_files()
        """

        def __init__(self, chat_wrapper, save_folder="chat_wrapper_saves"):
            self.chat_wrapper = chat_wrapper
            if not save_folder.endswith("/"):
                save_folder = save_folder + "/"
            self.save_folder = save_folder
            if not os.path.exists(self.save_folder):
                os.makedirs(self.save_folder)
            self.gpt_chat = chat_wrapper.gpt_chat
            self.chat_log = chat_wrapper.chat_log

        def make_save_dict(self, file_name: str) -> dict:
            """Returns a dictionary that can be used to recreate the chat wrapper"""

            chat_log_dict = self.chat_log.make_save_dict()
            gpt_chat_dict = self.gpt_chat.make_save_dict()

            meta_data = {
                "chat_wrapper_version": self.chat_wrapper.version,
                "chat_wrapper_uuid": self.chat_wrapper.uuid,
                "timestamp": datetime.datetime.now().isoformat(),
            }
            return {
                "meta_data": meta_data,
                "chat_log": chat_log_dict,
                "gpt_chat": gpt_chat_dict,
            }

        def load_save_dict(self, save_dict: dict) -> None:
            """Loads a save dict into the chat wrapper"""
            self.chat_wrapper.uuid = save_dict["meta_data"]["chat_wrapper_uuid"]
            self.chat_log.load_save_dict(save_dict["chat_log"])
            self.gpt_chat.load_save_dict(save_dict["gpt_chat"])
            self.chat_wrapper.is_loaded = True

        def save_to_file(self, file_name: str, overwrite=False) -> bool:
            """Saves the chat wrapper to a file, returns True if successful, False if not"""
            if not overwrite and os.path.exists(file_name):
                return False
            file_name = self._add_file_path(file_name)
            save_dict = self.make_save_dict(file_name)
            with open(file_name, "w") as f:
                json.dump(save_dict, f)
            return True

        def load_from_file(self, file_name: str) -> None:
            """Loads a save file into the chat wrapper"""
            file_name = self._add_file_path(file_name)
            if not os.path.exists(file_name):
                return False
            with open(file_name, "r") as f:
                save_dict = json.load(f)
            self.load_save_dict(save_dict)

        def _add_file_path(self, file_name: str) -> str:
            """Adds the path to the file name, as well as the .json extension"""

            if not file_name.endswith(".json"):
                file_name = file_name + ".json"
            if not file_name.startswith(self.save_folder):
                file_name = self.save_folder + file_name
            return file_name

        def _remove_file_path(self, file_name: str) -> str:
            """Removes the path from the file name, as well as the .json extension"""
            if file_name.startswith(self.save_folder):
                file_name = file_name[len(self.save_folder) :]
            if file_name.endswith(".json"):
                file_name = file_name[:-5]
            return file_name

        def get_files(self, remove_path=True) -> list:
            """Returns a list of files in the save folder, if remove_path is true, the path will be removed from the file names"""
            files = []
            for file in os.listdir(self.save_folder):
                if file.endswith(".json"):
                    if remove_path:
                        file = self._remove_file_path(file)
                    files.append(file)
            return files
