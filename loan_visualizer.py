from dataclasses import dataclass
from dash import Dash, dcc, html

def currency_round(input):
    return round(input, 2)

@dataclass
class Loan():
    balance: float = 2083190 / 85
    yearly_interest_rate: float = 13.5
    monthly_interest_points: float = yearly_interest_rate / 1200
    minimum_emi: float = 42780 / 85

    def update_rate(self, rate):
        self.yearly_interest_rate = rate
        self.monthly_interest_points = rate / 1200      

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
    total_expenses: float = 2000
    total_savings: float = total_income - total_expenses

class LoanPayment():
    loan = Loan()
    income = Income()

    def establish_strategies(self, emi_candidates):
        emi_candidates.insert(0, self.loan.minimum_emi)
        self.emi_candidates = emi_candidates

    def evaluate_strategies(self):
        self.interest_paid  = []
        self.yearly_savings = []
        self.payment_term   = []

        for emi_candidate in self.emi_candidates:
            interest = []
            monthly_saving = self.income.total_savings - emi_candidate
            yearly_saving = monthly_saving * 12
            current_balance = self.loan.balance
            while current_balance > 0:
                current_interest = current_balance * self.loan.monthly_interest_points
                current_balance = current_balance + current_interest
                current_balance = current_balance - emi_candidate
                interest.append(current_interest)
            self.payment_term.append(len(interest))
            self.interest_paid.append(currency_round(sum(interest)))
            self.yearly_savings.append(currency_round(yearly_saving))

if __name__ == '__main__':
    emi_eur = [600, 800, 1000, 1200, 1400]
    lp = LoanPayment()
    lp.establish_strategies(emi_eur)
    lp.evaluate_strategies()
    app = Dash(__name__)

    app.layout = html.Div(
        children=[
            html.H1(children="Loan Visualizer"),
            dcc.Graph(
                figure={
                    "data": [
                        {
                            "x": lp.emi_candidates,
                            "y": lp.interest_paid,
                            "type": "bar",
                            "name": "Interest Paid"
                        },
                        {
                            "x": lp.emi_candidates,
                            "y": lp.yearly_savings,
                            "type": "bar",
                            "name": "Yearly Savings"
                        },
                    ],
                    "layout": {"title": "Total Interest Paid"},
                },
            )
        ]
    )
    app.run_server(debug=True)