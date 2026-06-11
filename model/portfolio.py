"""
Portfolio aggregation layer.

Core responsibilities:
- aggregate policy-level valuation results
- support weighted model points
- produce portfolio-level structured outputs

Key design principles:
- portfolio layer contains no actuarial mechanics
- valuation delegated to valuation engine
- aggregation logic isolated from analytics

Architecture flow:
ValuationResult
→ Portfolio aggregation
→ PortfolioResult
"""

from model.valuation import value_policy
from model.results import (
    PortfolioResult,
    ValuationRow
)


class Portfolio:
    """
    Represents a portfolio of insurance policies.

    Responsibilities:
    - store policies
    - aggregate valuation results

    No projection or actuarial mechanics belong here.
    """

    def __init__(self, policies):

        self.policies = policies

    def value(self, assumptions, return_breakdown=False):
        """
        Calculate aggregated portfolio valuation.
        """

        pv_premiums = 0.0
        pv_claims = 0.0
        pv_expenses = 0.0
        # Aggregate portfolio emergence by projection period.
        breakdown_by_t = {}

        # Handle empty portfolio explicitly
        if not self.policies:

            return PortfolioResult(
                pv_premiums=0.0,
                pv_claims=0.0,
                pv_expenses=0.0,
                net_value=0.0,
                policy_count=0
            )

        for policy in self.policies:

            result = value_policy(
                policy,
                assumptions,
                return_breakdown=return_breakdown
            )

            weight = policy.weight

            pv_premiums += result.pv_premiums * weight
            pv_claims += result.pv_claims * weight
            pv_expenses += result.pv_expenses * weight

            if return_breakdown and result.breakdown is not None:

                for row in result.breakdown:

                    t = row.t

                    if t not in breakdown_by_t:

                        breakdown_by_t[t] = ValuationRow(
                            t=row.t,
                            age=row.age,
                            discount_factor=row.discount_factor,
                            lapse_rate=row.lapse_rate,
                            expected_premium=0.0,
                            expected_claim=0.0,
                            expected_lapse=0.0,
                            net_cashflow=0.0,
                            pv_premium=0.0,
                            pv_claim=0.0,
                            pv_acquisition_expense=0.0,
                            pv_maintenance_expense=0.0,
                            pv_total_expense=0.0,
                            pv_net=0.0,
                            cum_profit=0.0,
                            cum_cashflow=0.0
                        )

                    agg_row = breakdown_by_t[t]

                    agg_row.expected_premium += row.expected_premium * weight
                    agg_row.expected_claim += row.expected_claim * weight
                    agg_row.expected_lapse += row.expected_lapse * weight
                    agg_row.net_cashflow += row.net_cashflow * weight
                    agg_row.pv_premium += row.pv_premium * weight
                    agg_row.pv_claim += row.pv_claim * weight
                    agg_row.pv_acquisition_expense += row.pv_acquisition_expense * weight
                    agg_row.pv_maintenance_expense += row.pv_maintenance_expense * weight
                    agg_row.pv_total_expense += row.pv_total_expense * weight
                    agg_row.pv_net += row.pv_net * weight

        net_value = (
            pv_premiums
            - pv_claims
            - pv_expenses
        )

        breakdown = None

        if return_breakdown:

            breakdown = [
                breakdown_by_t[t]
                for t in sorted(breakdown_by_t.keys())
            ]

            cum_profit = 0.0
            cum_cashflow = 0.0

            for row in breakdown:

                cum_profit += row.pv_net
                cum_cashflow += row.net_cashflow

                row.cum_profit = cum_profit
                row.cum_cashflow = cum_cashflow

        return PortfolioResult(
            pv_premiums=pv_premiums,
            pv_claims=pv_claims,
            pv_expenses=pv_expenses,
            net_value=net_value,
            policy_count=len(self.policies),
            breakdown=breakdown
        )