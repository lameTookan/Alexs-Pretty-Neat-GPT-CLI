import tiktoken
import unittest 
import time 
import json
from contextlib import contextmanager
from EncodeMessage import EncodeMessage, EncodedMessage, BadMessageError
class TestMessageEncoder(unittest.TestCase):
    def setUp(self) -> None:
        self.encoder = EncodeMessage(model = 'gpt-4')
    def count_tokens(self, string):
        encoding = tiktoken.encoding_for_model('gpt-4')
        return len(encoding.encode(string))
    def encode_message_dict(self, message: dict):
        token_count = self.count_tokens(message['content'])
        return EncodedMessage(message, token_count)
    def test_encode_message_dict(self):
        message = {'role': 'user', 'content': 'Hello, how are you?'}
        token_count = self.count_tokens(message['content'])
        encoded_message = EncodedMessage(message, token_count)
        

        self.assertEqual(self.encoder.encode_message_dict(message), encoded_message)
    def test_encode_message_string(self):
        message = 'Hello, how are you?'
        role = 'user'
        token_count = self.count_tokens(message)
        encoded_message = EncodedMessage({'role': role, 'content': message}, token_count)
        self.assertEqual(self.encoder.encode_message_string(message, role), encoded_message)
    def test_encode_message_list(self):
        message_list = [
            {'role': 'user', 'content': 'Hello, how are you?'},
            {'role': 'assistant', 'content': 'I am well, how are you?'},
        ]
        encoded_message_list = [
            EncodedMessage(message_list[0], self.count_tokens(message_list[0]['content'])),
            EncodedMessage(message_list[1], self.count_tokens(message_list[1]['content'])),
        ]
        self.assertEqual(self.encoder.encode_message_list(message_list), encoded_message_list)
    def test_decode_message_dict(self):
        message = {'role': 'user', 'content': 'Hello, how are you?'}
        encoded_message = self.encode_message_dict(message)
        self.assertEqual(self.encoder.decode_message_dict(encoded_message), message)
    def test_decode_message_list(self):
        message_list = [
            {'role': 'user', 'content': 'Hello, how are you?'},
            {'role': 'assistant', 'content': 'I am well, how are you?'},
        ]
        encoded_message_list = self.encoder.encode_message_list(message_list)
        self.assertEqual(self.encoder.decode_message_list(encoded_message_list), message_list)
    def test_count_tokens_message_list(self):
        
        message = {'role': 'user', 'content': 'Hello, how are you?'}
        chat_log = [self.encode_message_dict(message) for _ in range(10)]
        self.assertEqual(self.encoder.count_tokens_message_list(chat_log), self.count_tokens(message['content']) * 10)
        
        


    def test_check_message_dict(self):
        self.assertRaises(BadMessageError, self.encoder._check_message_dict, 'Hello, how are you?')
        self.assertRaises(BadMessageError, self.encoder._check_message_dict, {'role': 'user', 'user': 'Hello, how are you?', 'extra': 'extra'})
    def test_custom_token_counter(self):
        self.assertRaises(ValueError, EncodeMessage, model = 'gpt-4', token_counter_func = 'Hello, how are you?')
        bad_token_counter = lambda x: 'Hello, how are you?'
        self.assertRaises(ValueError, EncodeMessage, model = 'gpt-4', token_counter_func = bad_token_counter)

    def tearDown(self) -> None:

        del self.encoder
    

if __name__ == '__main__':

    unittest.main(argv=[''], verbosity=2, exit=False)

@contextmanager
def timer():
    import time
from contextlib import contextmanager

@contextmanager
def timer():
    start = time.perf_counter()
    try:
        yield
    finally:
        end = time.perf_counter()
        print(f'Time elapsed: {end - start} seconds')

#worst case scenario, we have to encode 1400 short messages

with open('test_chat_logs/short_7000.json', "r") as f:
    worst_case = json.load(f)
encoder = EncodeMessage(model = 'gpt-4')
with timer():
    encoded_messages = encoder.encode_message_list(worst_case)


def time_decoding(encoded_messages):
    
    start = time.time()
    encoder.decode_message_list(encoded_messages)
    end = time.time()
    return end - start
results = []
for i in range(5):
    n = (time_decoding(encoded_messages))
    print("Test", str(i), ": ",  str(n))
    results.append(n)

def simple_average(lst):
    return sum(lst) / len(lst)
print(str(simple_average(results)))



with timer():
    encoder.count_tokens_message_list(encoded_messages)




    

with timer():
    time.sleep(3)