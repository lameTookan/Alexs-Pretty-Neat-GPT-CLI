import tiktoken

from collections import namedtuple, UserString, UserList, UserDict, deque, namedtuple
import datetime
from EncodeMessage import EncodeMessage, BadMessageError, EncodedMessage
import unittest
import json
import os
import uuid


class NoSystemPromptError(Exception):
    pass


class BadSysWildcardError(Exception):
    pass


class BadSaveDictError(Exception):
    pass


class Message(UserDict):
    """
    A message object containing a role and content, along with methods to count tokens and style
    Attributes:
        role (str): The role of the message, either 'user', 'assistant', or 'system'
        content (str): The content of the message
        tokens (int): The number of tokens in the message
        model (str): The model used to encode the message, for use in counting tokens
        .data (dict): The data of the message, containing the role and content
    Methods:
        _count_tokens: Counts the number of tokens in the message
        pretty: Returns a pretty-printed version of the message

    """

    def __init__(self, role: str, content: str, model: str = "gpt-4"):
        super().__init__({"role": role, "content": content})
        self.role = role
        self.content = content
        self.model = model
        self.tokens = self._count_tokens(content)

    def _count_tokens(self, string):
        encoding = tiktoken.encoding_for_model(self.model)
        return len(encoding.encode(string))

    def pretty(self):
        if self.role == "user":
            return f"> {self.content}"
        elif self.role == "assistant":
            return f" >> \u001b[32m{self.content}\u001b[0m"
        elif self.role == "system":
            return f" >>> \u001b[31m{self.content}\u001b[0m"
        else:
            return f" >> {self.content}"


