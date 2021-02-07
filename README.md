# Quantum Circuit Simulator
This project is an implementation of a quantum computer simulator. 
This was written for my submission to [Quantum Open Source Foundation's Quantum Computing Mentorship](https://github.com/quantastica/qosf-mentorship/blob/master/qosf-simulator-task.ipynb)

## Overview
The only requirement for the running of the simulation is the installation of the Python3 package __Numpy__.
The simulator implements the following:
- Initialisation of the ground state
- Reads a quantum circuit with a range of gates (listed below)
- Allows the appending of gates to a quantum circuit
- Runs the quantum circuit and for each gate: 
    * Find the operator matrix
    * Applies it to the state
- Performs a measurement perform multi-shot measurement of all qubits using weighted random technique

## Use of the Simulation
The simulation class is imported into a python file as below:
'''python
from quantum_simulator import quantum_circuit
'''
