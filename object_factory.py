import sys
import unittest
import os
import datetime
import time
import openai
import tiktoken
import json
import random

import GPTchat as g
import ChatHistory as ch
from typing import List, Dict, Tuple, Set, Union, Optional, Any

from super_secret import OPENAI_API_KEY as API_KEY

templates = {
        "gpt-4_default": {
            "chat_log": {
                "model": "gpt-4",
                "max_model_tokens": 8000,
                "max_completion_tokens": 1000,
                "max_chat_messages": 1000,
                "token_padding": 500,
            },
            "gpt_chat": {
                "model_name": "gpt-4",
                "max_tokens": 1000,
                "temperature": 1.1,
                "top_p": 1.0,
                "frequency_penalty": 0.5,
            },
            "description": "Default settings for gpt-4",
            "tags": {"gpt-4", "default", "normal"},
        },
        "gpt-4_small": {
            "chat_log": {
                "model": "gpt-4",
                "max_model_tokens": 8000,
                "max_completion_tokens": 1000,
                "max_chat_messages": 50,
                "token_padding": 500,
            },
            "gpt_chat": {
                "model_name": "gpt-4",
                "max_tokens": 1000,
                "temperature": 0.5,
                "top_p": 1.0,
            },
            "description": "To save money on tokens use this to limit the number of messages to 50",
            "tags": {"gpt-4", "small", "cheap", "low-cost"},
        },
        "gpt-4_creative": {
            "chat_log": {
                "model": "gpt-4",
                "max_model_tokens": 8000,
                "max_completion_tokens": 1000,
                "max_chat_messages": 1000,
                "token_padding": 500,
            },
            "gpt_chat": {
                "model_name": "gpt-4",
                "max_tokens": 1000,
                "temperature": 1.5,
            },
            "description": "Use this to get more creative responses, higher temperature means more creative",
            "tags": {"gpt-4", "creative", "high-temperature"},
            "gpt-3_16K_default": {
                "chat_log": {
                    "model": "gpt-3",
                    "max_model_tokens": 16000,
                    "max_completion_tokens": 2000,
                    "max_chat_messages": 2000,
                    "token_padding": 500,
                },
                "gpt_chat": {
                    "model_name": "gpt-3-16K",
                    "max_tokens": 2000,
                    "temperature": 0.5,
                },
                "description": "Default settings for gpt-3-16K",
                "tags": {"gpt-3-16K", "default", "normal", "gpt-3"},
            },
        
        },
    }

class ChatLogAndGPTChatFactory:
    templates = templates

    def __init__(self, API_KEY):
        self.API_KEY = API_KEY
        self.selected_template = None
    def search_by_tag(self, tag: str) -> set:
        results =  {key:template for key,template in self.templates.items() if tag in template["tags"]}
        if len(results) == 0:
            return set()
        return set(results.keys())
    def select_template(self, template_name: str) -> dict:
        
        self.selected_template = self.templates.get(template_name, None)
        return self.selected_template
    def _make_chat_log(self, chat_log_settings: dict, template_name: str = None) -> ch.ChatLog:
        chat_log_settings.update({"template": template_name})
        return ch.ChatLog(**chat_log_settings)
    def _make_gpt_chat(self,  gpt_chat_settings: dict, template_name: str = None) -> g.GPTChat:
       settings = gpt_chat_settings.copy()
       settings.update({
              "API_KEY": self.API_KEY,
              'template': template_name,
       })
       gpt_chat =  g.GPTChat(**settings)
    
    def make_chat_log_and_gpt_chat(self) -> tuple[ch.ChatLog, g.GPTChat]:
        if self.selected_template is None:
            raise Exception("No template selected")
        chat_log = self._make_chat_log(self.selected_template["chat_log"])
        gpt_chat = self._make_gpt_chat(self.selected_template["gpt_chat"])
        return (chat_log, gpt_chat)
    
    
factory = ChatLogAndGPTChatFactory(API_KEY)
factory.select_template("gpt-4_default")
chat_log, gpt_chat = factory.make_chat_log_and_gpt_chat()
print(repr(chat_log))
print(gpt_chat)
