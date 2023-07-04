# Dev Log for Intermediate ChatBot

## Day 1 of this project(June 25, 2023)

- I created a new project, I have made previous versions of this project but I wanted to start fresh, now that I have learned more about python and programming in general. In particular the collections module is a game changer.
- I created a new repository on github and I am using git to track my progress.
- Made the EncodeMessage class to handle turning a message into a named tuple, containing the message and the token count.
- Made a robust test class to generate chat logs of a given size using some sample messages

---

## Day 2 Of this project(June 26, 2023)

- Made ChatLog class and Message class, and test cases for each
- Decided to abandon the EncodeMessage class in favor of the Message class, which is includes all direct functionality related to messages. A UserDict with .pretty() method and a token count attribute.
- Made a test class for the ChatLog class, and debugged the ChatLog class
- Started on GPTChat class, though ended up scrapping that version and starting over

---

## Day 3 of this project (June 27, 2023)

Made and debugged the following classes:

- GPTChat

  _A wrapper for the openai ChatCompletion end point, with setters and getters for each model parameter that includes validation_

  - Supports a return type attribute that can be set to string, dictionary, or Message object
  - Also relies on the BadModelParameterError exception class. This class also includes a dictionary of info for each parameter for reference. Same dictionary is included in the class, as well as a set of valid parameters.

- ChatWrapper
  _A wrapper for the GPTChat class and the ChatLog class, to make interacting with the model seamless_ - Takes a GPTChat object and a ChatLog object as parameters during construction - Has setters and getters for user and assistant messages - One main method `chat_with_assistant` that takes a string user message as a parameter and returns a string assistant message, and updates the chat log accordingly
- ChatLog
  _debugged the save and loading features in this class and reorganized it, to group related methods together_
  - Expanded my test classes

---

## Day 4 of this project (June 28, 2023)

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
  - Should probably  do this before working anymore on the menu system,
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

## Day 5 of this project (June 29, 2023)

As a brief note, _this was edited by GPT-4_, so my voice has changed a touch. The words themselves were mine, just rephrased a bit more professional sounding than I'd normally write, It would probably look better not to include this note, however, I think its best to be open with AI involvement

**Question Asked to GPT-4(via ChatGPT)** : _"Can you please describe your involvement in the editing process?"_

> "As an AI developed by OpenAI, my role in the editing process involved taking the original text and improving its clarity, coherence, and readability. The input was provided by the user and I did not add any new information or ideas. My goal was to respect the user's voice while ensuring that the message is clearly conveyed. I also helped to format the text in a Markdown format suitable for a development log. I strive to maintain a neutral, professional tone in my edits, but always within the parameters set by the user's original input."

### Progress Today

- Enhanced the **template system** for better robustness and encapsulation. Integrated it with other classes, enabling the saving of templates within the classes themselves and methods for reloading the classes from the template in case of any unwanted issues.
- Separated the **template selection and verification system** from the object factory class. This ensures avoidance of circular imports, since the template selector and system does not need to directly use any of the classes, thus eliminating the chance of circular imports when importing it into various classes.
- Undertook a comprehensive **debugging** process across the entire system.

  - Created **test classes** for:
    - Object factory
    - Template selector
    - GPTChat
  - Also updated the test class for ChatLog to test the new template reloading system.

- Accomplished an extensive debugging exercise along with **light refactoring**. This included adding more doc strings and reorganizing classes so that related methods are next to each other for simplicity.

### To Do

- Expand the test classes for the chat wrapper. This is to include testing of the new save and load feature which utilizes the 'save to dict' system from GPTchat and the SaveToDict subclass. This is separate from the SaveToFile subclass that is responsible for saving to the file path.

### Dev Notes

