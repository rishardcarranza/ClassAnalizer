class Token:
    def __init__(self, line, type, value, position):
        self.line = line
        self.type = type
        self.value = value
        self.position = position
