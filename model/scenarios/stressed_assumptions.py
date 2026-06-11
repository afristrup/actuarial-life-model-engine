from model.assumptions.expense import (
    ExpenseResult
)

class StressedMortalityTable:
    """
    Mortality provider wrapper applying
    scenario-based mortality stresses.

    Responsibilities:
    - wrap an existing mortality provider
    - apply mortality stress overlays
    - preserve mortality provider interface

    Does NOT:
    - perform projection logic
    - perform valuation logic
    - know SCR calculations
    """

    def __init__(
        self,
        base_mortality,
        mortality_multiplier: float = 1.0
    ):

        self.base_mortality = base_mortality

        self.mortality_multiplier = (
            mortality_multiplier
        )

    def qx(self, policy, age: int) -> float:
        """
        Resolve stressed mortality.
        """

        base_qx = self.base_mortality.qx(
            policy,
            age
        )

        stressed_qx = (
            base_qx
            * self.mortality_multiplier
        )

        return min(stressed_qx, 1.0)

    def px(self, policy, age: int) -> float:

        return 1 - self.qx(policy, age)

    def __repr__(self):

        return (
            f"StressedMortalityTable("
            f"multiplier="
            f"{self.mortality_multiplier}"
            f")"
        )
    
class StressedLapseTable:
    """
    Lapse provider wrapper applying
    scenario-based lapse stresses.

    Responsibilities:
    - wrap an existing lapse provider
    - apply lapse stress overlays
    - preserve lapse provider interface
    """

    def __init__(
        self,
        base_lapse,
        lapse_multiplier: float = 1.0
    ):

        self.base_lapse = base_lapse

        self.lapse_multiplier = (
            lapse_multiplier
        )

    def lapse_rate(
        self,
        policy,
        t: int
    ) -> float:
        """
        Resolve stressed lapse rate.
        """

        if self.base_lapse is None:

            return 0.0
        
        base_lapse_rate = (
            self.base_lapse.lapse_rate(
                policy,
                t
            )
        )

        stressed_lapse_rate = (
            base_lapse_rate
            * self.lapse_multiplier
        )

        return min(
            stressed_lapse_rate,
            1.0
        )

    def __repr__(self):

        return (
            f"StressedLapseTable("
            f"multiplier="
            f"{self.lapse_multiplier}"
            f")"
        )
    
class StressedYieldCurve:
    """
    Yield curve provider wrapper applying
    scenario-based interest rate stresses.

    Responsibilities:
    - wrap an existing yield curve provider
    - apply interest rate stress overlays
    - preserve yield curve provider interface

    Does NOT:
    - perform valuation logic
    - perform interpolation
    - perform scenario orchestration
    """

    def __init__(
        self,
        base_yield_curve,
        interest_rate_shift: float = 0.0
    ):

        self.base_yield_curve = (
            base_yield_curve
        )

        self.interest_rate_shift = (
            interest_rate_shift
        )

    def discount_factor(
        self,
        t: float
    ) -> float:
        """
        Resolve stressed discount factor.
        """

        base_rate = (
            self.base_yield_curve
            ._resolve_rate(t)
        )

        stressed_rate = (
            base_rate
            + self.interest_rate_shift
        )

        return 1 / (
            (1 + stressed_rate) ** t
        )

    def __repr__(self):

        return (
            f"StressedYieldCurve("
            f"interest_rate_shift="
            f"{self.interest_rate_shift}"
            f")"
        )
    
class StressedExpenseTable:
    """
    Expense provider wrapper applying
    scenario-based expense stresses.

    Responsibilities:
    - wrap an existing expense provider
    - apply expense stress overlays
    - preserve expense provider interface

    Does NOT:
    - perform projection logic
    - perform valuation logic
    - know SCR calculations
    """

    def __init__(
        self,
        base_expense_table,
        expense_multiplier: float = 1.0
    ):

        self.base_expense_table = (
            base_expense_table
        )

        self.expense_multiplier = (
            expense_multiplier
        )

    def expenses(
        self,
        policy,
        t: int
    ) -> ExpenseResult:
        """
        Resolve stressed expenses.
        """

        if self.base_expense_table is None:

            return ExpenseResult.zero()
        
        base_result = (
            self.base_expense_table.expenses(
                policy,
                t
            )
        )

        stressed_acquisition = (
            base_result.acquisition_expense
            * self.expense_multiplier
        )

        stressed_maintenance = (
            base_result.maintenance_expense
            * self.expense_multiplier
        )

        return ExpenseResult(
            acquisition_expense=
                stressed_acquisition,

            maintenance_expense=
                stressed_maintenance
        )

    def __repr__(self):

        return (
            f"StressedExpenseTable("
            f"expense_multiplier="
            f"{self.expense_multiplier}"
            f")"
        )