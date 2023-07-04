import unittest
import os
import json
from ExportChatLogs import ChatLogExporter, NoFolderError

testchat = {
    "meta_data": {
        "chat_wrapper_version": "0.1.0",
        "chat_wrapper_uuid": "f2c6f7f1-183d-4a24-b5b7-b5aa36c3f194",
        "timestamp": "2023-07-01T05-00-03.141480"
    },
    "chat_log": {
        "metadata": {
            "date": "2023-07-01 05:00:03",
            "length": 6,
            "uuid": "9b65dcb7-80ba-4053-b9ad-595334eed758",
            "ChatLog version": "1.0.1",
            "SaveToDict version": "1.0.0",
            "size": 3744
        },
        "max_chat_tokens": 6456,
        "max_chat_messages": 1000,
        "max_model_tokens": 8000,
        "token_padding": 500,
        "max_completion_tokens": 1000,
        "full_chat_log": [
            {
                "role": "user",
                "content": "hdeqsxa "
            },
            {
                "role": "assistant",
                "content": "I'm sorry, but I don't recognize \"hdeqsxa\" as a word or command. Could you please provide more information or rephrase your request?"
            },
            {
                "role": "user",
                "content": "param"
            },
            {
                "role": "assistant",
                "content": "I noticed you've mentioned a term \"param\", which is often short for \"parameter\". In various programming, scientific, or mathematical contexts it could refer to a variable or detail of certain operations. However, without more context, it's hard for me to provide specific information that could be helpful to you.\n\nIf you provide additional details about what particular usage of \"param\" you're interested in (like C++ programming, statistical analysis, etc.), I could certainly give you a more accurate and tailored response."
            },
            {
                "role": "user",
                "content": "I am so sorry for confusing you. I think i just need to knock out. I could have sworn I finished adding the param menu feature to the main chat loop. Save cheese though, I am saving this chat as debug!"
            },
            {
                "role": "assistant",
                "content": "No problem at all, it sounds like you've been working pretty hard! It's perfectly okay to take a rest. And don't worry, I'm here whenever you need assistance.\n\nJust a note- save \"cheese\", or logging and debugging processes are widely used in development to track actions and identify issues. Remember, it's always important to take breaks in order to stay motivated and produce better results. Rest well!\n"
            }
        ],
        "trimmed_chat_log": [
            {
                "role": "user",
                "content": "hdeqsxa "
            },
            {
                "role": "assistant",
                "content": "I'm sorry, but I don't recognize \"hdeqsxa\" as a word or command. Could you please provide more information or rephrase your request?"
            },
            {
                "role": "user",
                "content": "param"
            },
            {
                "role": "assistant",
                "content": "I noticed you've mentioned a term \"param\", which is often short for \"parameter\". In various programming, scientific, or mathematical contexts it could refer to a variable or detail of certain operations. However, without more context, it's hard for me to provide specific information that could be helpful to you.\n\nIf you provide additional details about what particular usage of \"param\" you're interested in (like C++ programming, statistical analysis, etc.), I could certainly give you a more accurate and tailored response."
            },
            {
                "role": "user",
                "content": "I am so sorry for confusing you. I think i just need to knock out. I could have sworn I finished adding the param menu feature to the main chat loop. Save cheese though, I am saving this chat as debug!"
            },
            {
                "role": "assistant",
                "content": "No problem at all, it sounds like you've been working pretty hard! It's perfectly okay to take a rest. And don't worry, I'm here whenever you need assistance.\n\nJust a note- save \"cheese\", or logging and debugging processes are widely used in development to track actions and identify issues. Remember, it's always important to take breaks in order to stay motivated and produce better results. Rest well!\n"
            }
        ],
        "trimmed_chat_log_tokens": 271,
        "trimmed_messages": 0,
        "sys_prompt": "You are a helpful AI assistant. Your model is {model} Today's date is {date}, and your training data cuts off in September 2021 ",
        "model": "gpt-4",
        "wildcards": {
            "date": {
                "value": "__DATE__",
                "description": "The current date and time"
            },
            "model": {
                "value": "__MODEL__",
                "description": "The model used to encode the message"
            }
        }
    },
    "gpt_chat": {
        "temperature": 1.1,
        "model_name": "gpt-4",
        "max_tokens": 1000,
        "top_p": 1.0,
        "frequency_penalty": 0.5,
        "presence_penalty": None,
        "return_type": "string"
    }
}
class TestChatLogExporter(unittest.TestCase):
    def setUp(self):
        self.chatlog_folder = 'chatbot_saves/'
        self.save_folder = 'text_exports/'
        self.file_name = 'chatlog1'
        self.file_path = self.chatlog_folder + self.file_name + '.json'
        self.export_path = self.save_folder + self.file_name + '.txt'
        self.exporter = ChatLogExporter(self.chatlog_folder, self.save_folder)
        self.chat_data = testchat
        with open(self.file_path, 'w') as f:
            json.dump(self.chat_data, f)

    def tearDown(self):
        os.remove(self.file_path)
        if os.path.exists(self.export_path):
            os.remove(self.export_path)

    def test_export(self):
        self.exporter.export(self.file_name)
        self.assertTrue(os.path.exists(self.export_path))

    def test_check_if_chatlog_exists(self):
        self.assertTrue(self.exporter.check_if_chatlog_exists(self.file_name))

    def test_check_if_chatlog_does_not_exist(self):
        self.assertFalse(self.exporter.check_if_chatlog_exists('non_existing_file'))

    def test_export_all(self):
        self.exporter.export_all()
        self.assertTrue(os.path.exists(self.export_path))

    def test_list_chatlog_files(self):
        files = self.exporter.list_chatlog_files()
        self.assertIn(self.file_name, files)

    def test_list_save_files(self):
        self.exporter.export(self.file_name)
        files = self.exporter.list_save_files()
        self.assertIn(self.file_name, files)

    def test_check_if_save_file_exists(self):
        self.exporter.export(self.file_name)
        self.assertTrue(self.exporter.check_if_save_file_exists(self.file_name))

    def test_check_if_save_file_does_not_exist(self):
        self.assertFalse(self.exporter.check_if_save_file_exists('non_existing_file'))

if __name__ == '__main__':
    unittest.main()
