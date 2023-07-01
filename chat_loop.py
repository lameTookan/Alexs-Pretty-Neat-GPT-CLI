import datetime
import json
import os
import random
import sys

import openai
import tiktoken
from typing import Any, Dict, List, Optional, Set, Tuple, Union
from settings import API_KEY, DEFAULT_MODEL, DEFAULT_TEMPLATE_NAME

import object_factory as fact
import misc.MyStuff as ms


def split_input_from_cmd(cmd: str, string: str) -> str:
    if cmd in string:
        return string.split(cmd)[1].strip()
    else:
        return None


def format_dict_as_string(d: dict, delim: str = ": ", title_case=False) -> str:
    """Formats a dictionary as a string with each key-value pair on a new line, separated by a delimiter.
    Does the same for nested dictionaries. Nested tuples, lists, and sets are also supported are separated by commas.
    """

    result = []
    for key, value in d.items():
        key = key.title() if title_case else key
        if isinstance(value, dict):
            item = []
            item.append(key)
            for k, v in value.items():
                k = k.title() if title_case else k
                item.append(f">>{k}{delim}{v}")

            value = "\n".join(item)
        elif (
            isinstance(value, list)
            or isinstance(value, tuple)
            or isinstance(value, set)
        ):
            value = [key] + [f"{v}" for v in value]
            value = ", ".join(value)
        else:
            value = f"{key}{delim}{value}"
        result.append(value)
    return "\n".join(result)


def toggle(input: bool):
    if input == True:
        return False
    else:
        return True


def bool_to_yes(val: bool, y="yes", n="no") -> str:
    if val:
        return y
    else:
        return n


def chunk_input(ini_message: str = "Type enter twice when done.", input_message="> "):
    print(ini_message)
    input_list = []
    while True:
        ans = input(input_message)
        if ans == "":
            break
        input_list.append(ans)
    return " ".join(input_list)


def confirm(message: str = "Are you sure?", y_n="(y/n)", y="y", n="n") -> bool:
    print(message + " " + y_n)
    while True:
        ans = input("> ")
        if ans.lower() == y:
            return True
        elif ans.lower == n:
            return False
        else:
            print("Invalid input. Please try again.")


