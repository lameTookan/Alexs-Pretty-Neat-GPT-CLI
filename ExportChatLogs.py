import json
import os
from typing import Any, Dict, List, Optional, Set, Tuple, Union


class NoFolderError(Exception):
    def __init__(self, message: str = None):
        if message is None:
            message = "No folder specified"
        super().__init__(message)


class ChatLogExporter:
    """
    Terminology:
        ChatWrapper generates and saves .json save files. These may be referred to as chat logs, chatlog saves, or ChatWrapper saves.
        Text file exports may be called "saves", "exports", or "save files"

    This class is used to export ChatWrapper's save files to text files. Does not support importing text files into ChatWrapper.
    Designed to be used with ChatWrapper's save files, and assumes the structure is the same. Will not work with other save files, and cause errors.
    Attributes:
        - folder: str, folder where the chat logs are saved Defaults to "chatbot_saves", which is the default folder for ChatWrapper
        - save_folder: str, folder where the text files will be saved Defaults to "text_exports"
    Methods:
        Public:

            Helper methods:
                list files:
                    - list_chatlogs_files: lists all chat logs in the folder
                    - list_save_files: lists all save files in the save folder
                check if file exists:
                    - check_if_chatlog_exists: checks if a chat log exists
                    -check_if_save_file_exists: checks if a save file exists
                Read/Write Files:
                    -read_chatlog_save: reads a chat log save file, returns a dict
                    -write_save : writes a save file using a string and a file path
            Main methods:
                -export(chatlog_file, save_filename, overwrite): exports a chat log to a text file. Will overwrite existing files. Defaults to False
                -export_all(overwrite): exports all chat logs to text files. Will overwrite existing files if overwrite is true. Defaults to False

        Private:
            Formatting File Names:
                - _remove_filepath_chatlogs: removes the folder path and .json from a file path, if included
                - _add_filepath_chatlogs: adds the folder path and .json to a file path, if not included doesn't exist
                - _add_filepath_saves: adds the save folder path and .txt to a file path, if not included
                - _remove_filepath_saves: removes the save folder path and .txt from a file path, if included
            Formatting Data:
                -_check_message: checks if a message is valid, otherwise raises a type error or value error. This system is designed to work on ChatWrappers save files. Do not modify the save files, or this will not work.
                -_format_chat_list: formats a list of messages into a string
                -_format_meta : formats the meta data into a string
                -format_data: formats the data into a string
        Raises:
            - NoFolderError: Raised if chatlog folder does not exist
            - TypeError and ValueError in _check_message: raised if the message is not valid
        Dependencies:
            - os
            - json
            - typing
        Example Usage:
            exporter = ChatLogExporter()
            exporter.export_all()
            (all chat logs are exported to text files in the save folder)








    """

    def __init__(self, folder: str = "chatbot_saves", save_folder="text_exports"):
        if not folder.endswith("/"):
            folder += "/"
        if not os.path.exists(folder):
            raise NoFolderError
        self.folder = folder
        if not save_folder.endswith("/"):
            save_folder += "/"
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        self.save_folder = save_folder
        print(save_folder)

    def _remove_filepath_chatlogs(self, filepath: str) -> str:
        """Removes the folder path from the file path, if it exists."""
        if filepath.startswith(self.folder):
            filepath = filepath[len(self.folder) :]
        if filepath.endswith(".json"):
            filepath = filepath[:-5]
        return filepath

    def _add_filepath_chatlogs(self, filepath: str) -> str:
        """Adds the folder path to the file path, if it doesn't already exist.
        Same with the .json extension.
        """
        if not filepath.endswith(".json"):
            filepath += ".json"
        if not filepath.startswith(self.folder):
            filepath = self.folder + filepath
        return filepath

    def list_chatlog_files(self, remove_filepath: bool = True) -> list:
        """Lists all the files in the folder. If remove_filepath is True, the folder path is removed from the file path."""
        if remove_filepath:
            return [
                self._remove_filepath_chatlogs(file) for file in os.listdir(self.folder)
            ]
        return os.listdir(self.folder)

    def check_if_chatlog_exists(self, filename: str) -> bool:
        """Checks if a ChatLog file exists."""
        return os.path.exists(self._add_filepath_chatlogs(filename))

    def _check_message(self, message: dict) -> dict:
        """Checks if a message is valid, otherwise raises a type error or value error. This system is designed to work on ChatWrappers save files. Do not modify the save files, or this will not work."""
        if not isinstance(message, dict):
            raise TypeError(f"Expected dict, got {type(message)}")
        if "content" not in message:
            raise ValueError("Expected 'content' key in message")
        if "role" not in message:
            raise ValueError("Expected 'role' key in message")
        return message

    def _format_chat_list(self, chatlog: list[dict]) -> str:
        """Accepts the full_chat_log or trimmed_chat_log list of dictionaries(messages) from a ChatWrapper save file, and formats it into a string.
        Format:
            {role}: {content}
            ------
            ....

        """
        result = []
        for message in chatlog:
            message = self._check_message(message)
            template = "{role}: {content}" + "\n" + "-" * 5
            template = template.format(**message)
            result.append(template)
        return "\n".join(result)

    def _format_meta(self, file_title: str, data: dict) -> str:
        """Formats the metadata from a chatlog file into a string
        Takes the file title and the data dictionary, and returns a string
        """
        meta_dict = data["meta_data"]
        result = [
            "File: " + file_title,
            "Timestamp: " + meta_dict["timestamp"],
        ]
        return "\n".join(result)

    def _format_data(self, file_name, data: dict) -> str:
        """Formats the data from a chatlog file into a string
        The string is formatted as follows:
        Header:
            File: {file_name}
            Timestamp: {timestamp}
        Body:
            {role}: {content}
            Separator: ------
        Args:
            file_name (str): The name of the file to format
            data (dict): The data to format, as a dictionary. Should be result of the chat wrapper's save formatting method, or equivalent. Will cause errors if not

        """
        result = []
        header = self._format_meta(file_name, data)
        body = self._format_chat_list(data["chat_log"]["full_chat_log"])
        result.append(header)
        result.append("-" * 10)
        result.append(body)
        return "\n".join(result)

    def read_chatlog_save(self, file_name: str) -> str:
        """Gets a chatlog save dictionary from a file
        file_name (str): The name of the file to get the chatlog from, without the folder or file extension
        Raises:
            FileNotFoundError: If the file does not exist
        """
        file_name = self._add_filepath_chatlogs(file_name)
        try:
            with open(file_name, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"File {file_name} not found")
        return data

    def _add_filepath_saves(self, filepath: str) -> str:
        """
        Adds the filepath and file extension to a save file
        Used for files in the export folder, not the chatlog folder

        """
        if not filepath.endswith(".txt"):
            filepath += ".txt"
        if not filepath.startswith(self.save_folder):
            filepath = self.save_folder + filepath
        return filepath

    def _remove_filepath_saves(self, filepath: str) -> str:
        """Removes the filepath and file extension from a save file
        Used for files in the export folder, not the chatlog folder
        Returns the filepath without the folder and without the file extension
        """
        if filepath.startswith(self.save_folder):
            filepath = filepath[len(self.save_folder) :]
        if filepath.endswith(".txt"):
            filepath = filepath[:-4]
        return filepath

    def write_save(self, filename, data: str, overwrite: False) -> bool:
        """Writes a save file. Returns True if successful, False if not
        If overwrite is False, and the file already exists, returns False
        """
        filename = self._add_filepath_saves(filename)
        if os.path.exists(filename) and not overwrite:
            return False

        with open(filename, "w") as f:
            f.write(data)
        return True

    def export(
        self, chatlog_file: str, save_filename: str = None, overwrite: bool = False
    ) -> bool:
        """Export a chatlog file to a text file
        Args:
            chatlog_file (str): The name of the chatlog file to export
            save_filename (str, optional): The name of the file to save to. Defaults to None. If None, the name of the chatlog file will be used
            overwrite (bool, optional): Whether to overwrite the file if it already exists. Defaults to False.
        Raises:
            FileNotFoundError: If the chatlog file does not exist
        Returns:
            bool: Whether the file was successfully exported, that is, whether the file already existed and overwrite was False
        """
        chatlog_file = self._add_filepath_chatlogs(chatlog_file)
        if not self.check_if_chatlog_exists(chatlog_file):
            raise FileNotFoundError(f"File {chatlog_file} not found")
        data = self.read_chatlog_save(chatlog_file)
        if save_filename is None:
            save_filename = self._remove_filepath_chatlogs(chatlog_file)
        data = self._format_data(save_filename, data)
        return self.write_save(save_filename, data, overwrite=overwrite)

    def list_save_files(self, remove_filepath: bool = True) -> list:
        """Get all save files in the exports folder"""
        if remove_filepath:
            result = [
                self._remove_filepath_saves(file)
                for file in os.listdir(self.save_folder)
            ]
            print(result)
        return os.listdir(self.save_folder)

    def check_if_save_file_exists(self, filename: str) -> bool:
        """Checks if a save file exists in the exports folder"""
        return os.path.exists(self._add_filepath_saves(filename))

    def export_all(self, overwrite: bool = False) -> None:
        """Exports all chatlogs to text files"""
        for file in self.list_chatlog_files():
            self.export(file, overwrite=overwrite)


