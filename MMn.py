import numpy as np
import simpy


def customer(env: simpy.Environment, mu: float, counter: simpy.Resource, waiting: list):
    """
    Function used to serve customers with an expected service time of mu from an exponential distribution.

    :param env: Simpy environment
    :param mu: Expected service rate of each server
    :param counter: Simpy resource object as counter
    :param waiting: List used to store the waiting time of each customer
    :return: Generator object
    """
    # Customer has arrived
    arrive = env.now

    # Wait on counter
    with counter.request() as req:
        yield req

        # Get waiting time
        wait = env.now - arrive
        waiting.append(wait)

        # Service time
        service_time = np.random.exponential(1 / mu)

        # Update time
        yield env.timeout(service_time)


def source(env: simpy.Environment, customers: int, lambda_: float, mu: float, counter: simpy.Resource, waiting: list):
    """
    Function used to create the customers in a M/M/n queueing system.

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


def simulate_MMn(customers: int, rho: float, mu: float, n=1, seed=None):
    """
    Function used to simulate a M/M/n queuing system

    :param customers: Number of customers
    :param rho: System load
    :param mu: Expected service rate of each server
    :param n: Number of servers
    :param seed: Optional seed to reproduce results
    :return: Waiting time for each customer
    """

    # Calculate lambda
    lambda_ = rho * n * mu

    # List for saving results
    wait_times = []

    # Setup and start the simulation
    np.random.seed(seed)
    env = simpy.Environment()

    # Start processes and run
    counter = simpy.Resource(env, capacity=n)
    env.process(source(env, customers, lambda_, mu, counter, wait_times))
    env.run()

    return wait_times
