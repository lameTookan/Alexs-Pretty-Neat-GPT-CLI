import pyfiglet as pf

import chat_loop as cl

result = pf.figlet_format("Alex's P.N.G.CLI Chatbot")
print("\u001b[35m" + result + "\u001b[0m")
divider = "_-_" * 20
print(divider)
msg = pf.figlet_format("Alex's Pretty Neat GPT CLI Chatbot", font="digital")
print("\u001b[33m" + msg + "\u001b[0m")
# print("Alex's")
# print("Pretty Neat ")
# print("GPT CLI Chatbot")
print("Version 1.0.0")
print("Ensure that you have completed the setup process before using this program.")
print(divider)
print()
print()

cl.main_menu.main_menu()
