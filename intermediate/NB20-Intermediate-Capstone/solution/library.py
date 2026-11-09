from datetime import date, timedelta
from catalog import LibraryError
from members import Member, PremiumMember

FINE_PER_DAY = 25  # cents


class UnknownMember(LibraryError):
    pass


class NoCopiesLeft(LibraryError):
    pass


class NotBorrowed(LibraryError):
    pass


class Library:
    def __init__(self, catalog):
        self.catalog = catalog
        self.members = {}
        self.history = []    # (date text, "out" or "back", member, isbn)

    def join(self, name, premium=False):
        member = PremiumMember(name) if premium else Member(name)
        self.members[name] = member
        return member

    def member(self, name):
        if name not in self.members:
            raise UnknownMember(f"{name} is not a member")
        return self.members[name]

    def checkout(self, name, isbn, today):
        member = self.member(name)
        book = self.catalog.get(isbn)
        member.check()
        if book.available() <= 0:
            raise NoCopiesLeft(f"{book.title} has no copies left")
        book.on_loan += 1
        due = today + timedelta(days=member.loan_days)
        member.loans[isbn] = due
        self.history.append((today.isoformat(), "out", name, isbn))
        return due

    def give_back(self, name, isbn, today):
        member = self.member(name)
        if isbn not in member.loans:
            raise NotBorrowed(f"{name} has not borrowed {isbn}")
        due = member.loans.pop(isbn)
        self.catalog.get(isbn).on_loan -= 1
        fine = max(0, (today - due).days) * FINE_PER_DAY
        member.fines += fine
        self.history.append((today.isoformat(), "back", name, isbn))
        return fine

    def pay(self, name):
        member = self.member(name)
        paid = member.fines
        member.fines = 0
        return paid

    def overdue(self, today):
        late = []
        for name in sorted(self.members):
            for isbn, due in sorted(self.members[name].loans.items()):
                if due < today:
                    late.append((name, isbn, (today - due).days))
        return late

def run_events(library, events):
    outcomes = []
    for when, *rest in events:
        today = date.fromisoformat(when)
        try:
            match rest:
                case ["join", name]:
                    library.join(name)
                    message = f"{name} joined"
                case ["join", name, "premium"]:
                    library.join(name, premium=True)
                    message = f"{name} joined as premium"
                case ["out", name, isbn]:
                    due = library.checkout(name, isbn, today)
                    message = f"{name} took {isbn}, due {due}"
                case ["back", name, isbn]:
                    fine = library.give_back(name, isbn, today)
                    message = f"{name} returned {isbn}, fine {fine}"
                case ["pay", name]:
                    message = f"{name} paid {library.pay(name)}"
                case _:
                    raise LibraryError(f"unknown action {rest[0]}")
            outcomes.append((when, True, message))
        except LibraryError as e:
            outcomes.append((when, False, f"{type(e).__name__}: {e}"))
    return outcomes
