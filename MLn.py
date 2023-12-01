import simpy
import numpy as np
import matplotlib.pyplot as plt


def customer(env: simpy.Environment, mu: list, p: float, counter: simpy.Resource, waiting: list):
    """
    Function used to serve customers with an expected service time described by the hyper-exponential

    :param env: Simpy environment
    :param mu: Expected service time of each exponential in the hyper-exponential
    :param p: Probability of first exponential of the hyper-exponential
    :param counter: Simpy resource object as counter
    :param waiting: List used to store the waiting time of each customer
    :return: Generator object
    """

    # Time of customer arrival
    arrival = env.now

    # Wait until customer can get serviced
    with counter.request() as req:
        yield req
        # Add waiting time
        waiting.append(env.now - arrival)

        # Time for service
        if np.random.uniform() < p:
            time = np.random.exponential(1 / mu[0])
        else:
            time = np.random.exponential(1 / mu[1])
        # Update time
        yield env.timeout(time)


def source(env: simpy.Environment, customers: int, lambda_: float, mu: list, p: float, counter: simpy.Resource,
           waiting: list):
    """
    Function used to create the customers in a M/L/n queueing system with two exponential functions
    as the hyper-exponential

    :param env: Simpy environment
    :param customers: Number of customers
    :param lambda_: Expected arrival time
    :param mu: Expected service time of each exponential of the hyper-exponential
    :param p: Probability of first exponential of the hyper-exponential
    :param counter: Simpy resource object as a counter
    :param waiting: List used to store data
    :return: Void
    """

    # Creating customers
    for i in range(customers):
        # Create the customer
        c = customer(env, mu, p, counter, waiting)
        env.process(c)

        # Time for new person to arrive
        t = np.random.exponential(1 / lambda_)

        # Update time
        yield env.timeout(t)


def simulate_MLn(customers: int, rho: float, mu: list, p: float, n=1, seed=None):
    """
    Function used to simulate a M/L/n queuing system

    :param customers: Number of customers
    :param rho: System load
    :param mu: Expected service time for each exponential of the hyper-exponential
    :param p: Probability of first exponential of the hyper-exponential
    :param n: Number of servers
    :param seed: Optional seed to reproduce results
    :return: Waiting time for each customer
    """

    # Calculate lambda
    lambda_ = rho * n * (p * mu[0] + (1 - p) * mu[1])

    # Array for waiting time
    waiting = []

    # Set seed
    np.random.seed(seed)

    # Create environment
    env = simpy.Environment()

    # Create process
    counter = simpy.Resource(env, capacity=n)
    env.process(source(env, customers, lambda_, mu, p, counter, waiting))
    env.run()

    return waiting