class ChatLog:
    system_prompt_wildcards = {
        "date": {"value": "__DATE__", "description": "The current date and time"}
    }
    
    """
    A ChatLog class for managing and preparing a chat log for use with the OpenAI API.

    Attributes:
        Token Information:
            max_model_tokens (int): Maximum tokens allowed for the model.
            max_completion_tokens (int): Maximum tokens allowed for the completion.
            token_padding (int): Subtract from max_model_tokens to allow for the completion.
            max_chat_tokens (int): Maximum tokens allowed for the chat log.
        Chat Log:
            max_chat_messages (int): Maximum messages allowed in the chat log.
            model (str): Model used to encode the messages for token counting.
            full_chat_log (list): Contains Message objects.
            trimmed_chat_log (deque): Contains Message objects, trimmed to max_chat_messages and max_chat_tokens.
        Other:
            _sys_prompt (str): System prompt. Must be added via setter before use.
            is_loaded (bool): True if the chat log has been loaded from a file.

    Methods:
        Token Information:
            set_token_info, work_out_tokens
        Chat Log Setup and Management:
            setup, trim_chat_log, add_message, add_message_list
        System Prompt:
            _check_sys_prompt, system_prompt
        Messages:
            make_message, add_message_obj, get_messages, get_messages_as_list
        Save/Load:
            save, load
        Other:
            add_more_wildcards, _add_wildcards, _check_wildcards

    Subclasses:
        SaveToDict: Saves/loads the class to a dictionary and verifies it.
        SaveToFile: Saves/loads the class to a file using SaveToDict.

    Usage Example:
        ```
        chat_log = ChatLog(max_model_tokens=100, max_completion_tokens=50, token_padding=5)
        chat_log.system_prompt = "Hello, how can I assist you today?"
        chat_log.add_message(role="user", content="Tell me about the weather.")
        response = OpenAI_API.call(chat_log.get_finished_chat_log())
        chat_log.add_message(role="assistant", content=response)
        chat_log.save("chatlog.txt")
        ```

    Exceptions:
        BadMessageError, NoSystemPromptError, NoTokenInfoError, BadSaveDictError

    Dependencies:
        Message class, Tiktoken module
    """
    version = "1.0.0"

    def __init__(
        self,
        max_model_tokens: int = 8000,
        max_completion_tokens: int = 1000,
        token_padding: int = 500,
        extra_wildcards=None,
        save_folder="chat_log_saves",
        model="gpt-4",
        max_chat_messages: int = 200,
       
    ):
        self.constructor_args = {
            "max_model_tokens": max_model_tokens,
            "max_completion_tokens": max_completion_tokens,
            "token_padding": token_padding,
            "extra_wildcards": extra_wildcards,
            "save_folder": save_folder,
            "model": model,
            "max_chat_messages": max_chat_messages,

        }
        self.token_info = {
            "max_model_tokens": int(max_model_tokens),
            "max_completion_tokens": max_completion_tokens,
            "token_padding": token_padding,
        }
        self.id = str(uuid.uuid4())
        self.max_model_tokens = max_model_tokens
        self.max_completion_tokens = max_completion_tokens
        self.token_padding = token_padding
        self.save_to_dict = SaveToDict(self)
        self.save_to_file = self.SaveToFile(self, save_folder)
        self.model = model
        self.max_chat_tokens = None
        self.max_chat_messages = max_chat_messages
        self.full_chat_log = []
        self.trimmed_chat_log = deque()
        self.trimmed_chat_log_tokens = 0
        self._sys_prompt = None
        self.trimmed_messages = 0
        self.is_loaded = False
        self.max_chat_messages = max_chat_messages
        if extra_wildcards:
            self.system_prompt_wildcards.update(extra_wildcards)
        # this is for use with the ChatLogAndGPTChatFactory class, see object_factory.py for more info 
        #self.template = template
    # def reload_from_template(self, template_name: str = None)-> bool:
    #     if template_name:
    #         self.template = template_name
    #     else:
    #         template_name = self.template
    #     if not template_name:
    #         return False
    #     template = templates.get(template_name).get("chat_log")
    #     if not template:
    #         return False
       
    #     for key, val in template.items():
    #         if val:
    #             self.__setattr__(key, val)
    #     self.work_out_tokens()
      
    #     return True
    def _check_wildcards(self, wildcards: dict):
        """Checks if wildcards are valid"""
        if not isinstance(wildcards, dict):
            raise TypeError("Wildcards must be a dictionary")
        for key, value in wildcards.items():
            if not isinstance(key, str):
                raise BadMessageError("Wildcard keys must be strings")
            if not isinstance(value, dict):
                raise BadMessageError("Wildcard values must be dictionaries")
            if "value" not in value:
                raise BadMessageError("Wildcard values must have a value key")
            if "description" not in value:
                raise BadMessageError("Wildcard values must have a description key")

    def set_token_info(
        self,
        max_model_tokens: int = None,
        max_completion_tokens: int = None,
        token_padding: int = None,
    ):
        self.max_model_tokens = max_model_tokens
        self.max_completion_tokens = max_completion_tokens
        self.token_padding = token_padding
    # methods dealing with the system prompt
    def setup(self):
        for key in self.token_info.keys():
            if self.token_info[key] == None:
                raise ValueError(f"{key} must be set")
        self._check_sys_prompt()
        self.work_out_tokens()

    def _check_sys_prompt(self):
        """Checks if the system prompt has been set"""
        if not self._sys_prompt:
            raise NoSystemPromptError("System prompt has not been set")

    

    @property
    def sys_prompt(self):
        """Returns the system prompt with wildcards added"""
        self._check_sys_prompt()
        return self._add_wildcards(self._sys_prompt)

    @sys_prompt.setter
    def sys_prompt(self, value: str):
        """Sets the system prompt, works out the number of tokens allowed for the chat log, and trims the chat log"""
        self._sys_prompt = value
        self.work_out_tokens()
        self.trim_chat_log()

    def add_more_wildcards(self, wildcards: dict):
        """Adds more wildcards to the system prompt"""
        self._check_wildcards(wildcards)
        self.system_prompt_wildcards.update(wildcards)

    def _add_wildcards(self, string):
        """Adds wildcards to the system prompt"""
        wild_cards = {
            key: value["value"] for key, value in self.system_prompt_wildcards.items()
        }
        for key, value in wild_cards.items():
            if value == "__DATE__":
                wild_cards[key] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        return string.format(**wild_cards)

    

   # methods for core functionality of trimming and managing the chat log

    def work_out_tokens(self):
        """Works out the number of tokens allowed for the chat log"""
        self._check_sys_prompt()
        self.sys_prompt_message = self.make_message("system", self.sys_prompt)
        self.sys_prompt_tokens = self.sys_prompt_message.tokens
        self.max_chat_tokens = self.max_model_tokens - (
            self.sys_prompt_tokens
            + self.token_padding
            + self.max_completion_tokens
        )
    def trim_chat_log(self):
        """Trims the chat log to the maximum number of messages and tokens allowed"""
        while self.trimmed_chat_log_tokens > self.max_chat_tokens:
            message = self.trimmed_chat_log.popleft()
            self.trimmed_chat_log_tokens -= message.tokens
            self.trimmed_messages += 1
        while len(self.trimmed_chat_log) > self.max_chat_messages:
            self.trimmed_chat_log.popleft()
            self.trimmed_chat_log_tokens -= message.tokens
            self.trimmed_messages += 1
    # main method to retrieve the chat log, for use with the OpenAI API
    def get_finished_chat_log(self):
        """Returns the trimmed chat log with the system prompt at the start for use with the OpenAI API"""
        head = [{"role": "system", "content": self.sys_prompt}]
        tail = [dict(message) for message in self.trimmed_chat_log]
        return head + tail
    @property
    def finished_chat_log(self):
        """Returns the trimmed chat log with the system prompt at the start"""
        return self.get_finished_chat_log()

   # adding messages 
   # main function to add messages to the chat log, takes a message object
    #makes a message object from a role and content, or a dictionary
    def make_message(self, role: str = None, content: str = None, message: dict = None):
        """Make a message object from a role and content"""
        if not message:
            if not role and not content:
                raise ValueError("Either role and content or message must be provided")
        if role and content and message:
            raise ValueError("Only role and content or message can be provided")
        if message:
            return Message(role = message["role"], content=message["content"], model=self.model)
        return Message(role, content, self.model)
    
    def add_message_obj(self, message: Message):
        """Adds a message to the chat log"""

        self._check_sys_prompt()
        self.full_chat_log.append(message)
        self.trimmed_chat_log.append(message)
        self.trimmed_chat_log_tokens += message.tokens
        self.trim_chat_log()
   
    #helper functions to add messages to the chat log, takes a role and content, or a dictionary
    def add_message(self, role: str = None, content: str = None, message: dict = None):
        """Wrapper for add_message_obj, makes a message object from a role and content, can take a dictionary, or role and content"""
        if not message and not (role and content):
            raise ValueError("Either role and content or message must be provided")
        if message and (role or content):
            raise ValueError("Only role and content or message can be provided")
        if message:
            message = self.make_message(message=message)
        else:
            message = self.make_message(role, content)
        self.add_message_obj(message)
    # add a list of messages to the chat log, takes a list of dicts
    def add_message_list(self, message_list: list[dict]):
        """Adds a list of messages to the chat log"""

        for message in message_list:
            self.add_message(message=message)
            
                
    #setters and getters for the last user and assistant messages, for convenience
    # the getters return the last message as Message objects
    # the setters add a message to the chat log, taking a string 
    @property
    def user_message(self)-> Message:
        """Returns the last user message"""
        for message in self.get_messages(role = "user", limit = 1):
            result = message
        if result == None:
            return None
        else:
            return result

    @user_message.setter
    def user_message(self, value: str ):
        """Adds a user message to the chat log"""
        self.add_message(role = "user", content = value)

    @property
    def assistant_message(self) -> Message:
        """Returns the last assistant message"""
        result = None
        for message in self.get_messages(role = "assistant", limit =1):
            result = message
        if result == None:
            return None
        else:
            return result

    @assistant_message.setter
    def assistant_message(self, value: str) :
        """Adds an assistant message to the chat log"""
        self.add_message("assistant", value)

    
    # wrappers that deal with saving and loading the chat log to a file.
    # The two subclasses are SaveToFile and SaveToDict control most of the functionality, however these wrappers are provided for convenience
    def save(self, filename: str, overwrite: bool = False) -> bool:
        """Wrapper for SaveToFile.save, saves a chat log to a file, check SaveToFile.save for more info"""
        return self.save_to_file.save(filename, overwrite)

    def load(self, filename: str) -> bool:
        """Wrapper for SaveToFile.load, loads a chat log from a file, check SaveToFile.load for more info"""
        return self.save_to_file.load(filename)
    def make_save_dict(self) -> dict:
        """convenience function to make a save dict, calls SaveToDict.make_save_dict"""
        return self.save_to_dict.save()
    def load_save_dict(self, save_dict: dict) -> bool:
        """convenience function to load a save dict, calls SaveToDict.load()"""
        return self.save_to_dict.load(save_dict)

   

    

    

    

    class SaveToFile:
        version = "1.0.0"
        """This class handles saving and loading chat logs to and from files
        Attributes:
            chat_log (ChatLog): the chat log object to save from.
            save_folder (str): the folder to save to.
            dict_saver (function): the SaveToDict object to use to save the state of the ChatLog object to a dict, and load from a dict.
        Methods:
        add_path(filename: str) -> str:
            Adds the save_folder to the filename if it doesn't already have it, and adds .json to the end if it doesn't already have it.
        remove_path(filename: str) -> str:
            Removes the save_folder from the filename if it has it, and removes .json from the end if it has it.
        save(filename: str, overwrite: bool = False) -> bool:
            Saves the current state of the chat log to a file. If overwrite is False, it will not overwrite an existing file and return False. If overwrite is True, it will overwrite an existing file and return True.
        load(filename: str) -> bool:
            Loads the state of the chat log from a file. Returns True if successful, False if not.
        get_file_list(remove_path = False) -> list:
            Returns a list of all the files in the save_folder. If remove_path is True, it will remove the save_folder from the filenames and remove .json from the end of the filenames.


        """

        def __init__(self, chat_log, save_folder: str):
            self.chat_log = chat_log
            if not save_folder.endswith("/"):
                save_folder += "/"
            self.save_folder = save_folder
            
            self.dict_saver = self.chat_log.save_to_dict

        def add_path(self, filename: str) -> str:
            """Adds the save_folder to the filename if it doesn't already have it, and adds .json to the end if it doesn't already have it."""
            if not filename.endswith(".json"):
                result =  filename + ".json"
            if not os.path.exists(self.save_folder):
                os.makedirs(self.save_folder)
            if not filename.startswith(self.save_folder):   
                result = os.path.join(self.save_folder, result)
            return result 

        def remove_path(self, filename: str) -> str:
            """Removes the save_folder from the filename if it has it, and removes .json from the end if it has it."""
            if filename.endswith(".json"):
                filename = filename[:-5]
            if filename.startswith(self.save_folder):
                filename = filename[len(self.save_folder + "/") :]
            return filename
  
        def save(self, filename: str, overwrite: bool = False) -> bool:
            """Save the current state of the chat log to a file. If overwrite is True, the file will be overwritten if it already exists, otherwise, False will be returned."""
            filename = self.add_path(filename)
            if os.path.exists(filename) and not overwrite:
                return False
            save_dict = self.dict_saver.save()
            with open(filename, "w") as f:
                json.dump(save_dict, f)
            return True

        def load(self, filename: str) -> bool:
            """Using the SaveToDict class, load a save file."""
            file_name = self.add_path(filename)
            if not os.path.exists(file_name):
                return False
            with open(file_name, "r") as f:
                save_dict = json.load(f)
            print(save_dict)
            self.chat_log.save_to_dict.load(save_dict)
            return True

        def get_file_list(self, remove_path: bool = False) -> list:
            """Get a list of all files in the save folder. If remove_path is True, the save folder path will be removed from the filenames."""
            file_list = os.listdir(self.save_folder)
            if remove_path:
                file_list = [self.remove_path(filename) for filename in file_list]
            return file_list
        
    #related to getting and outputting messages
    # main function to get messages
    def get_messages(self, role: str = None, limit: int = None, reverse: bool = True) -> Message:
        """Returns a generator of messages from the chat log in reverse order if limit is not None"""
        chat_log = self.full_chat_log[::-1] if reverse else self.full_chat_log
       
        counter = 0
        for message in chat_log:
            
            if role == None or message.role == role:
                yield message
                counter += 1
            if limit != None and counter == limit:
                break
    #helper functions to get messages
    def get_message_obj(self, role: str = None, limit: int = None, reverse = None) -> Message:
        if reverse is None:
            generator = self.get_messages(role, limit)
        else:
            generator = self.get_messages(role, limit, reverse)
        result = []
        for message in generator:
            result.append(message)
        return result
    def get_messages_as_list(self, role: str = None, limit: int = None, reverse: bool = True, format: str = 'Message') -> list:
        """Returns a list of messages from the chat log in reverse order if limit is not None. format can be 'Message', 'dict', 'str', or 'pretty'"""
        formats = {"Message", "dict", "str", "pretty"}
        if format not in formats:
            raise ValueError(f"format must be one of {formats}")    
        result = []
        for message in self.get_messages(role, limit, reverse):
            if format == "Message":
                result.append(message)
            elif format == "str":
                result.append(message.content())
            elif format == "dict":
                result.append(dict(message))
            elif format == "pretty":
                result.append(message.pretty())
            else: 
                result.append(message)
        return result
    def get_pretty_messages(self, role: str = None, limit: int = None, reverse = False) -> str:
        """Returns a string of messages from the chat log in reverse order if limit is not None"""
        result = []
        for message in self.get_messages(role, limit, reverse):
            result.append(message.pretty())
        return "\n".join(result)
    def reset(self, clear_sys_prompt = False):
        """Resets the chat log to its initial state"""
        self.full_chat_log = []
        self.trimmed_chat_log = []
        self.trimmed_messages = 0 
        self.trimmed_chat_log_tokens = 0
        if clear_sys_prompt:
            self._sys_prompt = None
        self.is_loaded = False
    def __str__(self):
        return self.get_pretty_messages()
    def __repr__(self):
        constructor_list = []
        for key, val in self.constructor_args.items():
            constructor_list.append(f"{key}={val}")
        constructor_arg_str = ", ".join(constructor_list)
        constructor = f"ChatLog({constructor_arg_str})"
        important_vars = {
            "is_loaded":self.is_loaded ,
            "max_chat_tokens":self.max_chat_tokens,
            "max_chat_messages":self.max_chat_messages,
            "chat_log len ":len(self.full_chat_log),
            "trimmed chat log len":len(self.trimmed_chat_log),
            "trimmed messages ": self.trimmed_messages,
            "trimmed chat log tokens": self.trimmed_chat_log_tokens,
            "system prompt": self._sys_prompt,

            }
        important_vars  = "\n".join(['{}: {}'.format(key, val) for key, val in important_vars.items()])
        return f"{constructor}\n{important_vars}"


