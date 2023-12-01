import simpy
import numpy as np


def customer(env: simpy.Environment, mu: float, counter: simpy.Resource, waiting: list):
    """
    Function used to serve customers with a constant service time of mu.

    :param env: Simpy environment
    :param mu: Expected service rate of each server
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
        time = 1 / mu

        # Update time
        yield env.timeout(time)


def source(env: simpy.Environment, customers: int, lambda_: float, mu: float, counter: simpy.Resource,
           waiting: list):
    """
    Function used to create the customers in a M/D/n queueing system

    :param env: Simpy environment
    :param customers: Number of customers
    :param lambda_: Expected arrival rate
    :param mu: Expected service rate of each server
    :param counter: Simpy resource object as a counter
    :param waiting: List used to store data
    :return: Void
    """

    # Creating customers
    for i in range(customers):
        # Create the customer
        c = customer(env, mu, counter, waiting)
        env.process(c)

        # Time for new person to arrive
        t = np.random.exponential(1 / lambda_)

        # Update time
        yield env.timeout(t)


def simulate_MDn(customers: int, rho: float, mu: float, n=1, seed=None):
    """
    Function used to simulate a M/D/n queuing system

    :param customers: Number of customers
    :param rho: System load
    :param mu: Expected service rate of each server
    :param n: Number of servers
    :param seed: Optional seed to reproduce results
    :return: Waiting time for each customer
    """

    # Calculate lambda
    lambda_ = rho * n * mu

    # Array for waiting time
    waiting = []

    # Create environment
    env = simpy.Environment()
    np.random.seed(seed)

    # Create process
    counter = simpy.Resource(env, capacity=n)
    env.process(source(env, customers, lambda_, mu, counter, waiting))

    # Run process
    env.run()

    return waiting