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
    * Find the operator matrix using the universal operator function
    * Applies it to the state
- Performs a measurement perform multi-shot measurement of all qubits using weighted random technique
Examples of the implementation are given in the file _main.py_

## Use of the Simulation
The simulation class is imported into a python file as below:
```python
from quantum_simulator import quantum_circuit
```
First the circuit object must be defined, inputting the number of qubits in your circuit and the quantum circuit itself:
```python
qc = quantum_circuit(num_qubits, my_circuit)
```
_Note the quantum circuit is not a requirement to be input here if you are planning on using the built in functions to append gates_ <br/>
The simulation allows the following quantum gates with any number of targets, or controls if applicable:
| Gate | Function | Description | Requirements |
| ---- | ----- | ----------- | ------------ |
| X    | x   | Pauli X     | Targets      |
| Y    | y   | Pauli Y     | Targets      |
| Z    | z   | Pauli Z     | Targets      |
| H    | h   | Pauli X     | Targets      |
| CX   | mx  | (Multi) Controlled X | Controls, Targets |
| CY   | my  | (Multi) Controlled Y | Controls, Targets |
| CZ   | mz  | (Multi) Controlled Z | Controls, Targets |
| U3    | u3   | U3 Gate     | Targets, Parameters      |
| CU3   | mu3  | (Multi) Controlled U3 | Controls, Targets, Parameters |

### Creation of the Circuit
__Note that this simulator uses big endian encoding__
The circuit can be created in one of two ways:
- Defining the circuit initially as an array of dictionaries
- Using the built in functions to append a gate to the circuit
For the first option a sample circuit is provided below:
```python
my_circuit = [
{ 'gate': 'x', 'controls': [], 'targets': [1,3] },
{ 'gate': 'cx', 'controls': [1,3], 'targets': [0,2] },
{ 'gate': 'u3', 'controls': [2], 'targets': [3], 'params': { "theta": "global_1", "phi": "global_2", "lambda": np.pi/2 } }
]
```
As you can see from this example, there are three main types of gate inputs:
- __single qubit gates__ _('x', 'y', 'z', 'h')_ do not require any controls, however an empty controls list must be input
- __multi control quibit gates__ _('cx','cy','cz')_ require arrays of both controls and targets
- __parameter qubit gates__ _('u3')_ require arrays of controls, targets and parameters, with the parameters defined as above. If using global variables (as theta and phi are in the example), these must be defined later when running the circuit <br/>
The second option is to use the built in functions to append gates, as in the example below:
```python
qc.x([1,3])
qc.mx([1,3],[0,2])
qc.mu3([2],[3],{ "theta": "global_1", "phi": "global_2", "lambda": np.pi/2 })
```
This creates the same circuit as above. Note:
- __single qubit gates__ no longer require an empty controls list, only targets
- __multi controlled gates__ are called with an m as a prefix in the function
- __parameter qubit gates__ still require the parameters to be input in the same form

### Running of the Circuit
Once the circuit has been created, it can be run using the following:
```python
qc.run(params={ "global_1": np.pi/2, "global_2": 3*np.pi/2 })
counts = qc.get_counts(num_shots)
```
Note that the parameters are only needed in _qc.run()_ if global variables were called in the creation of the circuit. <br/>
The counts produces an ouput as below:
```
{'1111': 503, '1110': 497}
```