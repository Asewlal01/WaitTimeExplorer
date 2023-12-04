# Wait Time Explorer
This repository contains Python code used for determining the average waiting time of queueing systems in different enviroments (distribution and scheduling). This project focuses on using Discrete Event Simulation to simulate the queue, and use the waiting time of each customer to determine the average waiting time.

# Dependencies
The following dependencies have to be installed:
- NumPy
- SciPy
- Matplotlib
- SimPy

# Structure
- main.ipynb: Main file of this repository. All implemented functions and visualizition takes place within this file.
- MMn.py: Implementation of a M/M/n queueing system using the FIFO scheduling method
- MMn_SJF.py: Implementation of a M/M/n queuing system but uses SJF instead of FIFO
- ExpectedWaitTime.py: Implementation of the expected waiting time of a M/M/n queue using FIFO
- MDN.py: Implementation of a M/D/n queuing system
- MLN.py: Implementation of a M/L/n queuing system
- Analysis.py: This file constains functions used to analyse results obtained from the simulations. It contains some visualization methods, and statistical methods to get the average waiting time with the 95% confidence interval
