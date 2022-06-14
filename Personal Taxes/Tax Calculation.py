from decimal import *

getcontext().prec = 50

singleBrackets = [
    (9700, 10),
    (39475, 12),
    (84200, 22),
    (160725, 24),
    (204100, 32),
    (510300, 35),
]
endPercent = 37

def bracketsToAmounts(brackets):
    amounts = []
    prevAmount = 0
    for bracket in brackets:
        amount = bracket[0]
        percent = bracket[1]

        amounts.append(
            (amount-prevAmount, percent)
        )
        prevAmount = amount
    return amounts

def incomeToTaxes(income, deduction, brackets):
    income -= deduction
    tax = Decimal(0)
    untaxed = income
    for amounts in bracketsToAmounts(brackets):
        amount = amounts[0]
        percent = amounts[1]
        if untaxed >= amount:
            untaxed -= amount
            tax += Decimal(amount) * (Decimal(percent) / Decimal(100))
        else:
            tax += Decimal(untaxed) * (Decimal(percent) / Decimal(100))
            untaxed = 0
            break
    if untaxed > 0:
        tax += Decimal(untaxed) * (Decimal(endPercent) / Decimal(100))
    return tax


print(incomeToTaxes(130152, 12200, singleBrackets) - 18661)
print(incomeToTaxes(423000, 12200, singleBrackets) - 89382)