class SaveToDict:
        """Class for saving and loading chat logs to a dict
        Generally used for saving to a file using the SaveToFile class, however can be used for other purposes if needed
        Attributes:
            chat_log (ChatLog): The chatlog object to be saved
        Methods:
            save: Prepares a dict to be saved to a file or for use in other objects/functions, returns the dict
            load: Loads a dict into the chat log
            _check_save_dict: Checks that the dict to be loaded is valid, raises BadSaveDictError if not valid and/or missing required keys with datatypes

        """
        version = "1.0.0"

        def __init__(self, chat_log: ChatLog):
            self.chat_log = chat_log

        def save(self) -> dict:
            """Prepares a dict to be saved to a file or for use in other objects/functions"""
            

           
            save_dict = {
                "metadata": {
                    "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "length": len(self.chat_log.full_chat_log),
                    "uuid": self.chat_log.id,
                    "ChatLog version": self.chat_log.version,
                    "SaveToDict version": self.version,


                },
                'max_chat_tokens': self.chat_log.max_chat_tokens,
                'max_chat_messages': self.chat_log.max_chat_messages,
                'max_model_tokens': self.chat_log.max_model_tokens,
                'token_padding': self.chat_log.token_padding,
                'max_completion_tokens': self.chat_log.max_completion_tokens,
                'max_chat_tokens': self.chat_log.max_chat_tokens,
                'full_chat_log': [message.data for message in self.chat_log.full_chat_log],
                'trimmed_chat_log': [message.data for message in self.chat_log.trimmed_chat_log],
                'trimmed_chat_log_tokens': self.chat_log.trimmed_chat_log_tokens,
                'trimmed_messages': self.chat_log.trimmed_messages,
                'sys_prompt': self.chat_log._sys_prompt,
                'model': self.chat_log.model,
                'wildcards': self.chat_log.system_prompt_wildcards,

                


            }
            size = len(json.dumps(save_dict))
            save_dict['metadata']['size'] = size
            del size
            return save_dict

           

        def _check_save_dict(self, save_dict: dict):
            """Checks that the save dict is valid, raises BadSaveDictError if not"""
            required_keys = {
                "max_chat_tokens": int,
                "max_chat_messages": int,
                "max_model_tokens": int,
                "token_padding": int,
                "max_completion_tokens": int,
                "model": str,
                "sys_prompt": str,
                "wildcards": dict,
                "full_chat_log": list,
                "trimmed_chat_log": list,
                "trimmed_chat_log_tokens": int,
                "trimmed_messages": int,
            }
            if not isinstance(save_dict, dict):
                raise BadSaveDictError(
                    "Save dict must be a dict, got {}".format(type(save_dict))
                )
            
            for key, datatype in required_keys.items():
                if key not in save_dict:
                    raise BadSaveDictError(
                        "Save dict missing required key {}".format(key)
                    )
                if not isinstance(save_dict[key], datatype):
                    raise BadSaveDictError(
                        "Save dict key {} must be of type {}, got {}".format(
                            key, datatype, type(save_dict[key])
                        )
                    )
            

        def load(self, save_dict: dict) -> None:
            """Loads a save_dict into the chat log, by setting the chat log attributes from the save dict"""
            self._check_save_dict(save_dict)
            model = save_dict["model"]
            self.chat_log.id = save_dict["metadata"]["uuid"]
            self.chat_log.model = model
            self.chat_log.max_chat_tokens = save_dict["max_chat_tokens"]
            self.chat_log.max_chat_messages = save_dict["max_chat_messages"]
            self.chat_log.max_model_tokens = save_dict["max_model_tokens"]
            self.chat_log.token_padding = save_dict["token_padding"]
            self.chat_log.max_completion_tokens = save_dict["max_completion_tokens"]
            self.chat_log.model = save_dict["model"]
            self.chat_log.sys_prompt = save_dict["sys_prompt"]
            self.chat_log.system_prompt_wildcards = save_dict["wildcards"]
            self.chat_log.full_chat_log = [ self.chat_log.make_message(message = msg ) for msg in save_dict["full_chat_log"] ]
            self.chat_log.trimmed_chat_log = [ self.chat_log.make_message(message = msg ) for msg in save_dict["trimmed_chat_log"]]
            self.chat_log.trimmed_chat_log_tokens = save_dict["trimmed_chat_log_tokens"]
            self.chat_log.trimmed_messages = save_dict["trimmed_messages"]
            self.chat_log.is_loaded = True
            self.chat_log.work_out_tokens()

