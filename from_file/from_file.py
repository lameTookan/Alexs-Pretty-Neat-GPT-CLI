import os 

import os

class FromFile:
    """A class meant to interact with text files in a specific folder or return a default text file.
    If the specified file or folder does not exist, it gets created.
    """
    def __init__(self, file_folder="files", default="default.txt"):
        self.parent_dir = os.path.dirname(os.path.realpath(__file__))
        self.file_folder = file_folder
        self.default = default
        self.save_path = os.path.join(self.parent_dir, self.file_folder)
        self.default_path = os.path.join(self.parent_dir, self.default)
        self._set_up_files()

    def _set_up_files(self):
        """Sets up the necessary folders and files."""
        os.makedirs(self.save_path, exist_ok=True)
        if not os.path.exists(self.default_path):
            open(self.default_path, 'w').close()

    def get_default(self):
        """Returns the contents of the default file."""
        with open(self.default_path, "r") as f:
            return f.read()

    def get_file(self, filename):
        """Returns the contents of the file with the given name, if it exists."""
        filename = f"{filename}.txt" if not filename.endswith(".txt") else filename
        file_path = os.path.join(self.save_path, filename)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {filename} not found.")
        with open(file_path, "r") as f:
            return f.read()

    def _display_files(self):
        """Prints a list of the files in the save_path."""
        files = os.listdir(self.save_path)
        for i, file in enumerate(files, start=1):
            print(f"{i}: {file}")

    def menu(self):
        """Displays a menu to select a file from the save_path, returns the content of the selected file."""
        while True:
            print("Select a file to open by typing the number or the filename")
            print("Type 'q' to quit")
            self._display_files()
            ans = input(">>> ").strip()
            if ans.lower() in  ("q", "quit", "exit"):
                return None
            if ans.isdigit():
                try: 
                    ans = int(ans)
                    file = os.listdir(self.save_path)[ans-1]
                    return self.get_file(file)
                except IndexError:
                    print("Please enter a valid number")
            else:
                return self.get_file(ans)


file_selector = FromFile()
        
        

 
    