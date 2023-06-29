import sys
import os
import datetime
import openai
import tiktoken
import json
import random
import ChatHistory as ch
import GPTchat as g

def format_dict_as_string(d: dict, delim: str = ": ") -> str:
    result = []
    for key, value in d.items():
        result.append(f"{key}{delim}{value}")
    return "\n".join(result)
def toggle(input: bool):
    if input == True:
        return False
    else:
        return True


def chunk_input(ini_message: str = "Type enter twice when done.", input_message="> "):
    print(ini_message)
    input_list = []
    while True:
        ans = input(input_message)
        if ans == "":
            break
        input_list.append(ans)
    return input_list


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
    def __init__(self, chat_wrapper: g.ChatWrapper, chunking=True):
        self.chat_wrapper = chat_wrapper
        self.chunking = chunking
        self.chat_log = chat_wrapper.chat_log
        self.gpt_chat = chat_wrapper.gpt_chat

    def run_chat_loop(self):
        msg_list = [
            "Welcome to the chatbot!",
            "Type 'quit' to quit(and return to main menu)",
            "Type save to save the chat log",
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
                    break
            elif ans_lower == "save":
                # add save menu here
                pass
            elif ans_lower in (
                "clear",
                "r",
                "reset",
            ):
                self.chat_log.reset()
            elif ans_lower in ("help", "h"):
                print(message)
            elif ans_lower in ("c", "chunk"):
                print("Toggling chunking")
                self.chunking = toggle(self.chunking)
            else:
                response = self.chat_wrapper.chat_with_assistant(ans)

    def save_menu(self):
        msg_list = [
            "Type a filename for the chat log save file",
            "Type 'quit' to quit(and return to main menu)",
            "If the file already exists, you will be asked to confirm overwriting it"
            "Type help to see this message again",
            "Type enter to save chat log with a timestamp as the filename",
            "The following is a list of files in the current directory:",
        ]
        file_list = self.chat_wrapper.save_and_load._get_files(remove_path=True)
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
                if self.chat_wrapper.save(filename=ans):
                    print("Save successful!")
                    print("Returning to main menu...")
                    break
                else:
                    if confirm(
                        f"File: {ans} already exists. Are you sure you want to overwrite it?"
                    ):
                        if self.chat_wrapper.save(filename=ans, overwrite=True):
                            print("Save successful!")
                            print("Returning to main menu...")
                            break
                        else:
                            print("Save failed. Please try again.")
                            continue

    def modify_model_param_menu(self) -> None:
        def split_input_from_cmd(cmd: str, string:str) -> str:
            if cmd in string:
                return string.split(cmd)[1].strip()
            else:
                return None
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
        possible_params = self.gpt_chat. possible_optional_params
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
                        self.gpt_chat.modify_params()
                    except g.BadChatCompletionParams as e:
                       print("Invalid Parameter. More info:")
                       print(e)
                       continue
                    print("Parameter set successfully!")
                       
                        
                


class MainMenu:
    def __init__(self):
        pass

    def _make_chat_log(self):
        pass

    def _make_chat_wrapper(self):
        pass

    def _make_gpt_chat(self):
        pass

    def _make_chat_loop(self):
        pass
