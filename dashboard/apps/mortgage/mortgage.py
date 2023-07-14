#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

import dataclasses
import decimal
import time
from decimal import Decimal

MONTHS_IN_YEAR = 12
DOLLAR_QUANTIZE = decimal.Decimal(".01")


def dollar(f, round_ceil=decimal.ROUND_CEILING):
    """
    This function rounds the passed float to 2 decimal places.
    """
    if not isinstance(f, decimal.Decimal):
        f = decimal.Decimal(str(f))
    return f.quantize(DOLLAR_QUANTIZE, rounding=round_ceil)


@dataclasses.dataclass
class Mortgage:
    interest: float
    months: int
    amount: Decimal
    monthly_surplus:Decimal=Decimal("0.00")
    def __post_init__(self):
        self.amount = dollar(self.amount)
        self.monthly_surplus = dollar(self.monthly_surplus)


    def month_growth(self):
        return 1.0 + self.interest / MONTHS_IN_YEAR

    def apy(self):
        return self.month_growth() ** MONTHS_IN_YEAR - 1

    def loan_years(self):
        return float(self.months) / MONTHS_IN_YEAR

    def loan_months(self):
        return self.months

    def monthly_payment(self):
        pre_amt = (
                float(self.amount)
                * self.interest
                / (
                        float(MONTHS_IN_YEAR)
                        * (1.0 - (1.0 / self.month_growth()) ** self.loan_months())
                )
        )
        return dollar(pre_amt, round_ceil=decimal.ROUND_CEILING)

    def total_value(self, m_payment):
        return (
                m_payment
                / self.interest
                * (
                        float(MONTHS_IN_YEAR)
                        * (1.0 - (1.0 / self.month_growth()) ** self.loan_months())
                )
        )

    def annual_payment(self):
        return self.monthly_payment() * MONTHS_IN_YEAR

    def total_payout(self):
        return dollar(self.monthly_payment() * dollar(self.loan_months()))
    def total_interest(self):
        return self.total_payout()-self.amount

    def monthly_payment_schedule(self):
        monthly = self.monthly_payment()
        balance = dollar(self.amount)
        rate = decimal.Decimal(str(self.interest)).quantize(decimal.Decimal(".000001"))
        while True:
            interest_unrounded = balance * rate * decimal.Decimal(1) / MONTHS_IN_YEAR
            interest = dollar(interest_unrounded, round_ceil=decimal.ROUND_HALF_UP)
            if monthly >= balance + interest:
                yield float(balance), float(interest), float(rate)
                break
            principle = monthly - interest
            yield float(balance), float(interest), float(rate)
            balance -= principle

    def calculate_mortgage_length(self, monthly_payment):
        remaining_principal = self.amount
        month_int = Decimal(self.month_growth())
        months = 0
        while remaining_principal > 0:
            interest = dollar(month_int * remaining_principal)
            remaining_principal = dollar(interest - monthly_payment)
            if remaining_principal > float(self.amount):
                # Break the loop if the remaining principal is not decreasing
                return -1
            if remaining_principal == float(self.amount):
                return 0
            months += 1

        return months


class RefactorMortgage:
    @staticmethod
    def byMonthlyPayment(mortgage, monthly_payment):
        months = mortgage.calculate_mortgage_length(monthly_payment)
        if months == -1:
            raise Exception("Payment Not Large Enough")
        if months == 0:
            print("Payment of just interest")
        print(f"Shifting mortgage to a {months} month time scale @ {mortgage.interest} %")
        return Mortgage(mortgage.interest, months, mortgage.amount)

    @staticmethod
    def byInterest(mortgage, interest):
        return Mortgage(interest, mortgage.months, mortgage.amount)

    @staticmethod
    def byTerm(mortgage, term):
        return Mortgage(mortgage.interest, term, mortgage.amount)

    @staticmethod
    def byPrinciple(mortgage, principle):
        return Mortgage(mortgage.interest, mortgage.months, principle)
    @staticmethod
    def byExtraInstallment(mortgage, extra_installment):
        return Mortgage(mortgage.interest, mortgage.months, mortgage.principle, monthly_surplus=extra_installment)

def print_summary(m):
    print("{0:>25s}:  {1:>12.6f}".format("Rate", m.interestAlter))
    print("{0:>25s}:  {1:>12.6f}".format("Month Growth", m.month_growth()))
    print("{0:>25s}:  {1:>12.6f}".format("APY", m.apy()))
    print("{0:>25s}:  {1:>12.0f}".format("Payoff Years", m.loan_years()))
    print("{0:>25s}:  {1:>12.0f}".format("Payoff Months", m.loan_months()))
    print("{0:>25s}:  {1:>12.2f}".format("Amount", m.amount))
    print("{0:>25s}:  {1:>12.2f}".format("Monthly Payment", m.monthly_payment()))
    print("{0:>25s}:  {1:>12.2f}".format("Annual Payment", m.annual_payment()))
    print("{0:>25s}:  {1:>12.2f}".format("Total Payout", m.total_payout()))

    print("\n{:>10s} | {:>10s} | {:>10s}".format("Balance", "Interest", "Rate"))
    print("-" * 40)
    for balance, interest, rate in m.monthly_payment_schedule():
        print(
            "{:>10.2f} | {:>10.2f} | {:>10.6f}".format(balance, interest, float(rate))
        )


# m = Mortgage(0.03, 360, 100_000)
# print(m,"\n\n")
#
# print("changing monthly payment to 250 (interest only)")
# y = RefactorMortgage.byMonthlyPayment(m,250)
# print(y)
# print("\nchanging monthly payment to above 250")
# z = RefactorMortgage.byMonthlyPayment(m,700)
# print(z)
# print("\nchanging below threashold")
# a = RefactorMortgage.byMonthlyPayment(m,100)
# print(a)

