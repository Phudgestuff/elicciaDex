import json

class Fetch:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_info(self):
        """
        Reads the user information from the JSON file and returns it as a dictionary.
        """
        try:
            with open(self.file_path, 'r') as file:
                info = json.load(file)
            return info
        except FileNotFoundError:
            print(f"File not found: {self.file_path}")
            return {}

    def update_info(self, new_info):
        """
        Updates the user information in the JSON file with the provided dictionary.
        """
        try:
            with open(self.file_path, 'w') as file:
                json.dump(new_info, file, indent=4)
            #print(f"User information updated successfully in {self.file_path}")
        except Exception as e:
            print(f"Error updating JSON information: {e}")

inventory = Fetch('./data/inventory.json')
pokemon = Fetch('./data/pokemon.json')

