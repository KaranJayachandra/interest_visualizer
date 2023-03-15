from math import floor
from numpy import arange
import matplotlib.pyplot as plot

BAR_WIDTH = 0.3
EXCHANGE_RATE = 85
MAX_SAVINGS = 1800
interest_rate = 13.5
monthly_interest_rate = interest_rate / 12
init_balance = 2300089
init_balance = 2083190
emi_inr_min = 42780
emi_eur_min = round(emi_inr_min / EXCHANGE_RATE)
emi_eur = [emi_eur_min, 600, 800, 1000, 1200, 1400, 1600, 1800]

total_interest_paid  = []
total_savings_yearly = []


for emi_candidate in emi_eur:
    balance = [init_balance]
    interest = []
    current_balance = init_balance
    emi_inr = emi_candidate * EXCHANGE_RATE
    while current_balance > 0:
        current_interest = current_balance * monthly_interest_rate / 100
        interest.append(current_interest)
        current_balance = current_balance + current_interest
        current_balance = current_balance - emi_inr
        balance.append(current_balance)
    print(f"EMI Value: {round(emi_inr, 2)}")
    print(f"Payment Period: {floor(len(balance) / 12)} years, {len(balance) % 12} months")
    print(f"Total Interest Paid: {round(sum(interest), 2)}")
    total_interest_paid.append(round(sum(interest) / 1e5, 2))
    total_savings_yearly.append(((MAX_SAVINGS - emi_candidate) * 85 * 12) / 1e5)
print(emi_eur)
print(total_interest_paid)
print(total_savings_yearly)

br1 = arange(len(emi_eur))
br2 = [x + BAR_WIDTH for x in br1]
plot.bar(br1, total_interest_paid, width=BAR_WIDTH, label='Total Interest Paid')
plot.bar(br2, total_savings_yearly, width=BAR_WIDTH, label='Yearly Savings')
plot.xticks([r + BAR_WIDTH/2 for r in range(len(emi_eur))], emi_eur)
plot.xlabel('EMI (\u20AC)')
plot.ylabel('Lakhs (\u20B9)')
plot.legend()
plot.show()