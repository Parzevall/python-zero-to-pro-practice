from members import Member, PremiumMember, LimitReached

ana = Member("Ana")
bo = PremiumMember("Bo")
for member in (ana, bo):
    print(member, member.limit, member.loan_days)
ana.loans = {"111": None, "222": None}
try:
    ana.check()
except LimitReached as e:
    print("Blocked:", e)