Today, I had a feeling that I wasn't accomplishing much, but I did a lot of work on debugging, testing, documenting, and reworking a few aspects. This is equally crucial as adding new features, even if it doesn't feel as productive. It's all part of the learning process, the primary purpose of this project. I'm nearing the end. Once I make sure all my code is bug-free (with a few things in ChatWrapper being all that's left), I should be ready to finish work on the main CLI menu interface. After 4 days, I'm excited to be able to actually use the systems I made beyond some light testing. Creating menus and interfaces is somewhat enjoyable, even if it's command-line based.

## Day 6 of this project (June 30, 2023)

### Progress Today

- Made test class for  and debugged `ChatWrapper`,
- Bunch of cleaning up
  - Better docstrings
  - Better comments
  - More consistent naming
  - Convince Methods for ChatWrapper
  
- Added some more documentation, for `ChatWrapper`
- Expanded tests for `ChatLog` and `Message`, more debugging
- Added an option for no max_messages in `ChatLog`(_None means no limit_)
- Improved `__repr__` for everything
- Added setters and getters for token info attributes in `ChatLog`
- Improved saving and loading for `ChatWrapper`
- Made test class for `GPTChat` using mocking, with the help of GPT-4
- Made an object factory for `ChatWrapper` allowing to make the entire thing from a template
- Added a few methods to `TemplateSelector` to output a list of names, and template info(name, description, and tags)
- Did some work on the menu system, but its still not done.
- Basically, everything aside from the menu system is done.
- Finally added the .env loader system and made .env.example
  - Includes API KEY, default model, and default template name
- Added return type option for `ChatWrapper`

### Things I have learned

- Think about circular imports from the beginning, and try to avoid them. Right now there are too many weird paths to objects buried in imports. Right now it would just be a pain to fix, but I'll keep it in mind for the future.

- Unittest mocking is a honking great idea! We should do more of that
- OOP is a lot of work but it also means I'll be able to reuse much of this and adding new features is fairly easy

### To Do

- README
- The menu system
  - Options to save and load system prompts
  - Options to modify model, choose new template, etc on the fly
  - Changing model parameters on the fly
  - Help menu
  - Maybe a few easter eggs and fun things like color and ascii art

- Improve and expand documentation
- Final testing and debugging, once the menu system is done
- Final checks and clean up before making the repo public

### Dev Notes

I am so close to being done I can feel it. Ready to be done with this thing. Today was another clean up and tweaking day, but again those are just as important as adding new features.

### An aside on last night's commit

So, I couldn't sleep last night ended up writing 500 lines of code and I can finally talk to my chatbot! Everything seems to be working well, did a little debugging (the wrapper return type system wasn't great, had to debug that and update my tests. But it works great!). Project is almost done!

---

## Dev Log Day 7 (July 1, 2023)

--

Today was a long day, for sure. It took forever, but things are finally coming together.

### What I did today

- Menu for the chat loop:

  - Save `ChatWrapper` class to a file with a menu
  - Modify model parameters on the fly
  - Load from a previous save
  - Change system prompts on the fly (with the `System Prompt Manager` class)
  - Reset chat

- System prompt manager menu:

  - One class is for the actual functionality of saving and reading files

  - The other is a wrapper with the menus

  - Supports loading a file (if accessed from the chat loop)

  - Writing a new one with info on the wild cards displayed

  - Quickly setting a new one, saving it, and returning it

  - Deleting saves

  - Viewing system prompts

  - Secret debug command that prints out the detailed  `__repr__` I made for the  `ChatWrapper` class
    - Includes the other detailed `__repr__` from `ChatLog` and `GPTChat`
    - Of course, any API keys are omitted, it just shows if one is present or not

- Main menu class:

  - Choose from templates

  - Set a system prompt, or manage system prompt saves/create new ones

  - Create the `ChatWrapper` object using the factory system

  - Load from a save for the `ChatWrapper` object

    - This is unfortunately mostly copied and pasted from the method `ChatLoop`. I can't really access it before making the chat loop object, and that requires a `ChatWrapper`
    - Wanted to give users the option to load a different save in both menus

### Dev Notes

- Tested it a lot, but still need to thoroughly use everything there.
- This is kind of a monster of a file, and certainly not my best work. If I ever make a CLI again, I will use specialized libraries.
- There's nothing super wrong with it; it's well structured and documented with type hints and docstrings. However, there is a lot of repetition and it's all nested conditional logic.
- The file itself is **huge** — over 1K lines.
- In my previous dev log, I was excited to make this, but gee whiz, this is taking a lot of effort.
- Almost done though! On track to finish by July 3.
- I seriously can't wait to be done.

### To Do

