class InvalidToken(Exception):
    def __init__(self, message="Most likely the token is invalid"):
        self.message = message
        super().__init__(self.message)

class InvalidGuild(Exception):
    def __init__(self, message="Most likely the guild is unavailable"):
        self.message = message
        super().__init__(self.message)

class InvalidChannel(Exception):
    def __init__(self, message="Most likely the channel is unavailable"):
        self.message = message
        super().__init__(self.message)

