class Keys():
    def __init__(self, file_path='./data/keys'):
        self.file_path = file_path
        self.client_id = None
        self.client_secret = None

    def load(self):
        with open(self.file_path) as keys_file:
            lines = keys_file.readlines()
            self.client_id = lines[0].strip()
            self.client_secret = lines[1].strip()