- Debug and test the menus.
- Make README.md.
- Add a GPT-generated guide on installing for complete beginners in the docs folder called `HELP_ME.md`.
- Reset chat log before returning to the menu after quitting the chat loop. **(REMEMBER, ALEX! THIS COULD CONFUSE USERS)**
- Add two features if I have time:
  - Outputting chat log as a text file.
  - Get messages from a text file, for copying in large messages.
    - Maybe add multiple files and a nice menu, otherwise just get them from a text file.
- Add more documentation if I have time.
- Fix up the `__repr__` to improve formatting a bit.
- Fix up the error messages for the input validation. It's currently saying "Can't be type False" due to the way I implemented it. I should save type first for the error message in my `BadModelParamError` exception.

### What I Learned Today

- Never make a CLI interface without using a library and studying various methods.
- Eye drops, and breaks are a honking good idea! Let's have more of those.
- I mean, overall lots more. But I am planning to add a retrospective what I learned section to the end of the dev log once I am done.

---

## Day 8 (July 2, 2023)

---

### What I did today

- Debugged and touched up my menu system.
- Fixed the little bugs I mentioned earlier
- Completed the from file feature
- Completed the export system, have not integrated it into the menu system
- Tested everything in the menu system
- Added a few more templates for the system
- Added a bypass menu env variable to bypass the main menu and go straight into the main chat loop
- Worked out a bug with the wildcard system preventing the ability for users to use curly braces in system prompts

### Dev Notes

- I honestly kinda hate the menu system, I have been doing a lot of research on command patterns and I wish I did it first
  - While I am tempted to give myself another day to work on it, I still think it would be better to release it as is, and work on refactoring once I have a little bit of time
- I really love my underlying codebase however, the menu system just needs a lot of reworking
- I am ready to be done with this project however, at least for now.
- I'll likely refactor the entire menu system later, as a side project, once I've sort of defragged my brain from this project
- The menu system does work really well, and I learned a lot from making it.

### What I learned today

- There are much better ways to make a command line interface like this, and I should use them
- A lot more on this will be included in my final retrospective

### To do(before release)

- Integrate the export chat feature into the menu system(if I have time)
- Do a final check through of my code base, make sure everything that should be removed is gone
- Make README
- Ask GPT to generate a more comprehensive HELP_ME.md file for folks that have never installed a python project before, as I have been there
- Update documentation

#### Longer term to do

This is stuff I can do when I pick up this project again to improve it

- Scrap the entire menu system and rework it using command pattern and specialized libraries for this kinda thing
- Reorganize code base to avoid circular imports
- Refactor chatlog.
  - UserList for the main chat log(what I call full_chat_log)
  - Take a hard line stance on the Messages. It should only work with Message objects, not strings. There are too many convince methods meant to allow for inputting of strings, dicts etc
  - To this end, use the message factory callable I have to generate a function to properly encode Messages with the model name,
  - Overall this is a pretty small thing though, it does work with Messages for the most part, I just have wrapper methods for the main ones that deal with Message objects to allow for inputting stuff as a string and role, and exporting as strings.
    - Maybe 4 of such methods

---

## Dev Log FInal Day (July 3, 2023)

### What I did today

- Made the parameter menu a little more user friendly
  - Typing the word `zero` will now set the param to zero
  - Typing the word `none` will now remove the parameter entirely
  - Directions that when setting a parameter to something between -1 and 1 (ie 0. something ) you must use a trailing zero
- Improved documentation for the template system
  - the template documentation now includes more information on what the chat log parameters do
  - Added a template directory that briefly describes each template built in
- Added documentation for `GPTChat`
- Improved the `from_file` system to be a little more user friendly
  - It will now tell users if there message is too long to be added to the chat log, with helpful information on what a token is
  - The message itself will be printed to the console so users can see what they added
- Made it so the default instructions in the chat loop are more concise, with help bringing up all the command info
- Cleaned up the code, removed any old commented out stuff, ran my unittests one more time to ensure nothing was broken while I was fixing stuff when debugging the menu system
- Integrated the chat export menu into the menu system
  - This is still kinda rough, probably should have added one command to accomplish this task rather than a menu
  - Also should have probably included a system to export only the most recent assistant message
