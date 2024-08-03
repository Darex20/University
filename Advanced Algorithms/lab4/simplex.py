import numpy as np

import numpy as np
from typing import Tuple


class SimpleLP:
    """
    Represents simple LP problem with tableau and indexing-vector of basis-columns

    members:
        self.tableau - stored simplex tableau

        self.basis  - contains ordered indices of identity submatrix within tableau. 
            This enables reading the solution from tableau
    """

    def __init__(self, A, b, c):
        """Creates simplex tableau assuming canonical form and b>=0 (self.tableau)

        Also creates an index-vector of basis-columns in the tableau (self.basis). 


        Args:
            A (np.array): canonical LP A (matrix)
            b (np.array): canonical LP b (1-D vector)
            c (np.array): canonical LP c (1-D vector)
        """
        c = np.array(c)
        b = np.array(b)
        A = np.array(A)
        m = A.shape[0]
        n = c.shape[0]

        zeroth_row = np.hstack([c, [0]*(m+1)])
        bottom_pack = np.hstack((A, np.identity(m), b.reshape(m, 1)))

        self.tableau = np.vstack((zeroth_row, bottom_pack))

        self.basis = np.arange(n, n+m) # identity submatrix in such specific problems is in the last columns

    def readSolution(self) -> Tuple[np.float32, np.array]:
        """Reads off the full solution from the tableau

        Returns:
            Tuple[np.float32, np.array]: returns objective value and 1-D vector of decisions
        """

        # TODO: add your code for objective function value here (None is not solution)
        obj = -self.tableau[0, -1]

        decisions = np.zeros((self.tableau.shape[1]-1))
        decisions[self.basis] = self.tableau[1:, -1] # uses basis index vector to assign values to basic variables

        return obj, decisions


class NaiveSimplex:
    """

    Represents all functionalities of "naive" simplex

    Raises:
        ValueError: if pivot row is 0

    """

    @staticmethod
    def pivot(lp_problem: SimpleLP, row: int, col: int) -> SimpleLP:
        """Does Gauss-Jordan elimination around the (row,col) 
        element of simplex tableau

        Args:
            lp_problem (SimpleLP): LP over which to operate
            row (int): pivot's row
            col (int): pivot's column

        Raises:
            ValueError: pivot cannot be in the row of the reduction factors

        Returns:
            SimpleLP: returns reference to LP (for chaining)
        """
        
        if row == 0: # cannot pivot around zeroth row in tableau
            raise ValueError

        # TODO: add your code here - tableau must be pivoted and basis updated (watch the order in basis vector!)
        tableau = lp_problem.tableau
        tableau[row, :] = tableau[row, :] / tableau[row, col]
        num_rows, _ = tableau.shape
        for i in range(num_rows):
            if i != row:
                tableau[i, :] = tableau[i, :] - tableau[i, col] * tableau[row, :]
        lp_problem.basis[row - 1] = col

        return lp_problem

    @staticmethod
    def solve(lp_problem: SimpleLP) -> SimpleLP:
        """Solves the input LP

        Args:
            lp_problem (SimpleLP): Input LP to be solved

        Returns:
            SimpleLP: returns None if the problem is unbounded, or reference to the LP otherwise
        """

        # TODO: add your code here - should call pivot method, like this: NaiveSimplex.pivot(lp_problem)
        while np.any(lp_problem.tableau[0, :-1] < 0):
            column = np.where(lp_problem.tableau[0, :-1] < 0)[0][0]
            ratio = lp_problem.tableau[1:, -1] / lp_problem.tableau[1:, column] 
            min_pos = ratio[ratio > 0].min() # finding min ratio
            i = np.where(ratio == min_pos)[0][0]
            lp_problem = NaiveSimplex.pivot(lp_problem, i + 1, column) # pivot

        return lp_problem