def count_tokens(str, model):
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(str))

def get_test_chat_log(name = "random_10000"):
    with open(f"test_chat_logs/{name}.json", "r") as f:
        chat_log = json.load(f)
    return chat_log





class TestChatLog(unittest.TestCase):
    def setUp(self) -> None:
        self.chat_log = ChatLog(
            8000,
            1000,
            500,
        )
        self.test_sysprompt = "You are a helpful AI assistant"
        self.chat_log.sys_prompt = self.test_sysprompt

    def test_sys_prompt(self):
        self.assertEqual(self.chat_log.sys_prompt, "You are a helpful AI assistant")

    
    def test_add_message(self):
        message = Message(
            content="Hello, how are you?",
            role = 'user')
        self.chat_log.add_message_obj(message)
        self.assertEqual(self.chat_log.get_message_obj(limit=1)[0], message)

    def test_finished_chat_log(self):
        with open("test_chat_logs/random_10000.json", "r") as f:
            chat_log = json.load(f)
        self.chat_log.add_message_list(chat_log)
        token_count = 0
        for message in chat_log:
            token_count += count_tokens(message["content"], self.chat_log.model)
        finished_token_count = 0
        for message in self.chat_log.get_finished_chat_log():
            finished_token_count += count_tokens(
                message["content"], self.chat_log.model
            )
        self.assertTrue(
            finished_token_count <= self.chat_log.token_info["max_model_tokens"]
        )
    def test_user_message(self):
        self.chat_log.user_message = "Hello, how are you?"
        self.assertEqual(self.chat_log.user_message.content, "Hello, how are you?")
    def test_assistant_message(self):
        self.chat_log.assistant_message = "Hello, how are you?"
        self.assertEqual(self.chat_log.assistant_message.content, "Hello, how are you?")
    def test_save_load(self):
        """Tests that a chat log can be saved and loaded"""
        with open('test_chat_logs/random_10000.json', 'r') as f:
            test = json.load(f)
        self.chat_log.add_message_list(test)

        self.chat_log.save('test', overwrite=True)
        loaded_chat_log = ChatLog()
        loaded_chat_log.load('test')
        self.assertEqual(self.chat_log.finished_chat_log, loaded_chat_log.finished_chat_log)
        self.assertEqual(self.chat_log.full_chat_log, loaded_chat_log.full_chat_log)
    def test_bad_save_dict(self):
        """Tests that a bad save dict raises a BadSaveDictError"""
        bad_dict = {
            "hello":"world",
            "max_chat_tokens": 8000,
            "max_chat_messages": 1000,
            "max_model_tokens": 500,
        }
        self.assertRaises(BadSaveDictError, self.chat_log.save_to_dict.load, bad_dict)

    def test_reset(self):
        """Tests that the chat log can be reset"""
        with open('test_chat_logs/random_10000.json', 'r') as f:
            test = json.load(f)
        self.chat_log.add_message_list(test)
        self.chat_log.reset()
        
        self.assertEqual(self.chat_log.full_chat_log, [])
        self.assertEqual(self.chat_log.trimmed_chat_log, [])
        self.assertEqual(self.chat_log.trimmed_chat_log_tokens, 0)
        self.chat_log.reset(clear_sys_prompt=True)
        self.assertEqual(self.chat_log._sys_prompt, None)
        
       
    
    def tearDown(self):
        del self.chat_log


