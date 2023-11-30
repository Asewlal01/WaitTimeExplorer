import simpy
import numpy as np
import matplotlib.pyplot as plt


def customer_MDn(env, mu, counter, waiting):
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


def source_MDn(env, number, arrival, capacity, counter, waiting):
    # Creating customers
    for i in range(number):
        # Create the customer
        c = customer_MDn(env, capacity, counter, waiting)
        env.process(c)

        # Time for new person to arrive
        t = np.random.exponential(1 / arrival)

        # Update time
        yield env.timeout(t)


def simulate_MDn(n, customers=100000, mu=1, rho=0.9, print_info=False):
    # Parameters
    arrival = rho * n * mu

    # Array for waiting time
    waiting = []

    # Create environment
    env = simpy.Environment()
    np.random.seed(42)
    # Create process
    counter = simpy.Resource(env, capacity=n)
    env.process(source_MDn(env, customers, arrival, mu, counter, waiting))
    env.run()

    # Get mean and standard deviation
    waiting_mean = np.mean(waiting)
    waiting_std = np.std(waiting, ddof=1)

    # Get confidence interval
    waiting_conf = 1.96 * waiting_std / np.sqrt(len(waiting))

    # Show the histogram
    plt.figure(dpi=300)
    plt.hist(waiting, bins=50, alpha=0.7)
    plt.title(f'Distribution of waiting times in a M/D/{n} queue')
    plt.xlabel('Waiting time')
    plt.ylabel('Number of customers')
    plt.yscale('log')
    plt.show()

    if print_info:
        print(f'Simulation of M/D/{n}:')
        print(f'lambda (arrival rate) = {arrival}')
        print(f'mu (service rate) = {mu}')
        print(f'Average waiting time: {waiting_mean} +- {waiting_conf}')

    return waiting, waiting_mean, waiting_conf
