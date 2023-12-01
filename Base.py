
import numpy as np
import simpy

def source(env, number, arrival_rate, counter, wait_times, service_rate):
    for i in range(number):
        c = customer(env, counter, wait_times, service_rate)
        env.process(c)
        t = np.random.exponential(1/arrival_rate)
        yield env.timeout(t)

def customer(env, counter, wait_times, service_rate):
    arrive = env.now

    with counter.request() as req:
        # Wait for the counter
        yield req

        wait = env.now - arrive
        wait_times.append(wait)

        service_time = np.random.exponential(1/service_rate)
        yield env.timeout(service_time)

def queueing_system(customers: int, lambda_: float, mu: float, num_servers: int, seed= None):
    # Setup and start the simulation
    np.random.seed(seed)
    env = simpy.Environment()

    wait_times = []

    # Start processes and run
    counter = simpy.Resource(env, capacity=num_servers)
    env.process(source(env, customers, lambda_, counter, wait_times, mu))
    env.run()

    return wait_times


