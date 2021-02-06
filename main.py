from quantum_simulator import quantum_circuit
import numpy as np

qc = quantum_circuit(4)


qc.x([0])
qc.x([1])
qc.u3([3] ,{ "theta": "global_1", "phi": "global_2", "lambda": np.pi/2 })


# qc.u3(3 ,{ "theta": "global_1", "phi": "global_2", "lambda": np.pi/2 })
# c = my_circuit = [
# { "gate": "x", "target": [0] },
# { 'gate': 'cx', 'target': [0,2] },
# { 'gate': 'h', 'target':[2] }
# ]
# params={ "global_1": np.pi/2, "global_2": 3*np.pi/2 }

qc.run(params={ "global_1": np.pi/2, "global_2": 3*np.pi/2 })
counts = qc.get_counts(1000)
print(counts)