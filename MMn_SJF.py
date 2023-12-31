import simpy
import numpy as np


def customer(env: simpy.Environment, mu: float, counter: simpy.PriorityResource, waiting: list):
    """
    Function used to serve customers with an expected service time of mu. Priority are given to customers with lower
    service time (SJF scheduling).

    :param env: Simpy environment
    :param mu: Expected service rate of each server
    :param counter: Simpy resource object as counter
    :param waiting: List used to store the waiting time of each customer
    :return: Generator object
    """

    # Time of customer arrival
    arrival = env.now

    # Time for service
    time = np.random.exponential(1 / mu)

    # Wait until customer can get serviced with the time as its priority
    with counter.request(priority=time) as req:
        yield req

        # Add waiting time
        waiting.append(env.now - arrival)
        # Update time
        yield env.timeout(time)


def source(env: simpy.Environment, customers: int, lambda_: float, mu: float, counter: simpy.PriorityResource,
           waiting: list):
    """
    Function used to create the customers.

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


def simulate_MMn_SJF(customers: int, rho: float, mu: float, n=1, seed=None):
    """
    Function used to simulate the queue using SJF scheduling.

    :param customers: Number of customers
    :param rho: System load
    :param mu: Expected service rate of each server
    :param n: Number of servers
    :param seed: Optional seed to reproduce results
    :return: Waiting time for each customer
    """
    # Calculate lambda
    lambda_ = rho * n * mu

    # Create list for storing waiting times
    waiting = []

    # Set seed
    np.random.seed(seed)

    # Create environment
    env = simpy.Environment()

    # Create counter
    counter = simpy.PriorityResource(env, capacity=n)

    # Run process
    env.process(source(env, customers, lambda_, mu, counter, waiting))
    env.run()

    return waiting

