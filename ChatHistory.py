import tiktoken
from collections import namedtuple, UserString, UserList, UserDict, deque, namedtuple
import datetime
class BadMessageError(Exception):
    pass
EncodedMessage = namedtuple('EncodedMessage', ['message', 'token_count'])
class ChatHistory:
    
    allowed_roles = {'user', 'system', 'assistant'}
    default_sys_wildcards = {
        'date': {
            'description': 'The current date',
            'value': lambda: datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        } 
    }
    def __init__(self,model = 'gpt-4', max_model_tokens=8_000,  max_completion_tokens = 1_000, token_padding = 500, token_counter_function = None, message_styler = None, wildcards = None):
        self.token_counter = token_counter_function or self.default_token_counter
        self.model = model
        self.max_model_tokens = max_model_tokens
        self.max_completion_tokens = max_completion_tokens
        self.token_padding = token_padding
        self.wildcards = wildcards or self.default_sys_wildcards
        
        self.trimmed_chat_log = deque()
        self.full_chat_log = []
        self._system_prompt = None
        self.trimmed_chat_log_tokens = 0
        self.trimmed_messages = 0
        pass
    def default_token_counter(self, string, model = None):
        if model is None:
            model = self.model
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(string))
    def _format_message(self, content, role):
        return {
            'role': role,
            'content': content,
        }
    def _check_message_dict(self, message: dict):
        if not isinstance(message, dict):
            raise BadMessageError('message must be a dict')
        if set(message.keys()) != {'role', 'content'}:
            raise BadMessageError('message must have keys "role" and "content"')
        if message['role'] not in self.allowed_roles:
            raise BadMessageError(f'role must be one of {self.allowed_roles}')
        if not isinstance(message['content'], str):
            raise BadMessageError('content must be a string')
    
        
    def _encode_message(self, message: dict) -> EncodedMessage:
        """Counts tokens in message content, returns message as named tuple with message and token"""
        self._check_message_dict(message)
        return EncodedMessage(message, self.token_counter(message['content']))
    def _unencode_message(self, encoded_message: EncodedMessage):
        return encoded_message.message
    @property
    def system_prompt(self):
        wildcards = {k: v['value']() for k, v in self.wildcards.items()}
        return self._system_prompt.format(**wildcards)
    @system_prompt.setter
    def system_prompt(self, value):
        self._system_prompt = value
        self.work_out_tokens()

    def work_out_tokens(self):
        system_prompt_tokens = self.token_counter(self.system_prompt)
        self.max_chat_tokens = self.max_model_tokens - (system_prompt_tokens + self.token_padding + self.max_completion_tokens)
    def add_message(self, message_dict: dict = None, message= None, role=None):
        if message_dict is None and (role is None or message is None):
            raise ValueError('Either message_dict or both message and role must be provided')
        if message_dict is None:
            message_dict = self._format_message(message, role)
        else:
            self._check_message_dict(message_dict)
        encoded_message = self._encode_message(message_dict)
        self.trimmed_chat_log_tokens += encoded_message.token_count
        self.full_chat_log.append(encoded_message)
        self.trimmed_chat_log.append(encoded_message)
        self.trim()
    def trim(self):
        while self.trimmed_chat_log_tokens > self.max_chat_tokens:
            popped_message = self.trimmed_chat_log.popleft()
            self.trimmed_chat_log_tokens -= popped_message.token_count
            self.trimmed_messages += 1
    def get_chat_log(self, unencoded = False):
        if unencoded:
            return [self._unencode_message(message) for message in self.trimmed_chat_log]
        else:
            return list(self.trimmed_chat_log)
    def get_finished_chat_log(self):
        header = self._format_message(self.system_prompt, 'system')
        return [header] + self.get_chat_log(unencoded = True)
    
        
        
       
    
    
        