class ChatLoop:
    def __init__(self, chat_wrapper: fact.cw.ChatWrapper, chunking=True):
        self.chat_wrapper: fact.cw.ChatWrapper = chat_wrapper
        self.chunking = chunking
        self.chat_log: fact.cw.g.ch.ChatLog = chat_wrapper.chat_log
        self.gpt_chat: fact.cw.g.GPTChat = chat_wrapper.gpt_chat

    def run_chat_loop(self):
        msg_list = [
            "Welcome to the chatbot!",
            "Type 'quit' to quit(and return to main menu)",
            "Type 'save' to save the chat log",
            "Type 'load' to load a chat log from the save folder",
            "Type 'clear' to clear the chat log",
            "Type 'help' to see this message again",
            "Type chunk to turn off/on input chunking(useful in linux/macOS)",
        ]
        message = "\n".join(msg_list)
        print(message)

        while True:
            if self.chunking:
                ans = chunk_input()
            else:
                ans = input("> ")
            ans_lower = ans.lower()
            if ans_lower in ("quit", "exit", "q"):
                if confirm("Are you sure you want to quit?"):
                    print("Quitting...")
                    break
            elif ans_lower in ("save", "s"):
                self.save_menu()
                print("Returning to the chat loop...")
                continue
            elif ans_lower in (
                "clear",
                "r",
                "reset",
            ):
                if confirm(
                    "Are you sure you want to clear the chat log? You cannot undo this. "
                ):
                    self.chat_log.reset()
                    print("Chat log cleared.")
                else:
                    print("Chat log not cleared.")
            elif ans_lower in ("help", "h"):
                print(message)
            elif ans_lower in ("c", "chunk"):
                print("Toggling chunking")
                self.chunking = toggle(self.chunking)
            elif ans_lower in ("load", "l"):
                print("Loading menu...")
                self.load_menu()
                if self.chat_wrapper.is_loaded:
                    print(self.chat_wrapper.chat_log.get_pretty_messages())
            elif ans_lower == "debug":
                print("Printing debug info...")
                print(self.chat_wrapper.__repr__())
            elif ans_lower == "nicki":
                print(ms.nicki_minaj)
            elif ans_lower in ("params", "p"):
                self.modify_model_param_menu()
            else:
                if ans == "" or ans == " " or ans== None:
                    ans = "User did not enter a message"
                response = self.chat_wrapper.chat_with_assistant(ans)
                print(response)

    def load_menu(self):
        msg_list = [
            "Type a filename to load a chat log",
            "As per usual, type 'quit' to quit(and return to main menu)",
            "Type help to see this message again",
            "Type list to see a list of files in the current directory",
        ]
        file_list = self.chat_wrapper.save_and_load.get_files(remove_path=True)
        files = "\n".join(
            ["The following is a list of currently saved_files: "] + file_list
        )
        message = "\n".join(msg_list)
        print(message)
        print(files)
        while True:
            ans = input("> ")
            ans_lower = ans.lower()
            if ans_lower in ("quit", "q"):
                if confirm("Are you sure you want to quit?"):
                    print("Returning to previous menu...")
                    break
                else:
                    print("Not quitting. Type 'help' to see the help message again.")
            elif ans_lower in ("help", "h"):
                print(message)
            elif ans_lower in ("list", "l"):
                print(files)
            else:
                if ans in file_list:
                    print(f"Loading {ans}...")
                    if confirm(
                        "Are you sure you want to load from this file? Any previous chat will be overwritten."
                    ):
                        self.chat_wrapper.load(ans)
                        print("Chat loaded. Returning to previous menu...")
                        return True
                    else:
                        print("Chat not loaded.")
                        print("Returning to previous menu...")
                        continue
                else:
                    print("File not found. Please try again.")

    def save_menu(self):
        msg_list = [
            "Type a filename for the chat log save file",
            "Type 'quit' to quit(and return to main menu)",
            "If the file already exists, you will be asked to confirm overwriting it"
            "Type help to see this message again",
            "Type enter to save chat log with a timestamp as the filename",
            "The following is a list of files in the current directory:",
        ]
        file_list = self.chat_wrapper.save_and_load.get_files(remove_path=True)
        msg_list.extend(file_list)
        msg = "\n".join(msg_list)
        print(msg)
        while True:
            ans = input("> ")
            if ans.lower() in ("quit", "q"):
                if confirm("Are you sure you want to quit?"):
                    break
            elif ans.lower() in ("help", "h"):
                print(msg)
            else:
                if self.chat_wrapper.save(file_name=ans):
                    print("Save successful!")
                    print("Returning to main menu...")
                    break
                else:
                    if confirm(
                        f"File: {ans} already exists. Are you sure you want to overwrite it?"
                    ):
                        if self.chat_wrapper.save(file_name=ans, overwrite=True):
                            print("Save successful!")
                            print("Returning to main menu...")
                            break
                        else:
                            print("Save failed. Please try again.")
                            continue
                    else:
                        print("Save failed. Please try again.")
                        continue

    def modify_model_param_menu(self) -> None:
        msg_list = [
            "Welcome to the model parameter modification menu!",
            "Explore different parameters to impact the chatbot's responses.",
            "'quit': Exit and return to main menu.",
            "'help': Display this help message again.",
            "'default': Reset all parameters to default values.",
            "'list': Display a list of all parameters.",
            "'set {parameter_name}': Set a specific parameter. Must use the exact parameter name.",
            "'param_help {parameter_name}': Get a description of a specific parameter. Use without a parameter name for a list of all parameters and their descriptions.",
        ]

        current_params_list = [
            f"{key}: {value}"
            for key, value in self.chat_wrapper.gpt_chat.get_params().items()
        ]
        msg = "\n".join(msg_list)
        current_params = "\n".join(current_params_list)
        print(msg)
        print("Current parameters:")
        print(current_params)
        possible_params = self.gpt_chat.possible_optional_params
        param_help_dict = self.gpt_chat.param_help

        while True:
            ans = input("> ")
            ans_lower = ans.lower()
            if ans_lower in ("q", "quit", "exit"):
                print("Returning to main menu...")
                break
            elif ans_lower in ("help", "h"):
                print(msg)
            elif ans_lower in ("list", "l"):
                print("Possible parameters:", " ".join(list(possible_params)))
                print("Current parameters:")
                print(current_params)
            elif ans_lower.startswith("param_help"):
                param = split_input_from_cmd("param_help", ans_lower)
                if param is None or param == "" or param not in possible_params:
                    print("Possible parameters:", " ".join(list(possible_params)))
                    print("Descriptions:")
                    print(format_dict_as_string(param_help_dict))
                else:
                    print(param_help_dict[param])
            elif ans_lower.startswith("set"):
                param = split_input_from_cmd("set", ans_lower)
                param = param.strip()
                if param is None or param not in possible_params:
                    print("Invalid parameter. Please try again.")
                    print("Possible parameters:", " ".join(list(possible_params)))
                else:
                    param = param.strip()
                    value = input(f"Enter a value for {param}: ")
                    try:
                        self.gpt_chat.modify_params(param = value)
                    except fact.cw.g.BadChatCompletionParams as e:
                        print("Invalid Parameter. More info:")
                        print(e)
                        continue
                    print("Parameter set successfully!")
                    print("Current parameters:")
                    print(current_params)
            elif ans_lower == "default":
                if confirm("Are you sure you want to reset all parameters?"):
                    self.gpt_chat.reload_from_template()
                    print("Parameters reset successfully!")
                    print("Current parameters:")
                    print(current_params)
            else:
                print("Invalid command. Please try again.")
                


