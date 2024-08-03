from collections import namedtuple
from typing import List


def create_table(N: int, M: int) -> List[List[int]]:
    """
    Creates a table (list of lists) with M columns and N rows, filled with 0.
    The table is of dimension (N+1)x(M+1).

    Args:
        N (int): The number of rows (+1) in the table. The index of the last row.
        M (int): The number of columns (+1) in the table. The index of the last column.
    """
    return [[0] * (M + 1) for _ in range(N + 1)]


InvestmentOption = namedtuple(
    "InvestmentOption", ["required_investment", "potential_profit"]
)
"""
A tuple class representing a single investment option.

Attributes:
    required_investment: int
        The required amount you need to invest to get the potential profit.
    potential_profit: int
        The potential amount you can earn by investing.
"""

def optimize_investment(
    options: List[InvestmentOption],
    max_budget: int
) -> List[List[int]]:
    """
    Calculates the table of best profits for the given maximal budget.

    Args:
        options (List[InvestmentOption]): List of InvestmentOption objects representing different options.
        max_budget (int): The maximum amount of money to invest.
    """
    # TODO: Create the table with the appropriate dimensions. Replace the '<N_rows>' and '<M_columns' arguments.
    N = len(options)
    M = max_budget // 1000
    table = create_table(N, M)

    # TODO: Iterate through the options in O(n*m) and calculate the optimal profits.
    for i in range(1, N + 1):
        for j in range(1, M + 1):
            required_investment = options[i - 1].required_investment // 1000
            potential_profit = options[i - 1].potential_profit
            if required_investment <= j:
                second_side = potential_profit + table[i - 1][j - required_investment]
                if table[i - 1][j] >= second_side:
                    table[i][j] = table[i - 1][j]
                else:
                    table[i][j] = second_side
            else:
                table[i][j] = table[i - 1][j]

    return table