if __name__ == "__main__":
     unittest.main(argv=[""], verbosity=2, exit=False)

# chat = ChatLog()


# class MakeChatLog:
#     """A class to hold templates for different GPT models, and make ChatLog objects from them
#     Attributes:
#         config_templates (dict): a dictionary of templates for different GPT models
#         template_name (str): the name of the template to use
#         config (dict): the config for the template
#     Methods:
#         _get_config: gets the config for the template
#         make_ChatLog: makes a ChatLog object from the template
#         __call__: makes a ChatLog object from the template, for use as a function
#     Example Usage:
#         chat_log = MakeChatLog("gpt-3-16K")
#     Dependencies:
#         ChatLog
    
    
#     """
#     config_templates = {
#         "gpt-3-16K": dict(
#                 max_model_tokens=16000,
#                 max_completion_tokens=1000,
#                 token_padding=500,
#                 model="gpt-3",
#                 max_chat_messages=1000,
#             ),
#             "gpt-4-8K": dict(
#                 max_model_tokens=8000,
#                 model="gpt-4",
#                 max_chat_messages=400,
#                 max_completion_tokens=1000,
#                 token_padding=500,
#             )
#     }

#     def __init__(self,  template_name):
        
#         self.config = self._get_config(template_name)
#     def __call__(self, template_name):
#         return self.make_ChatLog(template_name)
    
