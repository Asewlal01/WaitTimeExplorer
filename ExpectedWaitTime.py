from math import factorial


def expectedWait(rho, mu, n):
    """
    Function used to compute the expected waiting time for a M/M/n queuing system

    :param rho: System load
    :param mu: Service rate
    :param n: Number of servers
    :return: The expected waiting time
    """

    # Compute numerator of pi
    numerator = (n * rho) ** n / factorial(n)

    # Compute sum in denominator of pi
    denominator = 0
    for i in range(n):
        denominator += (n * rho) ** i / factorial(i)

    # Compute denominator
    denominator = denominator * (1 - rho) + numerator

    return numerator / denominator / (1 - rho) / (mu * n)
