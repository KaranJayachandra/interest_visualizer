from dataclasses import dataclass
import matplotlib.pyplot as plot

def currency_round(input):
    return round(input, 2)

@dataclass
class Loan():
    balance: float = 2083190
    yearly_interest_rate: float = 13.5
    monthly_interest_points: float = yearly_interest_rate / 1200
    minimum_emi: float = 42780
    currency: str = 'INR'

@dataclass
class Budget():
    rent: float = 700
    insurance: float = 150
    travel: float = 350
    needs: float = 300
    wants: float = 300

    def get_total_budget(self):
        total = 0
        for field in self.__dataclass_fields__:
            total += getattr(self, field)
        return total

class Income():
    total_income: float = 3500
    budget = Budget()
    total_expenses: float = budget.get_total_budget()
    total_savings: float = total_income - total_expenses
    currency: str = 'EUR'

class LoanPayment():
    loan = Loan()
    income = Income()
    EXCHANGE_RATE = 85
    BAR_WIDTH = 0.3
    strategies_established: bool = False

    def establish_strategies(self, emi_candidates, candidate_currency):
        if self.loan.currency == 'INR':
            emi_min = round(self.loan.minimum_emi / self.EXCHANGE_RATE, 2)
        if candidate_currency == 'INR':
            emi_candidates == [round(x / self.EXCHANGE_RATE, 2) for x in emi_candidates]
        emi_candidates.insert(0, emi_min)
        self.emi_candidates = emi_candidates
        self.strategies_established = True

    def evaluate_strategies(self):
        self.interest_paid  = []
        self.yearly_savings = []
        self.payment_term   = []

        for emi_candidate in self.emi_candidates:
            interest = []
            current_emi = emi_candidate * self.EXCHANGE_RATE
            monthly_saving = self.income.total_savings - emi_candidate
            yearly_saving = monthly_saving * 12 * self.EXCHANGE_RATE
            current_balance = self.loan.balance
            while current_balance > 0:
                current_interest = current_balance * self.loan.monthly_interest_points
                current_balance = current_balance + current_interest
                current_balance = current_balance - current_emi
                interest.append(current_interest)
            self.payment_term.append(len(interest))
            self.interest_paid.append(currency_round(sum(interest) / 1e5))
            self.yearly_savings.append(currency_round(yearly_saving / 1e5))

    def visualize_output(self):
        _, ax1 = plot.subplots()
        ax1.set_xlabel('EMI (\u20AC)')
        ax1.set_ylabel('Lakh (\u20B9)')
        br1 = [x for x in range(len(self.emi_candidates))]
        br2 = [x + self.BAR_WIDTH for x in br1]
        ax1.bar(br1, self.interest_paid, width=self.BAR_WIDTH, label='Total Interest Paid')
        ax1.bar(br2, self.yearly_savings, width=self.BAR_WIDTH, label='Yearly Savings')
        tick_positions = [r + self.BAR_WIDTH/2 for r in range(len(self.emi_candidates))]
        ax1.set_xticks(tick_positions, self.emi_candidates)
        plot.legend(loc='upper right')

        ax2 = ax1.twinx()
        ax2.plot(br1, self.payment_term, 'k', linewidth=2, label='Payment Term')
        ax2.set_ylabel('Months')
        plot.legend(loc='center right')
        
        plot.show()

def main():
    emi_eur = [600, 800, 1000, 1200, 1400, 1600]
    lp = LoanPayment()
    lp.establish_strategies(emi_eur, 'EUR')
    lp.evaluate_strategies()
    lp.visualize_output()

if __name__ == '__main__':
    main()