class MainMenu:
    def __init__(
        self, API_KEY=API_KEY, factory: fact.ChatWrapperFactory = fact.wrapper_factory
    ):
        self.API_KEY = API_KEY
        self.factory: fact.ChatWrapperFactory = factory
        self.selected_template_name = DEFAULT_TEMPLATE_NAME
        self.factory.select_template(self.selected_template_name)
        self.is_default_template = True
        self.chat_wrapper: fact.cw.g.GPTChat = None
        self.is_ready = False
        self.template_selector = self.factory.template_selector

    def _get_template_info(self, template_name: str) -> str:
        info = self.template_selector.get_template_info(template_name)
        for key, value in info.items():
            print(f"{key}: {value}")

    def template_menu(self) -> None:
        def format_template_dict_as_string(name: str, template_dict: dict) -> str:
            result = []
            result.append(f"Template Name: {name}")
            result.append("Description: " + template_dict["description"])
            result.append("Tags: " + ", ".join(template_dict["tags"]))
            result.append("ChatLog  Parameters:")

            for key, value in template_dict["chat_log"].items():
                result.append(f"{key.title()}: {value}")
            result.append("Completion Parameters:")
            for key, value in template_dict["gpt_chat"].items():
                result.append(f"{key.title()}: {value}")
            return "\n".join(result)

        msg_list = [
            "Welcome to the template menu!",
            "Type 'quit' to quit(and return to main menu)",
            "Type 'help' to see this message again",
            "Type list to see a list of all templates",
            "Type 'set {template_name}' to set the template",
            "Type 'info {template_name}' to see info about a specific template",
            "Type 'current' to see the current template",
        ]
        current_temp_info_list = [
            "Current Selected Template Name: " + self.selected_template_name,
            "Is Default Template: " + bool_to_yes(self.is_default_template),
            "Current Template Info:",
            format_dict_as_string(
                self.template_selector.get_template_info(self.selected_template_name)
            ),
        ]
        all_templates_dict = self.template_selector.get_all_templates()

        all_template_info = [
            format_template_dict_as_string(name, template_dict)
            for name, template_dict in all_templates_dict.items()
        ]
        message = "\n".join(msg_list)

        current_temp_info = "\n".join(current_temp_info_list)

        available_templates = ", ".join(list(all_templates_dict.keys()))
        print(ms.magenta("===( Current Template Info )==="))
        print(current_temp_info)
        print("---" * 10)
        print(ms.magenta("===( Template Menu )==="))

        print(message)

        print("Available Templates: " + available_templates)
        while True:
            ans = input("> ")
            ans_lower = ans.lower()
            if ans_lower in ("q", "quit", "exit"):
                print("Returning to main menu...")
                break
            elif ans_lower in ("help", "h"):
                print(message)
            elif ans_lower in ("list", "l"):
                print("Available Templates: " + available_templates)
            elif ans_lower.startswith("info"):
                cmd = split_input_from_cmd("info", ans_lower)
                if cmd is None:
                    print("Printing info for all templates...")
                    print(all_template_info)
                elif cmd in all_templates_dict.keys():
                    print(format_template_dict_as_string(cmd, all_templates_dict[cmd]))
                else:
                    print("Invalid template name. Please try again.")
                    print("Available Templates: " + available_templates)
                    continue
            elif ans_lower.startswith("set"):
                cmd = split_input_from_cmd("set", ans_lower)
                if cmd is None:
                    print("Invalid template name. Please try again.")
                    print("Available Templates: " + available_templates)
                    continue
                elif cmd not in all_templates_dict.keys():
                    print("Invalid template name. Please try again.")
                    print("Available Templates: " + available_templates)
                    continue
                else:
                    if confirm(
                        "Are you sure you want to set the template to " + cmd + "?"
                    ):
                        self.selected_template_name = cmd
                        self.factory.select_template(self.selected_template_name)
                        self.is_default_template = False
                        print("Template set successfully!")
                        print("Current Template Info:")
                        print(
                            format_dict_as_string(
                                self.template_selector.get_template_info(
                                    self.selected_template_name
                                )
                            )
                        )
                        print(
                            "Is Default Template: "
                            + bool_to_yes(self.is_default_template)
                        )
                    else:
                        print("Template not set.")
                        print(
                            "Type 'set {template_name}' to set the template, or 'quit' to quit."
                        )
                        continue
            elif ans_lower.startswith("current"):
                print("Current Selected Template Name: " + self.selected_template_name)
                print("Is Default Template: " + bool_to_yes(self.is_default_template))
                print("Current Template Info:")
                print(
                    format_dict_as_string(
                        self.template_selector.get_template_info(
                            self.selected_template_name
                        )
                    )
                )
            else:
                print("Invalid command. Please try again.")
                continue

    def modify_system_prompt(self) -> None:
        print("Coming soon...")

    def _make_chat_wrapper(self):
        self.factory.select_template(self.selected_template_name)
        self.chat_wrapper = self.factory.make_chat_wrapper()
        self.is_ready = True


