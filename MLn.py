import simpy
import numpy as np
import matplotlib.pyplot as plt


def customer_MLn(env, mu, p, counter, waiting):
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


def source_MLn(env, number, arrival, capacity, p, counter, waiting):
    # Creating customers
    for i in range(number):
        # Create the customer
        c = customer_MLn(env, capacity, p, counter, waiting)
        env.process(c)

        # Time for new person to arrive
        t = np.random.exponential(1 / arrival)

        # Update time
        yield env.timeout(t)


def simulate_MLn(n, customers=100000, mu=[1., 1 / 5], p=0.75, rho=0.9, print_info=False):
    # Parameters
    arrival = rho * n * (0.75 * mu[0] + 0.25 * mu[1])

    # Array for waiting time
    waiting = []

    # Create environment
    env = simpy.Environment()
    np.random.seed(42)
    # Create process
    counter = simpy.Resource(env, capacity=n)
    env.process(source_MLn(env, customers, arrival, mu, p, counter, waiting))
    env.run()

    # Get mean and standard deviation
    waiting_mean = np.mean(waiting)
    waiting_std = np.std(waiting, ddof=1)

    # Get confidence interval
    waiting_conf = 1.96 * waiting_std / np.sqrt(len(waiting))

    if print_info:
        print(f'Simulation of M/L/{n}:')
        print(f'lambda (arrival rate) = {arrival}')
        print(f'mu (service rate) = {mu}')
        print(f'{waiting_mean} +- {waiting_conf}')

    return waiting, waiting_mean, waiting_conf