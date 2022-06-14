#!/usr/bin/env python3


"""
This script simulates a hypothetical case where you sell before a dip and buy after the dip
and _still_ lose out to just hodling the whole time. In this case, you lose out due to having
to pay taxes when you sell, and the dip not making up for the difference.

In this example, you buy one share of a stock for $100. The stock proceeds to go from $100 to
$200, then $180, then $400. The tax rate is a flat 50% on all gains (no distinction for long/short
term). We then play out two scenarios. One where you sell when it hits $200 and buy back when it
hits $180. In the other scenario you hold it the whole time.

With these parameters, you get the following results:
    With selling before every drop.
    Portfolio value (day 0): 100.00
    Portfolio value (day 1): 200.00
    Portfolio value (day 2): 180.00
    Portfolio value (day 3): 400.00
    End portfolio value: 250.00

    Without selling before every drop.
    Portfolio value (day 0): 100.00
    Portfolio value (day 1): 200.00
    Price dropping, so we sell and pay tax of amount: 50.00
    Portfolio value (day 2): 150.00
    Portfolio value (day 3): 333.33
    End portfolio value: 241.67
"""


def calculate_portfolio_value(sell_before_price_drop):

    # The sequence of prices of the asset you buy.
    price_moves = [100, 200, 180, 400]

    # The rate of tax when you realize a gain.
    tax_rate = 0.50

    # The starting value of your portfolio of this asset you buy.
    cost_basis = 100
    portfolio = cost_basis

    print("Portfolio value (day 0): %.02f" % portfolio)

    # Iterate over every asset price change.
    for i in range(1, len(price_moves)):
        prev_price = price_moves[i-1]
        next_price = price_moves[i]

        # Two options, either HODL through the drop or sell before the drop
        # and buy back at the lower price.
        if not sell_before_price_drop and next_price < prev_price:

            # First, we DON'T multiple portfolio by the amount the price changed. This
            # is as though we sold our portfolio before the drop and bought it back after.

            # Calculate taxes owed so far.
            paid_taxes = (portfolio - cost_basis) * tax_rate
            print("Price dropping, so we sell and pay tax of amount: %.02f" %
                    paid_taxes)

            # Pay taxes out of portfolio.
            portfolio -= paid_taxes

            # Reset the cost basis to the new portfolio value.
            cost_basis = portfolio
        else:
            # Calculate the change in price of the underlying asset.
            multiply_by = float(next_price) / float(prev_price)

            # Multiply portfolio value by this much. Notice, we don't do this step if
            # `sell_before_price_drop` is True and the price drops. This means when
            # `sell_before_price_drop` is True, we only update portfolio value when the price
            # goes up.
            portfolio *= multiply_by

        print("Portfolio value (day %d): %.02f" % (i, portfolio))


    portfolio -= (portfolio - cost_basis) * tax_rate
    print("End portfolio value: %.02f" % portfolio)


print("With selling before every drop.")
calculate_portfolio_value(True)
print("\nWithout selling before every drop.")
calculate_portfolio_value(False)