class SystemPromptManager:
    def __init__(
        self,
        sys_info_dict=fact.cw.g.ch.ChatLog.system_prompt_wildcards,
        save_folder="system_prompts",
    ):
        self.sys_info_dict = sys_info_dict
        save_folder = (
            save_folder + "/" if not save_folder.endswith("/") else save_folder
        )
        if not os.path.exists(save_folder):
            os.mkdir(save_folder)
        self.save_folder = save_folder

    def add_file_path(self, file_name: str) -> str:
        if not file_name.endswith(".txt"):
            file_name = file_name + ".txt"
        if not file_name.startswith(self.save_folder):
            file_name = self.save_folder + file_name
        return file_name

    def remove_file_path(self, file_name: str) -> str:
        if file_name.startswith(self.save_folder):
            file_name = file_name[len(self.save_folder) :]
        if file_name.endswith(".txt"):
            file_name = file_name[:-4]
        return file_name

    def _read_file(self, file_name: str) -> str:
        file_name = self._add_file_path(file_name)
        with open(file_name, "r") as f:
            return f.read()

    def write_file(self, file_name: str, text: str, overwrite=False) -> bool:
        file_name = self._add_file_path(file_name)
        if os.path.exists(file_name) and not overwrite:
            return False
        with open(file_name, "w") as f:
            f.write(text)
        return True

    def get_file_names(self) -> List[str]:
        return [
            self._remove_file_path(file_name)
            for file_name in os.listdir(self.save_folder)
        ]

    def get_wildcard_info(self) -> str:
        result = []
        for key, value in self.sys_info_dict.items():
            result.append(key + ": " + value["description"])
        return "\n".join(result)


