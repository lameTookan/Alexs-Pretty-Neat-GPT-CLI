import ChatHistory as ch
import openai
import os
import json


from typing import List, Dict, Union, Any, Optional
import uuid
import datetime
import time
import super_secret

API_KEY = super_secret.OPENAI_API_KEY


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


def try_converting_to_datatype(value: Any, datatype: type) -> Any | bool:
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
    # this is a set of all the possible parameters that can be passed to the openai api, and their descriptions, used for error checking but also for help.
    # check out the official openai api docs for more info
    # https://platform.openai.com/docs/guides/gpt/chat-completions-api
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
        template: dict = None,
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
            "template": template,
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

    def reload_from_template(self) -> bool:
        """Reloads the model from the template, if the template is None, returns False"""
        if self.template == None:
            return False
        settings = self.template["gpt_chat"]
        self.modify_params(**settings)

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

    # all of the following are setters and getters for the model parameters. They accept None as a value, which means that the parameter not be sent to the openai api(ie it won't send over param=None, it just won't send over that param at all)
    @property
    def temperature(self) -> float:
        """Returns the temperature"""
        return self._temperature

    @temperature.setter
    def temperature(self, value: float) -> None:
        """Sets the temperature, which is a float between 0 and 2"""
        if value is None:
            self._temperature = value
            return None
        value = try_converting_to_datatype(value, float)
        if value is False:
            raise BadChatCompletionParams(
                bad_param={"temperature": value}, msg="Temperature must be a float"
            )
        elif not 0 <= value <= 2:
            raise BadChatCompletionParams(bad_param={"temperature": value})
        else:
            self._temperature = value

    @property
    def model_name(self) -> str:
        """Returns the model name"""
        return self._model_name

    @model_name.setter
    def model_name(self, value: str) -> None:
        """Sets the model name, which is a string, these are changed often by openai, so check the openai api for the most up to date models. The openai api will raise an error if it's not valid.The default is gpt-4"""

        self._model_name = value

    @property
    def max_tokens(self) -> int:
        """Returns the max tokens, which is an int between 1 and the model's max tokens"""
        return self._max_tokens

    @max_tokens.setter
    def max_tokens(self, value: int) -> None:
        """Sets the max tokens, which is an int between 1 and the model's max tokens"""
        if value is None:
            self._max_tokens = value
            return None
        value = try_converting_to_datatype(value, int)
        if value is False:
            raise BadChatCompletionParams(
                bad_param={"max_tokens": value}, msg="Max tokens must be an int"
            )

        elif value < 1:
            raise BadChatCompletionParams(bad_param={"max_tokens": value})
        else:
            self._max_tokens = value

    @property
    def top_p(self) -> float:
        """Returns the top p, which is a float between 0 and 1"""
        return self._top_p

    @top_p.setter
    def top_p(self, value: float) -> None:
        """Sets the top p, which is a float between 0 and 1"""
        if value is None:
            self._top_p = value
            return None
        value = try_converting_to_datatype(value, float)
        if value is False:
            raise BadChatCompletionParams(
                bad_param={"top_p": value}, msg="Top p must be a float"
            )
        elif not 0 <= value <= 1:
            raise BadChatCompletionParams(bad_param={"top_p": value})
        else:
            self._top_p = value

    @property
    def frequency_penalty(self) -> float:
        return self._frequency_penalty

    @frequency_penalty.setter
    def frequency_penalty(self, value: float) -> None:
        """Sets the frequency penalty, which is a float between 0 and 2"""
        if value is None:
            self._frequency_penalty = value
            return None
        value = try_converting_to_datatype(value, float)
        if value is False:
            raise BadChatCompletionParams(
                bad_param={"frequency_penalty": value},
                msg="Frequency penalty must be a float",
            )
        elif not 0 <= value <= 2:
            raise BadChatCompletionParams(bad_param={"frequency_penalty": value})
        else:
            self._frequency_penalty = value

    @property
    def presence_penalty(self) -> float:
        """Gets the presence penalty, which is a float between 0 and 2"""
        return self._presence_penalty

    @presence_penalty.setter
    def presence_penalty(self, value: float) -> None:
        """Sets the presence penalty, which is a float between 0 and 2"""

        if value is None:
            self._presence_penalty = value
            return None
        value = try_converting_to_datatype(value, float)
        if value is False:
            raise BadChatCompletionParams(
                bad_param={"presence_penalty": value},
                msg="Presence penalty must be a float",
            )
        elif not 0 <= value <= 2:
            raise BadChatCompletionParams(bad_param={"presence_penalty": value})
        else:
            self._presence_penalty = value

    @property
    def return_type(self) -> str:
        """Gets the return type of the chatbot"""
        return self._return_type

    @return_type.setter
    def return_type(self, value: str) -> None:
        """Sets the return type of the chatbot, can be one of the following:
            "string", "json", "dict", "Message"
        Verify that the value is one of the above, otherwise raise a BadReturnTypeError
        """
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
        add_to_dict_if_not_none(return_dict, "model_name", self.model_name)
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
        """Makes an API call to OpenAI's API and returns the result in the format specified by the return_type attribute
        Note: If a model parameter is None, it will not be included in the API call at all, so openai will use the default

        This means that you can set any of the parameters to None and instead of sending over `param_name = None' and causing an error, they just won't be sent at all
        """

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

    def _verify_save_dict(self, save_dict: dict) -> dict:
        """Verifies that a save dict is valid, if not raises an error"""
        required_keys = {
            "temperature": float,
            "max_tokens": int,
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
            if not isinstance(save_dict[key], value) and save_dict[key] is not None:
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


import unittest


class TestGPTChat(unittest.TestCase):
    def setUp(self):
        self.gpt_chat = GPTChat(API_KEY=API_KEY)

    def test_temperature_setter_and_getter(self):
        self.gpt_chat.temperature = 1.5
        self.assertEqual(self.gpt_chat.temperature, 1.5)

    def test_model_name_setter_and_getter(self):
        self.gpt_chat.model_name = "gpt-3"
        self.assertEqual(self.gpt_chat.model_name, "gpt-3")

    def test_max_tokens_setter_and_getter(self):
        self.gpt_chat.max_tokens = 500
        self.assertEqual(self.gpt_chat.max_tokens, 500)

    def test_top_p_setter_and_getter(self):
        self.gpt_chat.top_p = 0.9
        self.assertEqual(self.gpt_chat.top_p, 0.9)

    def test_frequency_penalty_setter_and_getter(self):
        self.gpt_chat.frequency_penalty = 0.5
        self.assertEqual(self.gpt_chat.frequency_penalty, 0.5)

    def test_presence_penalty_setter_and_getter(self):
        self.gpt_chat.presence_penalty = 0.5
        self.assertEqual(self.gpt_chat.presence_penalty, 0.5)

    def test_return_type_setter_and_getter(self):
        self.gpt_chat.return_type = "dict"
        self.assertEqual(self.gpt_chat.return_type, "dict")

    def test_modify_params(self):
        self.gpt_chat.modify_params(temperature=0.8, max_tokens=300)
        self.assertEqual(self.gpt_chat.temperature, 0.8)
        self.assertEqual(self.gpt_chat.max_tokens, 300)

    def test_get_params(self):
        self.gpt_chat.modify_params(temperature=0.8, max_tokens=300)
        params = self.gpt_chat.get_params()
        self.assertEqual(params["temperature"], 0.8)
        self.assertEqual(params["max_tokens"], 300)

    def test_load_save_dict(self):
        save_dict = self.gpt_chat.make_save_dict()
        test_chat = GPTChat(API_KEY=API_KEY)
        GPTChat.load_save_dict(test_chat, save_dict)
        for key, value in save_dict.items():
            with self.subTest(key=key):
                self.assertEqual(getattr(test_chat, key), value)


if __name__ == "__main__":
    unittest.main()
