class Tokens():
    def __init__(self, file_path='./data/tokens'):
        self.file_path = file_path
        self.access_token = None
        self.refresh_token = None

    def load(self):
        with open(self.file_path) as tokens_file:
            lines = tokens_file.readlines()
            self.access_token = lines[0].strip()
            self.refresh_token = lines[1].strip()

    def update(self, access_token, refresh_token=None):
        if self.refresh_token is None:
            refresh_token = self.refresh_token
        with open(self.file_path, 'w') as tokens_file:
            tokens_file.write('{}\n{}'.format(access_token, refresh_token))

        self.access_token = access_token
        self.refresh_token = refresh_token
