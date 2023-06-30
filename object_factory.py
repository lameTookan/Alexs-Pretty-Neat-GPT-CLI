import sys
import unittest
import os
import datetime
import time
import openai
import tiktoken
import json
import random
from templates import template_selector, GetTemplates

import chat_wrapper as cw
from typing import List, Dict, Tuple, Set, Union, Optional, Any

from super_secret import OPENAI_API_KEY as API_KEY


class NoTemplateSelectedError(Exception):
    def __init__(self, message: str = None):
        if message is None:
            message = "No template selected"
        super().__init__(message)
class ChatLogAndGPTChatFactory:
    """T
    his class is used to make ChatLog and GPTChat objects from templates
    Relies on:
        - template_selector: GetTemplates can use custom instance of this class (Separate instances might be working with a different set of templates, but functionality is the same)
        - GPTChat: GPTChat class from GPTchat.py
        - ChatLog: ChatLog class from ChatHistory.py
    Attributes:
        - API_KEY: OpenAI API key, required to make GPTChat objects
        - template_selector: GetTemplates object, used to get templates
        - selected_template: dict, selected template, selected in the select_template method
        
    Methods:
        - select_template(template_name: str): selects a template from the template_selector, by name
        - _make_chat_log: makes a ChatLog object from a template
        - _make_gpt_chat: makes a GPTChat object from a template
        - make_chat_log_and_gpt_chat: makes a ChatLog and GPTChat object from a template, returns a tuple of them
    Example Usage:
        template_name = template_selector.search_by_tag("gpt-4")[0]
        factory = ChatLogAndGPTChatFactory(API_KEY)
        factory.select_template(template_name)
        chat_log, gpt_chat = factory.make_chat_log_and_gpt_chat()
         
    """

    def __init__(self, API_KEY, template_selector: GetTemplates= template_selector  ):
        self.API_KEY = API_KEY
        self.template_selector = template_selector
        self.selected_template = None
        
    def select_template(self, template_name: str) -> None:
        self.selected_template = self.template_selector.get_template(template_name)
    
    
    def _make_chat_log(self,template: dict) -> cw.g.ch.ChatLog:
        """Makes a ChatLog object from a template"""
        settings: dict = template['chat_log']
      
        chat_log =cw.g.ch.ChatLog(**settings)
        return chat_log
    def _make_gpt_chat(self,  template: dict) -> cw.g.GPTChat:
        """Makes a GPTChat object from a template"""
        settings: dict  = template['gpt_chat']
        settings.update({"API_KEY": self.API_KEY, 
                        "template": template
                        })
        gpt_chat =  cw.g.GPTChat(**settings)
        return gpt_chat
       
    
    def make_chat_log_and_gpt_chat(self) -> tuple[cw.g.ch.ChatLog, cw.g.GPTChat]:
        """Makes a ChatLog and GPTChat object from a template, returns a tuple of them"""
        if self.selected_template is None:
            raise  NoTemplateSelectedError()
        chat_log = self._make_chat_log(self.selected_template)
        gpt_chat = self._make_gpt_chat(self.selected_template)
        return (chat_log, gpt_chat)
    
class TestChatLogAndGPTChatFactory(unittest.TestCase):
    def setUp(self):
        self.factory = ChatLogAndGPTChatFactory(API_KEY)
        self.template_selector = template_selector
        self.test_template = template_selector.get_template("gpt-4_default")
        self.test_template_name = 'gpt-4_default'
        
    def test_select_template(self):
        """Tests that the select_template method works"""
        template_name = self.factory.template_selector.search_templates_by_tag("gpt-4")[0]
        self.factory.select_template(template_name)
        self.assertIsNotNone(self.factory.selected_template)
    def test_make_chat_log(self):
        """Tests that the _make_chat_log method works"""
        template_name = self.test_template_name
        self.factory.select_template(template_name)
        chat_log = self.factory._make_chat_log(self.test_template)
        self.assertIsInstance(chat_log,cw.g.ch.ChatLog)
    def test_make_gpt_chat(self):
        """Tests that the _make_gpt_chat method works"""
        template_name = self.test_template_name
        self.factory.select_template(template_name)
        gpt_chat = self.factory._make_gpt_chat(self.factory.selected_template)
        self.assertIsInstance(gpt_chat, cw.g.GPTChat)
    def test_make_chat_log_and_gpt_chat(self):
        """Tests that the make_chat_log_and_gpt_chat method works"""
        self.factory.select_template(self.test_template_name)
        chat_log, gpt_chat  = self.factory.make_chat_log_and_gpt_chat()
        self.assertIsInstance(gpt_chat, cw.g.GPTChat)
        self.assertIsInstance(chat_log,cw.g.ch.ChatLog)
    def tearDown(self):
        del self.factory
        
if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
        
    
    

