import numpy as np

class Monomial:

    def __init__(self, a_vec):
        self.a_vec = np.array(a_vec)
        self.dimension = len(a_vec)
    
    def evaluate(self, input_vec):
        assert self.dimension == len(input_vec), "Input data dimension is different from the monomial's dimension"
        return np.prod(np.power(input_vec, self.a_vec))

class Monomial_Basis:

    def __init__(self, chi, dimension):
        permutations = Monomial_Basis._get_all_permutations(chi, dimension)
        self.monomials = list(map(lambda x: Monomial(x), permutations))
    
    @staticmethod
    def _get_all_permutations(chi, dimension):
        if chi == 0:
            return [[0]*dimension]
        elif dimension == 1:
            return [[i] for i in range(chi+1)]
        else:
            results = []
            for i in range(chi+1):
                result = map(lambda x: [i] + x, Monomial_Basis._get_all_permutations(chi - i, dimension-1))
                results += list(result)
            return results
    
    def evaluate(self, X):
        return np.array(list(map(lambda m: m.evaluate(X), self.monomials)))

class Regression:

    def __init__(self, X_mat, Y, chi=2, payoff_func=lambda x: np.sum(x)):
        assert len(X_mat.shape) == 2, "X in the regression should be a 2d matrix"

        self.dimension = len(X_mat[0])
        self.basis = Monomial_Basis(chi, self.dimension)
        
        index = [i for i in range(len(X_mat)) if payoff_func(X_mat[i]) > 0]
        target_X, target_Y = X_mat[index], Y[index]

        target_matrix_A = np.array(list(map(lambda x: self.basis.evaluate(x), target_X)))
        self.coefficients = np.linalg.lstsq(target_matrix_A, target_Y, rcond=None)[0]

    def evaluate(self, X):
        """
        X: a numpy array of input data (e.g., asset prices)
        """
        assert len(X) == self.dimension, "input vector X doesn't meet the regression dimension"
        monomial_terms = self.basis.evaluate(X)
        return np.sum(np.multiply(self.coefficients, monomial_terms))