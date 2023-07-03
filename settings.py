import os 
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL")
DEFAULT_TEMPLATE_NAME = os.getenv("DEFAULT_TEMPLATE_NAME")
bypass = os.getenv("BYPASS_MAIN_MENU")
if bypass == 1 or bypass == "1" or bypass == True or bypass == "True" or bypass == "true" or bypass == "TRUE":
    BYPASS_MAIN_MENU = True
else:
    BYPASS_MAIN_MENU = False

