import datetime
import uuid
import json
import os
import openai
import unittest

import GPTchat as g


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
        self,
        gpt_chat: g.GPTChat,
        chat_log: g.ch.ChatLog,
        save_path: str = "chatbot_saves",
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


class TestChatWrapper(unittest.TestCase):
    def setUp(self):
        pass
