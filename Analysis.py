import matplotlib.pyplot as plt
import numpy as np
from MMn import simulate_MMn


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


def plotComparison(rhos, save, names, colors, dpi=300):
    """

    :param rhos: All the rho's used to compare
    :param save: Name and path of file to save to
    :param names: Names of each method (used in legend)
    :param colors: Colors used in plot for each method
    :param dpi: DPI of figure
    :return: Figure and axis object of matplotlib figure
    """

    # Create figure
    fig, ax = plt.subplots()

    # Load data
    results = np.loadtxt(save)

    # Loop through results
    for i in range(results.shape[1] // 2):
        # Average and confidence
        average = results[:, i * 2]
        conf = results[:, i * 2 + 1]

        # Calculate left and right interval of confidence
        left = average - conf
        right = average + conf

        # Plot results
        ax.plot(rhos, average, color=colors[i], label=names[i])
        ax.fill_between(rhos, left, right, color=colors[i], alpha=0.5)

    # Plot settings
    ax.grid()
    ax.tight_layout()
    ax.legend()
    ax.set_xlabel('System load $\\rho$')
    ax.set_ylabel('Average waiting time $W$')
    fig.dpi = dpi

    return fig, ax


def compare(rhos, params, methods, save, names, colors, dpi=300):
    """
    Function used to compare the average waiting time as a function of rho for multiple queuing systems. Data is also
    saved using the save parameters.

    :param rhos: All the rho's used to compare
    :param params: Parameters for each method
    :param methods: Function names of the queuing systems
    :param save: Name and path of file to save to
    :param names: Names of each method (used in legend)
    :param colors: Colors used in plot for each method
    :param dpi: DPI of figure
    :return: Figure and axis object from matplotlib of the obtained plot
    """

    # Check if params and methods have same size
    if len(params) != len(methods):
        print('The size of parameters and methods are not the same')
        return

    # Array used to store results
    results = []

    # Loop through all rhos
    for rho in rhos:
        # Results for current rho
        res = []
        for method, param in zip(methods, params):
            # Get waiting results
            waiting = method(param[0], rho, *param[1:])

            # Get the average and confidence interval
            average, conf = statistics(waiting, False)

            # Add to list
            res += [average, conf]

        # Add to results
        results.append(res)

    # Convert to numpy array
    results = np.array(results)

    # Save the results
    np.savetxt(save, results)

    # Plot and return figure and axis objects
    return plotComparison(rhos, save, names, colors, dpi)
