import os 
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL")
DEFAULT_TEMPLATE_NAME = os.getenv("DEFAULT_TEMPLATE_NAME")

