class Hammock:
    def __init__(self):
        self.people = 0
        self.previous = ''
    def sitDown(self, name):
        if self.people and not name == self.previous:
            self.previous = name
            return 'sorry, no room'
        self.people += 1
        return 'welcome'
    def leave(self):
        if self.people:
            self.people -= 1
        return self.people
