from quantum_simulator import quantum_circuit
import numpy as np

"""EXAMPLE 1 - PREDEFINING THE CIRCUIT"""

# my_circuit = [
# { 'gate': 'x', 'controls': [], 'targets': [1,3] },
# { 'gate': 'cx', 'controls': [1,3], 'targets': [0,2] },
# { 'gate': 'u3', 'controls': [2], 'targets': [3], 'params': { "theta": "global_1", "phi": "global_2", "lambda": np.pi/2 } }
# ]

# qc = quantum_circuit(4, my_circuit)

# qc.run(params={ "global_1": np.pi/2, "global_2": 3*np.pi/2 })
# counts = qc.get_counts(1000)
# print(counts)

"""EXAMPLE 2 - USING BUILT IN FUNCTIONS TO DEFINE CIRCUIT"""

# qc = quantum_circuit(4)

# qc.x([1,3])
# qc.mx([1,3],[0,2])
# qc.mu3([2],[3],{ "theta": "global_1", "phi": "global_2", "lambda": np.pi/2 })

# qc.run(params={ "global_1": np.pi/2, "global_2": 3*np.pi/2 })
# counts = qc.get_counts(1000)
# print(counts)