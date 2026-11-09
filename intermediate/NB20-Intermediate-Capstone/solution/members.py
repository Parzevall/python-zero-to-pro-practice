from catalog import LibraryError


class LimitReached(LibraryError):
    pass


class FineOwed(LibraryError):
    pass


class Member:
    limit = 2
    loan_days = 14

    def __init__(self, name):
        self.name = name
        self.loans = {}      # isbn -> due date
        self.fines = 0       # in cents

    def kind(self):
        return "standard"

    def check(self):
        if self.fines > 0:
            raise FineOwed(f"{self.name} owes {self.fines} cents")
        if len(self.loans) >= self.limit:
            raise LimitReached(f"{self.name} already has {self.limit} books")

    def __str__(self):
        return f"{self.name} ({self.kind()})"


class PremiumMember(Member):
    limit = 4
    loan_days = 21

    def kind(self):
        return "premium"