class DevMessedUpError(Exception):
    def __init__(self, message: str = None):
        if message is None:
            message = "Developer messed up, please report this bug, including the circumstances that led to this error"

        super().__init__(message)


def confirm(message: str = "Are you sure?", y_n_msg="(y/n)", yes="y", no="n") -> bool:
    print(message + y_n_msg)
    while True:
        ans = input().lower().strip()
        if ans == yes:
            return True
        elif ans == no:
            return False
        else:
            print(f"Invalid input, please enter {yes} or {no}")


class ExportChatMenu:
    def __init__(self, chatlog_folder: str = None, save_folder: str = None):
        arg_dict = {}
        if chatlog_folder is not None:
            arg_dict.update({"chatlog_folder": chatlog_folder})
        if save_folder is not None:
            arg_dict.update({"save_folder": save_folder})

        self.chatlog_exporter = ChatLogExporter(**arg_dict)

    def main_menu(self) -> None:
        """Main menu for the chatlog exporter, which allows the user to export chatlogs to text files"""
        msg_list = [
            "Welcome to the chat log exporter",
            "Here, you can export a chatlog to a text file",
            "Options:",
            "Type 'export' to  export  a chatlog",
            "Type 'list' to list  all chatlog saves",
            " Type 'export all' to export all chatlogs",
            "Type q to exit",
            "Type h to show this message again",
        ]
        message = "\n".join(msg_list)
        print(message)
        while True:
            ans = input("> ")
            ans_lower = ans.lower().strip()
            if ans_lower == "q":
                print("Exiting...")
                return None
            elif ans_lower == "h":
                print(message)
            elif ans_lower in ("export", "e"):
                self.save_menu()
                print(message)
            elif ans_lower in ("list", "l"):
                print("Listing...")
                print("\n".join(self.chatlog_exporter.list_chatlog_files()))
                print(message)
            elif ans_lower in ("export all", "e a"):
                if confirm("Overwrite any existing files?"):
                    print("Exporting all...")
                    print("This may take a while...")
                    self.chatlog_exporter.export_all(overwrite=True)
                else:
                    print("Exporting all while skipping any existing files...")
                    print("This may take a while...")
                    self.chatlog_exporter.export_all(overwrite=False)
                print(message)
            else:
                print("Invalid input")
                print(message)

    def save_menu(self) -> None:
        """Save menu for the chatlog exporter, which allows the user to choose a chatlog to export"""
        msg_list = [
            "Choose a file to export",
            "Type q to exit",
            "Type h to show this message again",
        ]
        files_list = self.chatlog_exporter.list_chatlog_files()
        message = "\n".join(msg_list)
        files = "\n".join(files_list)

        print(message)
        print("Files:")
        print(files)
        while True:
            ans = input("> ")
            ans_lower = ans.lower().strip()
            if ans_lower in ("q", "quit"):
                print("Exiting...")
                return None
            elif ans_lower in ("h", "help"):
                print(message)
            elif self.chatlog_exporter.check_if_chatlog_exists(ans):
                filename, overwrite = self.choose_save_name_menu()
                if filename is None:
                    print("Exiting Chat Log Exporter...")
                    return None
                if self.chatlog_exporter.export(
                    chatlog_file=ans, save_filename=filename, overwrite=overwrite
                ):
                    print("Exported successfully")
                else:
                    raise DevMessedUpError(
                        "Error when exporting file. Please report to the developer that something is wrong with the chat log exporter, specifically the export function"
                    )
                if confirm("Do you want to export another file?"):
                    print()
                    print(message)
                else:
                    return None

    def choose_save_name_menu(self) -> tuple[str, bool]:
        """
        Menu for choosing a name for the save file
        Returns:
            tuple[str, bool]:
                str: The name of the save file, or None if the user wants to exit
                bool: True if the user wants to overwrite the file, False otherwise
        """

        msg_list = [
            "Choose a name for the file",
            "Type nothing to use the default name(the name of the chatlog)",
            "Type q to exit",
            "Type h to show this message again",
        ]

        def get_save_files():
            return self.chatlog_exporter.list_save_files(remove_filepath=True)

        save_intro = "List of save files: \n"
        save_message = save_intro + "\n".join(get_save_files())
        message = "\n".join(msg_list)
        print(message)
        print(save_message)
        while True:
            ans = input("> ")
            ans_lower = ans.lower().strip()
            if ans_lower in ("q", "quit"):
                print("Exiting...")
                return None, False
            elif ans_lower in ("h", "help"):
                print(message)
            elif ans_lower in ("", "default"):
                return "default", False
            elif self.chatlog_exporter.check_if_save_file_exists(ans_lower):
                print("File already exists, overwrite? (y/n)")
                while True:
                    confirm = input("> ").lower().strip()
                    if confirm in ("y", "yes"):
                        return ans_lower, True
                    elif confirm in ("n", "no"):
                        print("Choose another name")
                        break
                    else:
                        print("Choose y or n")
            else:
                return ans_lower, False


export_chat_menu = ExportChatMenu()
