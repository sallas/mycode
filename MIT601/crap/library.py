class Library:
    dailyFine = 0.25
    def __init__(self, books ):
        self.shelf = {}
        for book in books:
            self.shelf[book] = (None, None)
    def checkOut(self, book, patron, date):
        self.shelf[book] = (patron, date+7)
    def checkIn(self, book, date):
        patron, dueDate = self.shelf[book]
        self.shelf[book] = (None,None)
        if date > dueDate:
            return (date - dueDate) * Library.dailyFine
        else:
            return 0.0
    def overdueBooks(self, patron, date):
        [ book for book in self.shelf if self.shelf[book][0] == patron \
          and self.shelf[book][1] < date  ]
        for book in self.shelf:
            shelfPatron , due = self.shelf[book]
            if shelfPatron == patron and due < date:
                list.append(book)
class LibraryGrace(Library):
    def __init__(self, graceDays, books):
        Library.__init__(self, books)
        self.graceperiod = graceDays
    def checkIn(self, book, date):
        return Library.checkIn(self, book, date - self.graceperiod)