- Made the `main.py` added a few cute formatting stuff  using pyfig
- Changed the overall name of this project from "Intermediete Chatbot" to "Alex's Pretty Neat GPT CLI Chatbot" or " A.P.N.G.CLI" for short
- Made the README file
- Made the HELP_ME file

### Things I can do if I ever decide to pick up this project again

- Completely refactor the menu system
- Remake the ChatLog class to be better encapsulated and remove all the convenience methods included
- Perhaps add a few fun features, like a simple agent system

---

## Final Retrospective

Overall, I am honestly pretty pleased with how this turned out. The menus aren't quite as bad as I was thinking yesterday, I really like the from_file system. And the underlying codebase works extremely well, is well documented, clean, and tested. I also learned a lot in this process on how to make a larger project like this

### Things I learned

- Command patterns for CLI interfaces, no weird and complex nested menus

- Circular imports and code organization are something I need to think about and plan for from day one

  - No importing things as shortned version (like `g` for `GPTChat` , `cw` for `ChatWrapper` etc.)

- Unittests are great, but I should have put them all in a dedicated folder to not clog up my code base and file system

- Speaking of file systems, I should have organized everything into folders better

- Better adherence to OOP principals -- Its not that big of a deal to need to use objects when interacting with my classes, especially if I include factories

  - Doing stuff, like instead of accepting message dictionaries, roles and content as params, and Message objects in ChatLog just produce a dedicated callable factory object to make messages
    - I did this because, in order to count the tokens, Message needs the model name, and since that might change I didn't want to need to plan around that.
    - But using a class with a `__call__` method, I could have made a dedicated function and used that for creating message objects

- No returning None or False as a fail state anywhere

  - I did this because for scenarios like the following
    - User wants to save a file. The method that handles this has a `overwrite` argument that is set to `False` by default
    - Try writing the file using the method in an if statement, if the file is found it will output `False` , then I could ask the user if they would like to overwrite the given file and call it again with overwrite set to `True`
  - However, this design pattern, makes finding bugs extremely difficult, especially when they are multiple objects and methods chained together, in scenarios when something is `False` or `None` when it shouldn't have been tracking down where that occurred was kinda a pain
  - What I should have done was simply raise a FileNotFoundError in such a scenario, and catch it if I want to check, or use a dedicated method t check if a file exists

- No long classes, each class should only have a few methods and attributes for better readability and maintainability, with additional functionality being added using wrappers or child classes

  - Instead of my ChatLog class handling managing both the full chat log and the trimming process, I should have made `full_chat_log` a separate `UserList` with the trimming process being done by a wrapper

### Things I did well

- Custom exceptions and proactive defensive programming
  - Someone using my classes will never see any normal python errors, unless there is a programming error within my class.
  - The only exceptions they will see are a result of them using the classes incorrectly, with informative error information explaining exactly what the problem is and how to avoid it
  - Type checking when setting params to avoid it causing errors down the line
- I really like the GPTChat wrapper and all its verification and informative help information being displayed with incorrect variables

- The use of deques in the ChatLog class and the trimming process
  - This works super well and speedy as heck
  - In a previous version of this project, I used normal lists and `.pop(0)` for this functionality, this was extremely slow
    - I'd also recount the entire chat log's token count before and after removal of a message instead of just counting them once on creation and adding or subtracting the message's token count
    - Ive done a little stress testing, with massive files of 100,000 short messages and it takes only a few seconds to go through the entire thing, vs in my previous versions that took around 10-15 seconds

- My favorite overall is the template system. It really simplifies creating ChatLog, GPTChat, and ChatWrapper objects with common configs
- The chat wrapper class is also really solid and easy to use. Aside from saving and loading there is a single method you need to use to input a user message and generating a response
  - API calls, and adding the message to chat log, and retrieving the assistant message is all handled automatically

### Final Thoughts

I am pretty pleased with this project overall. I actually really dig the functionality here. In particular being able to easily change model params and system messages during a chat is super useful for testing out various configurations. I also really like the `from_file` and  exporting system for inputting longer messages.

Of course, its by no means perfect. The menu system is probably the worst out of everything, but everything works well. This project would have been sort of pointless if I didn't learn anything and did everything well.

Until next time,

Fin.

Made by Alex.
