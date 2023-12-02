import matplotlib.pyplot as plt
import numpy as np


def visualize(waiting, title='Distribution of waiting times', color='blue', bins=100, yscaling=None, dpi=300):
    """
    Function used to visualize the distribution of the waiting time

    :param waiting: Array with the waiting time of the customers
    :param title: Title of figure
    :param color: Color used for bins in histogram
    :param bins: Number of bins in the histogram
    :param yscaling: Option scaling of the y-axis e.g. logarithmic
    :param dpi: DPI of figure
    :return: Figure and axis of Matplotlib object
    """

    # Create figure
    fig, ax = plt.subplots(dpi=dpi)

    # Plot histogram
    fig = plt.hist(waiting, color=color, bins=bins, density=True)

    # Add labels and title
    plt.xlabel('Waiting time')
    plt.ylabel('Frequency')
    plt.title(title)

    # Set grid
    plt.grid()

    # Optional scaling of y-axis
    if yscaling is not None:
        plt.yscale(yscaling)

    return fig, ax


def statistics(waiting, print_info=True):
    """
    Function used to return the mean and confidence interval of the waiting times

    :param waiting: Array with the waiting time of the customers
    :param print_info: Boolean that represents if average +- confidence should be printed
    :return: Mean and confidence interval
    """

    # Compute the mean and the standard deviation
    wait_avg = np.mean(waiting)
    wait_std = np.std(waiting, ddof=1)

    # Calculate confidence interval from standard deviation
    wait_conf = wait_std * 1.96 / len(waiting) ** 0.5

    # Print the result
    if print_info:
        print(f'Average waiting time: {wait_avg} +- {wait_conf}')

    return wait_avg, wait_conf
