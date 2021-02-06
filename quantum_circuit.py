"""
qc = quantum circuit ( num qubits )

qc.x(3)
qc.cnot(2,3)
etc

qc.display()

state = initialise state()

state = qc.run ()

counts = qc.get counts
"""

import numpy as np

class quantum_circuit:

    X = np.array([[0, 1],[1, 0]])

    def __init__(self, num_qubits):
        self.num_qubits = num_qubits
        self.state = np.zeros((1,2**num_qubits))
        self.state[0,0]=1

    def x(self, X=X):
        O = np.kron(X, np.identity(2))
        self.state = np.dot(self.state, O)




qc=quantum_circuit(2)

A = np.array([0,1])
B = np.array([1,0])

print(np.kron(A,B))