class SysPromptManagerMenu:
    def __init__(self, sys_prompt_manager: SystemPromptManager):
        self.sys_prompt_manager = sys_prompt_manager
        self.loaded_file = None

    def load_menu(self):
        msg_list = [
            "Welcome to the System Prompt Loading Menu!",
            "Type 'help' to see this message again.",
            "Type 'list' to see a list of all available system prompts.",
            "Type view {file_name}' to view a system prompt.",
            "Type 'load {file_name}' to load a system prompt.",
            "Type remove {file_name}' to remove a system prompt.",
            "Type quit to return to the main menu.",
        ]
        message = "\n".join(msg_list)
        files_list = self.sys_prompt_manager.get_file_names()

        print(message)
        file_msg = (
            "System Prompts in Folder:"
            + "------\n"
            + "\n".join(files_list)
            + "\n"
            + "------"
        )
        while True:
            ans = input("> ")
            ans_lower = ans.lower()
            if ans_lower in ("q", "quit", "exit"):
                if confirm("Are you sure you want to quit?"):
                    print("Returning to main menu...")
                    return None
                else:
                    continue
            elif ans_lower in ("help", "h"):
                print(message)
            elif ans_lower in ("list", "ls", "l"):
                print(file_msg)
            elif ans_lower.startswith("view"):
                filename = split_input_from_cmd("view", ans)
                if filename is None or filename not in files_list:
                    print("Invalid file name. Please try again.")
                    continue
                else:
                    print(self.sys_prompt_manager._read_file(filename))
            elif ans_lower.startswith("load"):
                print("Loading system prompt...")
                self.loaded_file = self.sys_prompt_manager._read_file(filename)
                print("System prompt loaded successfully!")
                return self.loaded_file

            elif ans_lower.startswith("remove"):
                if split_input_from_cmd("remove", ans) in files_list:
                    if confirm("Are you sure you want to remove this system prompt?"):
                        os.remove(self.sys_prompt_manager.add_file_path(filename))
                        print("System prompt removed successfully!")
                    else:
                        print("System prompt not removed.")
                else:
                    print("Invalid file name. Please try again.")
                    continue
            else:
                print("Invalid command. Please try again.")

    def save_menu(self):
        msg_list = [
            "Welcome to the System Prompt Saving Menu!",
            "Type 'help' to see this message again.",
            "Type 'list' to see a list of all available system prompts.",
            "Type 'view {file_name}' to view a system prompt.",
            "Type quit to return to the main menu.",
            "Type remove {file_name}' to remove a system prompt.",
            "Please note that you can also save new system prompts by adding them to the system_prompts folder, as .txt files."
            "Otherwise, type  a file name to save a new system prompt. ",
        ]
        files = "\n".join(self.sys_prompt_manager.get_file_names())
        files_list = self.sys_prompt_manager.get_file_names()
        message = "\n".join(msg_list)
        print(message)
        print("System Prompts in Folder:" + "------\n" + files + "\n" + "------")
        while True:
            ans = input("> ")
            ans_lower = ans.lower()
            if ans_lower in ("q", "quit"):
                if confirm("Are you sure you want to quit?"):
                    print("Returning to main menu...")
                    break
                else:
                    continue
            elif ans_lower in ("help", "h"):
                print(message)
            elif ans_lower in ("list", "ls", "l"):
                print(files)
            elif ans_lower.startswith("view"):
                filename = split_input_from_cmd("view", ans)
                if filename is None or filename not in files_list:
                    print("Invalid file name. Please try again.")
                    continue
                else:
                    print(self.sys_prompt_manager._read_file(filename))
            elif ans_lower.startswith("remove"):
                filename = split_input_from_cmd("remove", ans)
                if filename is None or filename not in files_list:
                    print("Invalid file name. Please try again.")
                    continue
                else:
                    if confirm(f"Are you sure you want to delete {filename}?"):
                        os.remove(self.sys_prompt_manager.add_file_path(filename))
                        print("System prompt removed successfully!")
                    else:
                        print("System prompt not removed.")
                        continue
            else:
                if confirm(
                    f"Are you sure you want to write a new system prompt to filename {ans}?"
                ):
                    if ans in files_list:
                        if confirm(f"Are you sure you want to overwrite {ans}?"):
                            over_write = True

                        else:
                            print("System prompt not saved.")
                            continue
                    else:
                        over_write = False
                    txt = self.write_file_menu(ans)
                    if txt is False:
                        continue
                    else:
                        self.sys_prompt_manager.write_file(ans, txt, over_write)
                        print("System prompt saved successfully!")

    def write_file_menu(
        self,
        filename: str,
    ) -> str:
        print("To quit without saving, enter 'q' or 'quit'.")
        while True:
            print("You can use the following wildcards in your system prompt:")
            print(self.sys_prompt_manager.get_wildcard_info())
            ans = chunk_input(
                "Please input the text you would like to save. Double tap enter to save."
            )
            if ans is None:
                print("Invalid input. Please try again.")
            if ans.lower() in ("q", "quit"):
                if confirm("Are you sure you want to quit?"):
                    print("Returning to main menu...")
                    return False
                else:
                    continue
            else:
                print(
                    "Are you sure you want to save the following system prompt as "
                    + filename
                    + "?"
                )
                print(ms.yellow(ans))
                confirm = input("y/n > ").lower()
                if confirm.lower() in ("y", "yes"):
                    return ans

                else:
                    print(
                        "System prompt not saved. Type 'q' or 'quit' to quit without saving."
                    )
                    continue

    def main_menu(self) -> None | str:
        if self.loaded_file is not None:
            print("Loaded system prompt: " + self.loaded_file)
        msg_list = [
            "Welcome to the System Prompt Manager!",
            "Type 'help' to see this message again.",
            "Type 'load' to enter the system prompt loading menu.",
            "Type 'save' to save a system prompt.",
            "Type 'quit' to exit the manager.",
        ]
        message = "\n".join(msg_list)
        print(message)
        while True:
            ans_lower = input("> ").lower()
            if ans_lower in ("q", "quit"):
                if confirm("Are you sure you want to quit?"):
                    print("Exiting...")
                    return None
                else:
                    continue
            elif ans_lower in ("help", "h"):
                print("\n".join(message))
            elif ans_lower in ("load", "l"):
                prompt = self.load_menu()
                if prompt is not None:
                    print("Loaded system prompt: " + prompt)
                    print("Returning to main menu...")
                    self.loaded_file = prompt
                    return prompt
                else:
                    print("No system prompt loaded. Type quit to exit.")
                    continue
            elif ans_lower in ("save", "s"):
                self.save_menu()
                continue
            else:
                print("Invalid command. Please try again.")


if __name__ == "__main__":
    fact.wrapper_factory.select_template(DEFAULT_TEMPLATE_NAME)
    wrapper = fact.wrapper_factory.make_chat_wrapper()

    chat_loop = ChatLoop(wrapper)
    chat_loop.run_chat_loop()