#     def _get_config(self, template_name):
#         if template_name not in self.config_templates:
#            return None
#         config = self.config_templates[template_name]
#         return config
#     def make_ChatLog(self, template_name):
#         config = self._get_config(template_name)
#         if config is None:
#             raise ValueError(f"template_name must be one of {self.config_templates.keys()}")
#         return ChatLog(**config)

def make_chat_log(template_name: str) -> ChatLog:
    config_templates = {
        "gpt-3-16K": dict(
            max_model_tokens=16000,
            max_completion_tokens=1000,
            token_padding=500,
            model="gpt-3",
            max_chat_messages=1000,
        ),
        "gpt-4-8K": dict(
            max_model_tokens=8000,
            model="gpt-4",
            max_chat_messages=400,
            max_completion_tokens=1000,
            token_padding=500,
        )
    }

    if template_name not in config_templates:
        raise ValueError(f"template_name must be one of {config_templates.keys()}")
    
    config = config_templates[template_name]
    return ChatLog(**config)


class MessageMaker:
    """A class to make messages for a ChatLog
    Attributes:
        model_name (str): the name of the model to use
        role (str): the role of the message
    Methods:
        __call__: makes a Message object, for use as a function
    
    """
    def __init__(self, model_name: str, role: str = None) -> None:
        self.model = model_name
        self.role = role
    def __call__(self, content: str, role = None) -> Message:
        if role is None:
            role = self.role
        if role is None:
            raise ValueError("Role must be specified, either in the constructor or in the call")
        return Message(content =content, model = self.model, role = role)