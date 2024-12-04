import numpy as np
from scipy.optimize import minimize

def portfolio_optimization(predicted_returns, risk_tolerance=0.1):
    """
    Optimize portfolio weights based on predicted returns and risk tolerance.

    :param predicted_returns: Array of predicted returns
    :param risk_tolerance: Risk tolerance level (default: 0.1)
    :return: Optimized weights
    """
    n_assets = predicted_returns.shape[1]
    mean_returns = np.mean(predicted_returns, axis=0)
    cov_matrix = np.cov(predicted_returns.T)

    def objective(weights):
        # Maximize Sharpe Ratio: (returns - risk * variance)
        return -1 * (np.dot(weights, mean_returns) - risk_tolerance * np.dot(weights.T, np.dot(cov_matrix, weights)))

    constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})
    bounds = tuple((0, 1) for _ in range(n_assets))

    result = minimize(objective, n_assets * [1. / n_assets], bounds=bounds, constraints=constraints)
    return result.x

if __name__ == "__main__":
    # Example predicted returns
    example_returns = np.random.rand(100, 4)  # Replace with real predicted returns
    weights = portfolio_optimization(example_returns)
    print("Optimized Portfolio Weights:", weights)
