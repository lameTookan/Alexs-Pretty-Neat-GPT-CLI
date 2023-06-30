# Day 1 of this project(June 25, 2023)

- I created a new project, I have made previous versions of this project but I wanted to start fresh, now that I have learned more about python and programming in general. In particular the collections module is a game changer.
- I created a new repository on github and I am using git to track my progress.
- Made the EncodeMessage class to handle turning a message into a namedtuple, containing the message and the token count.
- Made a robust test class to generate chat logs of a given size using some sample messages

---

# Day 2 Of this project(June 26, 2023)

- Made ChatLog class and Message class, and test cases for each
- Decided to abandon the EncodeMessage class in favor of the Message class, which is includes all direct functionality related to messages. A UserDict with .pretty() method and a token count attribute.
- Made a test class for the ChatLog class, and debugged the ChatLog class
- Started on GPTChat class, though ended up scrapping that version and starting over

---

# Day 3 of this project (June 27, 2023)

Made and debugged the following classes:

- GPTChat

  _A wrapper for the openai ChatCompletion end point, with setters and getters for each model parameter that includes validation_

  - Supports a return type attribute that can be set to string, dictionary, or Message object
  - Also relies on the BadModelParameterError exception class. This class also includes a dictionary of info for each parameter for reference. Same dictionary is included in the class, as well as a set of valid parameters.

- ChatWrapper
  _ A wrapper for the GPTChat class and the ChatLog class, to make interacting with the model seamless_ - Takes a GPTChat object and a ChatLog object as parameters during construction - Has setters and getters for user and assistant messages - One main method `chat_with_assistant` that takes a string user message as a parameter and returns a string assistant message, and updates the chat log accordingly
- ChatLog
  _debugged the save and loading features in this class and reorganized it, to group related methods together_
  - Expanded my test classes

---

# Day 4 of this project (June 28, 2023)

- Finished the ChatWrapper class, and debugged it
- Finished GPTChat class, and debugged it, still need to make more robust test cases for both of these classes
- Wrote docstrings for both classes
- Added saving and loading functionality to GPTChat and ChatWrapper classes
  - GPTChat only outputs a dictionary containing essential information, however the ChatWrapper class is more comprehensive and has a subclass for the saving system
    - Make and load save dictionaries
    - Verify that the save dictionary is valid
    - Save the dict as a json file to a save folder
    - Load a save file from the save folder
    - Add or remove the file path and file extension from the save file name
    - Output files as a list
    - Top level save and load methods
- Started on a template system for various common configs for the GPTChat class, and ChatLog as well as a factory class to make it easier to create these objects
  - Still need to work on this. Might separate finding templates and managing them into a separate class from the factory class
  - Also added some information about the template to the class objects directly, to allow for reloading from the template
- Started work on the menu system for the chatbot in chat_loop.py
- Added methods for retrieving GPTChat model params as a dictionary for use in the menu system(Allowing users to change model params on the fly)
  - Speaking of which also sketched out the outline for this system
  - Added datatype verification and conversion to the setters for the GPTClass
- Expanded the saving system for the ChatLog class to include metadata about the chatlog

  - version number (1.0.0)
  - date created
  - uuid for each instance of the chatlog
  - Did some more cleaning and organizing of the code, slimming down the docstring and moving it to a documentation file

- Wrote out this dev log and expanded it. Haven't been super great about that
- Overall a pretty productive day. I'm sure what I wrote though, it seems to work fine based on my basic tests, is super buggy. Will need to make test classes for everything.
  - Should probs do this before working anymore on the menu system,
  - Also need to make a test class for the factory class

## To do

- Test classes for GPT4Chat, ChatWrapper, Factory classes
- Test the save system for these classes more thoroughly
- Make documentation for GPTChat, ChatWrapper, and the Factory class
- Update documentation for ChatLog and Message
- Move wrapper to a separate file from GPTChat for simplicity
- Template manager, based on a json file
- Work on the menu system
- Think about extending functionality for WorkingCopy

---

# Day 5 of this project (June 29, 2023)

_As a brief note, this was edited by GPT-4, so my voice has changed a touch. The words themselves were mine, just rephrased a bit more professional sounding than I'd normally write, It would probably look better not to include this note, however, I think its best to be open with AI involvement_

**Question Asked to GPT-4(via ChatGPT)** : _"Can you please describe your involvement in the editing process?"_

> "As an AI developed by OpenAI, my role in the editing process involved taking the original text and improving its clarity, coherence, and readability. The input was provided by the user and I did not add any new information or ideas. My goal was to respect the user's voice while ensuring that the message is clearly conveyed. I also helped to format the text in a Markdown format suitable for a development log. I strive to maintain a neutral, professional tone in my edits, but always within the parameters set by the user's original input."

## Progress Today:

- Enhanced the **template system** for better robustness and encapsulation. Integrated it with other classes, enabling the saving of templates within the classes themselves and methods for reloading the classes from the template in case of any unwanted issues.
- Separated the **template selection and verification system** from the object factory class. This ensures avoidance of circular imports, since the template selector and system does not need to directly use any of the classes, thus eliminating the chance of circular imports when importing it into various classes.
- Undertook a comprehensive **debugging** process across the entire system.

  - Created **test classes** for:
    - Object factory
    - Template selector
    - GPTChat
  - Also updated the test class for ChatLog to test the new template reloading system.

- Accomplished an extensive debugging exercise along with **light refactoring**. This included adding more doc strings and reorganizing classes so that related methods are next to each other for simplicity.

## To Do:

- Expand the test classes for the chat wrapper. This is to include testing of the new save and load feature which utilizes the 'save to dict' system from GPTchat and the SaveToDict subclass. This is separate from the SaveToFile subclass that is responsible for saving to the file path.

## Dev Notes:

Today, I had a feeling that I wasn't accomplishing much, but I did a lot of work on debugging, testing, documenting, and reworking a few aspects. This is equally crucial as adding new features, even if it doesn't feel as productive. It's all part of the learning process, the primary purpose of this project. I'm nearing the end. Once I make sure all my code is bug-free (with a few things in ChatWrapper being all that's left), I should be ready to finish work on the main CLI menu interface. After 4 days, I'm excited to be able to actually use the systems I made beyond some light testing. Creating menus and interfaces is somewhat enjoyable, even if it's command-line based.
